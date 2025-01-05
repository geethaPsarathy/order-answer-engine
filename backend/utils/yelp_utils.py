import aiohttp
import os
from utils.error_utils import handle_api_error
from dotenv import load_dotenv
import ssl
import certifi

ssl_context = ssl.create_default_context(cafile=certifi.where())

load_dotenv()

YELP_API_KEY = os.getenv("YELP_API_KEY")
YELP_SEARCH_ENDPOINT = "https://api.yelp.com/v3/businesses/search"
YELP_REVIEWS_ENDPOINT = "https://api.yelp.com/v3/businesses/{}/reviews"

# Pagination for Yelp Search (fetch up to 50 businesses)
async def fetch_yelp_data(query: str, location: str, limit: int = 20):
    """
    Fetch businesses from Yelp matching the dish and location.

    :param dish_name: Name of the dish to search for.
    :param location: Location of the restaurant.
    :param limit: Number of businesses to fetch.
    :return: List of businesses.
    """
    headers = {
        "Authorization": f"Bearer {YELP_API_KEY}",
        "Content-Type": "application/json"
    }
    results = []
    offset = 0
    max_results = limit

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        try:
            while len(results) < max_results:
                params = {
                    "term": query,
                    "location": location,
                    "limit": min(50, max_results - len(results)),  # Max 50 per request
                    "offset": offset,
                    "sort_by": "best_match"
                }

                async with session.get(YELP_SEARCH_ENDPOINT, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        businesses = data.get('businesses', [])
                        results.extend(businesses)
                        offset += len(businesses)
                        
                        if len(businesses) == 0:  # No more results to fetch
                            break
                    else:
                        raise Exception(f"Yelp API Error: {response.status} - {await response.text()}")
            print(f"Fetched {len(results)} Yelp businesses for '{query}' in '{location}'")
            return results
        except Exception as e:
            handle_api_error(e)
            return []
        finally:
            await session.close()


# Fetch multiple reviews by iterating through businesses
async def fetch_yelp_reviews_for_businesses(businesses: list, min_reviews: int = 3):
    """
    Fetch reviews for each business and ensure at least 10 reviews are aggregated.

    :param businesses: List of Yelp businesses.
    :param min_reviews: Minimum reviews required.
    :return: Aggregated list of reviews.
    """
    headers = {
        "Authorization": f"Bearer {YELP_API_KEY}",
        "Content-Type": "application/json"
    }
    aggregated_reviews = []

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        try:
            print(f"Fetching reviews for {len(businesses)} businesses...")
            for business_id in businesses:
                print(f"Fetching reviews for {business_id}...")
                
                url = YELP_REVIEWS_ENDPOINT.format(business_id)
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        reviews = data.get("reviews", [])
                        aggregated_reviews.extend(reviews)

                        print(f"Fetched {len(reviews)} reviews")

                        # Stop once we reach the required number of reviews
                        if len(aggregated_reviews) >= min_reviews:
                            return aggregated_reviews
                    else:
                        print(f"Failed to fetch reviews")
                        continue
            return aggregated_reviews
        except Exception as e:
            handle_api_error(e)
            return []
        finally:
            await session.close()

