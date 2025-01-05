from fastapi import APIRouter, Query, HTTPException
from models.dish_model import DishModel
from services.RAG.rag_service import process_rag_pipeline
from utils.yelp_utils import fetch_yelp_data, fetch_yelp_reviews_for_businesses
from services.RAG.indexing_service import update_faiss_index
from services.llm_service import generate_customizations, generate_suggestions
from asyncio import gather, wait_for, TimeoutError

router = APIRouter()

@router.get("/menu-decode", response_model=DishModel)
async def decode_menu(
    dish_name: str = Query(..., description="Name of the dish to decode."),
    location: str = Query(..., description="Location of the restaurant."),
    user_query: str = Query(..., description="User's specific question about the dish."),
    limit: int = Query(10, description="Number of reviews to fetch."),
):
    """
    Decode a menu item by fetching insights from Yelp and generating customizations based on user queries.
    """
    try:
        yelp_reviews = []
        print(f"[INFO] Fetching reviews for '{dish_name}' in {location}...")

        yelp_data = await fetch_yelp_data(dish_name, location, limit)
        business_ids = [business["id"] for business in yelp_data]
        tasks = [fetch_yelp_reviews_for_businesses([business_id]) for business_id in business_ids]
        yelp_reviews_list = await gather(*tasks)
        yelp_reviews = [review for sublist in yelp_reviews_list for review in sublist]

        # Update FAISS index
        update_faiss_index(yelp_reviews)

        # Perform RAG Pipeline
        response = await process_rag_pipeline(dish_name, yelp_reviews)
        
        # Generate customizations
        customizations, suggestions = await gather(
            generate_customizations(dish_name, response["insights"], user_query),
            generate_suggestions(dish_name, response["insights"])
        )

        return {
            "name": dish_name,
            "dish_name": dish_name,
            "location": location,
            "insights": response["insights"],
            "customizations": customizations,
            "ingredients": suggestions["ingredients"],
            "beverages": suggestions["beverages"],
            "flavors": suggestions["flavors"],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to decode menu: {str(e)}")
