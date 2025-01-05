import pytest
import asyncio
from utils.reddit_utils import fetch_reddit_posts


@pytest.mark.asyncio
async def test_fetch_reddit_posts():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        response = await fetch_reddit_posts("pulled pork sandwich", 5)
        assert isinstance(response, list)
        assert len(response) > 0  # Ensure non-empty response
    finally:
        loop.close()
