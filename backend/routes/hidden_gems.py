# from fastapi import APIRouter, Query, HTTPException
# from backend.services.RAG.rag_service import fetch_hidden_gems

# router = APIRouter(
#     prefix="/hidden-gems",
#     tags=["Hidden Gems"]
# )

# @router.get("/")
# async def get_hidden_gems(
#     location: str = Query(..., description="Location for hidden gem dishes")
# ):
#     try:
#         hidden_gems = await fetch_hidden_gems(location)
#         return {
#             "location": location,
#             "hidden_gems": hidden_gems
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
