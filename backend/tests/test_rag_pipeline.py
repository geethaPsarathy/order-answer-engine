import pytest
from httpx import AsyncClient
from main import app  # Assuming your FastAPI app is in main.py


@pytest.mark.asyncio
async def test_decode_menu_success():
    """
    Test the /decode-menu endpoint for a successful response.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/decode-menu",
            params={
                "dish_name": "BBQ Burger",
                "restaurant_name": "Smokehouse Grill",
                "location": "Austin",
                "limit": 3
            }
        )
        assert response.status_code == 200
        json_response = response.json()

        assert "dish_name" in json_response
        assert "insights" in json_response
        assert "source" in json_response
        assert json_response["dish_name"] == "BBQ Burger"
        assert len(json_response["insights"]) > 0


@pytest.mark.asyncio
async def test_decode_menu_yelp_fail():
    """
    Simulate Yelp data failure by providing an invalid location.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/decode-menu",
            params={
                "dish_name": "Nonexistent Dish",
                "restaurant_name": "Unknown Place",
                "location": "Nowhere",
                "limit": 2
            }
        )
        assert response.status_code == 404
        assert "detail" in response.json()
        assert "No Yelp results" in response.json()["detail"]


@pytest.mark.asyncio
async def test_decode_menu_partial_results():
    """
    Test partial results when one data source (Reddit or Yelp) fails.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/decode-menu",
            params={
                "dish_name": "Garlic Pasta",
                "restaurant_name": "",
                "location": "Los Angeles",
                "limit": 3
            }
        )
        assert response.status_code == 200
        json_response = response.json()

        assert json_response["dish_name"] == "Garlic Pasta"
        assert "insights" in json_response
        assert len(json_response["insights"]) >= 0


@pytest.mark.asyncio
async def test_decode_menu_invalid_params():
    """
    Test API validation for missing required parameters.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/decode-menu")
        assert response.status_code == 422  # Unprocessable Entity
        assert "detail" in response.json()
