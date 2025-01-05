# from fastapi import APIRouter, Query, HTTPException
# from backend.services.RAG.rag_service import fetch_dish_recommendations

# router = APIRouter(
#     prefix="/recommend",
#     tags=["Recommendations"]
# )

# @router.get("/")
# async def get_recommendations(
#     location: str = Query(..., description="User location"),
#     dish_type: str = Query(None, description="Type of dish (optional)")
# ):
#     try:
#         recommendations = await fetch_dish_recommendations(location, dish_type)
#         return {
#             "location": location,
#             "dish_type": dish_type or "Any",
#             "recommendations": recommendations
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
