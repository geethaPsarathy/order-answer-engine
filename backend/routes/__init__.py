from fastapi import APIRouter

from .chat_routes import router as chat_routes
# from .recommend import router as recommend_router
from .decode_menu import router as decode_menu_router
# from .hidden_gems import router as hidden_gems_router

router = APIRouter()

# Register all routes here
# router.include_router(recommend_router)
router.include_router(decode_menu_router)
router.include_router(chat_routes)
# router.include_router(hidden_gems_router)
