import asyncpraw
import os
from dotenv import load_dotenv
import aiohttp
import certifi
import ssl
from asyncio import gather

# SSL Context to Avoid Certificate Verification Errors
ssl_context = ssl.create_default_context(cafile=certifi.where())

# Load environment variables from .env
load_dotenv()

# Reddit Authentication (singleton instance)
reddit = asyncpraw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)


async def fetch_multiple_reddit_comments(posts):
    """
    Fetch comments for multiple Reddit posts concurrently.

    :param posts: List of Reddit posts (with IDs).
    :return: Flattened list of comments across all posts.
    """
    tasks = [fetch_reddit_comments(post["id"]) for post in posts]
    all_comments = await gather(*tasks)
    return [comment for comments in all_comments for comment in comments if comments]


# Fetch Reddit posts based on a query
async def fetch_reddit_posts(query: str, subreddits: list = None, limit: int = 5):
    """
    Fetch Reddit posts by querying multiple subreddits concurrently.

    :param query: Search term (e.g., dish or restaurant name).
    :param subreddits: List of subreddits to search in.
    :param limit: Max number of posts to fetch from each subreddit.
    :return: List of matching posts.
    """
    posts = []
    subreddits = subreddits or ["food", "Cooking", "AskCulinary", "FoodPorn", "restaurants"]

    tasks = [search_reddit_multiple_subs(query, [subreddit], limit) for subreddit in subreddits]
    results = await gather(*tasks)

    # Flatten results and remove duplicates by post ID
    all_posts = [post for subreddit_posts in results for post in subreddit_posts]
    unique_posts = list({post["id"]: post for post in all_posts}.values())

    print(f"Fetched {len(unique_posts)} Reddit posts for '{query}'")
    return unique_posts


# Fetch comments for a specific Reddit post
async def fetch_reddit_comments(post_id: str):
    """
    Fetch comments from a specific Reddit post by ID.

    :param post_id: Reddit post ID.
    :return: List of comments from the post.
    """
    comments = []
    try:
        submission = await reddit.submission(id=post_id)
        await submission.load()

        for top_level_comment in submission.comments:
            if isinstance(top_level_comment, asyncpraw.models.Comment):
                comments.append({
                    "body": top_level_comment.body,
                    "score": top_level_comment.score,
                    "created_at": top_level_comment.created_utc
                })
        print(f"Fetched {len(comments)} Reddit comments for post '{post_id}'")
        return comments
    except Exception as e:
        print(f"Error fetching Reddit comments: {str(e)}")
        return []


# Fetch reviews from Reddit comments
async def fetch_reddit_reviews(dish_name: str, restaurant_name: str = None, location: str = None, limit: int = 5):
    """
    Search for dish or restaurant reviews in Reddit comments.

    :param dish_name: Name of the dish.
    :param restaurant_name: (Optional) Restaurant name.
    :param location: (Optional) Location.
    :param limit: Number of results to fetch.
    :return: List of relevant comments matching the dish/restaurant.
    """
    reviews = []
    subreddits = ["food", "FoodPorn", "restaurants"]

    if location:
        subreddits.append(location.lower())  # Add location-specific subreddit dynamically

    query = f"{dish_name} {restaurant_name or ''}".strip()

    try:
        tasks = [fetch_reddit_posts(query,  subreddits=[subreddit] , limit = limit) for subreddit in subreddits]
        results = await gather(*tasks)

        for posts in results:
            tasks = [fetch_reddit_comments(post["id"]) for post in posts]
            comments = await gather(*tasks)

            # Flatten and filter matching comments
            for post_comments in comments:
                for comment in post_comments:
                    if dish_name.lower() in comment["body"].lower() or (
                        restaurant_name and restaurant_name.lower() in comment["body"].lower()
                    ):
                        reviews.append(comment)

        print(f"Fetched {len(reviews)} Reddit reviews for '{dish_name}'")
        return reviews
    except Exception as e:
        print(f"Error fetching Reddit reviews: {str(e)}")
        return []


# Perform a search across multiple subreddits
async def search_reddit_multiple_subs(query: str, subreddits: list, limit: int = 5):
    """
    Perform a full-text search across multiple subreddits.

    :param query: Search term (dish or restaurant).
    :param subreddits: List of subreddits to search.
    :param limit: Number of posts to return per subreddit.
    :return: List of search results.
    """
    results = []
    try:
        for subreddit in subreddits:
            subreddit_obj = await reddit.subreddit(subreddit)
            async for post in subreddit_obj.search(query, limit=limit, sort="relevance"):
                results.append({
                    "title": post.title,
                    "url": post.url,
                    "body": post.selftext,
                    "subreddit": subreddit,
                    "score": post.score,
                    "id": getattr(post, "id", None)
                })
        print(f"Fetched {len(results)} results for '{query}' across subreddits.")
        return results
    except Exception as e:
        print(f"Error searching Reddit: {str(e)}")
        return []


# Fallback to comment search if post search fails
async def fetch_reddit_fallback(query: str, location: str = None, limit: int = 5):
    """
    Perform fallback search in case post search yields no results.

    :param query: Search term.
    :param location: (Optional) Location filter.
    :param limit: Number of comments to fetch.
    :return: List of comments or fallback results.
    """
    subreddits = ["food", "travel", "restaurants"]
    if location:
        subreddits.append(location.lower())

    print(f"Performing Reddit fallback search for '{query}'")

    results = await search_reddit_multiple_subs(query, subreddits, limit)

    if not results:
        return await fetch_reddit_reviews(query, location=location, limit=limit)
    return results
