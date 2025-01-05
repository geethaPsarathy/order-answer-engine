from fastapi import APIRouter, Query, HTTPException
from models.dish_model import DishModel
from services.menu_service import decode_menu_service

router = APIRouter()

@router.get("/decode-menu", response_model=DishModel)
async def decode_menu(
    dish_name: str = Query(..., description="Name of the dish to decode."),
    restaurant_name: str = Query(None, description="Name of the restaurant (optional)."),
    location: str = Query(..., description="Location of the restaurant."),
    user_query: str = Query(None, description="User's specific question about the dish."),
    limit: int = Query(10, description="Number of results to return for Yelp and Reddit."),
):
    """
    Decode a menu item by fetching insights from Yelp and Reddit.
    """
    return await decode_menu_service(
        dish_name=dish_name,
        restaurant_name=restaurant_name,
        location=location,
        user_query=user_query,
        limit=limit
    )
