from utils.cache_utils import get_from_cache, set_to_cache
from fastapi import HTTPException
from asyncio import gather, wait_for
from services.RAG.rag_service import process_rag_pipeline
from utils.yelp_utils import fetch_yelp_data, fetch_yelp_reviews_for_businesses
from utils.reddit_utils import fetch_reddit_posts, fetch_multiple_reddit_comments
from services.RAG.indexing_service import update_faiss_index
from services.RAG.search_service import faiss_only_search
from services.llm_service import generate_customizations, generate_suggestions, generate_dish_insight

async def decode_menu_service(
    dish_name: str,
    restaurant_name: str,
    location: str,
    user_query: str,
    limit: int
) -> dict:
    """
    Service to decode a menu item by fetching insights from Yelp and Reddit.
    """
    try:
        # Create a unique cache key based on input parameters
        cache_key = f"decode_menu:{dish_name}:{restaurant_name}:{location}:{limit}"
        
        # Step 0: Check if data is already cached (up to Step 5)
        cached_data = await get_from_cache(cache_key)
        if cached_data:
            print("[INFO] Returning data from cache...")
            intermediate_results = cached_data
        else:
            yelp_data, yelp_reviews, reddit_comments = None, None, []

            print(f"[INFO] Decoding menu item: {dish_name} at {restaurant_name} in {location}...")

            # Step 1: Fetch Yelp data
            try:
                yelp_data = await fetch_yelp_data(
                    query=f"{dish_name} at {restaurant_name}" if restaurant_name else f"{dish_name}",
                    location=location,
                    limit=limit,
                )
                if not yelp_data:
                    raise HTTPException(status_code=404, detail=f"No Yelp results for '{dish_name}' in '{location}'.")
            except Exception as e:
                print(f"Yelp Error: {e}")

            # Fetch Yelp reviews if Yelp data is available
            if yelp_data:
                business_ids = [business["id"] for business in yelp_data]
                print("Fetching Yelp reviews...")
                if business_ids:
                    tasks = [fetch_yelp_reviews_for_businesses([business_id]) for business_id in business_ids]
                    yelp_reviews_list = await gather(*tasks)
                    yelp_reviews = [review for reviews in yelp_reviews_list for review in reviews]
                    print(f"[INFO] Fetched {len(yelp_reviews)} reviews.")

            # Step 2: Fetch Reddit data
            subreddits = ["food", "restaurants", "Cooking", "Allrecipes"]
            reddit_tasks = [fetch_reddit_posts(f"{dish_name} {restaurant_name}", [sub], limit) for sub in subreddits]
            reddit_posts = await wait_for(gather(*reddit_tasks), timeout=15)

            for posts in reddit_posts:
                top_posts = sorted(posts, key=lambda x: x['score'], reverse=True)[:10]
                comments = await fetch_multiple_reddit_comments(top_posts) if top_posts else []
                reddit_comments.extend(comments)

            print(f"[INFO] Fetched {len(reddit_comments)} Reddit comments.")

            # Step 3: Update FAISS if new data is available
            print(f"[INFO] Updating FAISS index...")
            if yelp_reviews or reddit_comments:
                await update_faiss_index(yelp_reviews, reddit_comments)
                print(f"[INFO] FAISS index updated.")

            # Step 4: Perform Hybrid Search with Weighted Combination
            print(f"[INFO] Performing hybrid search...")
            hybrid_results = faiss_only_search(dish_name, k=limit)

            # Step 5: Process through RAG pipeline for final summarization
            print(f"[INFO] Generating insights...")
            response = await process_rag_pipeline(
                dish_name=dish_name,
                yelp_reviews=yelp_reviews or hybrid_results,
                reddit_comments=reddit_comments or []
            )

            # Cache intermediate results (Steps 1-5)
            intermediate_results = {
                "name": dish_name,
                "dish_name": dish_name,
                "restaurant_name": restaurant_name or "Unknown",
                "location": location or "Unknown",
                "rating": None,
                "review_count": None,
                "summarized_reviews": response["insights"],
                "source": response["source"],
                "yelp_data": yelp_data,
                "yelp_reviews": yelp_reviews,
                "reddit_comments": reddit_comments,
                "hybrid_results": hybrid_results
            }
            
            # Store the intermediate results in the cache with a TTL (e.g., 1 hour)
            await set_to_cache(cache_key, intermediate_results)

        # LLM-related steps (Final Insights and Suggestions)
        print(f"[INFO] Generating insights with LLM...")
        final_insight = await generate_dish_insight(dish_name, intermediate_results["summarized_reviews"])

        print(f"[INFO] Generating customizations and suggestions...")
        customizations, suggestions = await wait_for(
            gather(
                generate_customizations(dish_name, intermediate_results["summarized_reviews"], user_query),
                generate_suggestions(dish_name, intermediate_results["summarized_reviews"])
            ),
            timeout=30  # Timeout after 30 seconds
        )
        
        # final response from /decode-menu
        print("[INFO] Decoding menu completed.")
        

        # Return structured response including LLM-generated content
        return {
            "name": dish_name,
            "dish_name": dish_name,
            "restaurant_name": restaurant_name or "Unknown",
            "location": location or "Unknown",
            "rating": None,
            "review_count": None,
            "summarized_reviews": intermediate_results["summarized_reviews"],
            # **intermediate_results,
            "insights": [final_insight],
            "customizations": customizations,
            "ingredients": suggestions["ingredients"],
            "beverages": suggestions["beverages"],
            "flavors": suggestions["flavors"],
            "desserts": suggestions["desserts"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to decode menu: {str(e)}")
