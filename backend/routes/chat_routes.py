from uuid import UUID
from fastapi import APIRouter, HTTPException, Query
from models.chat_models import ChatCreateRequest, Message
from services.chat_service import (
    create_new_chat,
    process_followup_message,
    send_message,
    get_chat_history,
    get_library,
)

router = APIRouter()


def is_valid_uuid(uuid_to_test: str, version: int = 4) -> bool:
    """
    Validate whether a given string is a valid UUID.
    """
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


@router.post("/chat/new")
async def create_chat(request: ChatCreateRequest):
    """
    Create a new chat and send the first message.
    """
    try:
        chatId = request.chatId
        title = request.title

        # Validate that 'chatId' is a valid UUID
        if not is_valid_uuid(chatId):
            raise HTTPException(status_code=400, detail="Invalid 'chatId'. Must be a valid UUID.")

        # Pass chatId to the service function
        return await create_new_chat(chatId, title)
    except HTTPException as e:
        raise e  # Re-raise HTTPExceptions for proper status codes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat/{chat_id}/send-message")
async def send_chat_message(
    chat_id: str,
    dish_name: str = Query(..., description="Name of the dish."),
    restaurant_name: str = Query(None, description="Name of the restaurant (optional)."),
    location: str = Query(..., description="Location of the restaurant."),
    user_query: str = Query(None, description="User's specific question about the dish."),
    limit: int = Query(10, description="Number of results to return."),
):
    """
    Send a message in an existing chat.
    """
    try:
        # Pass query parameters to the service function
        return await send_message(
            chat_id=chat_id,
            dish_name=dish_name,
            restaurant_name=restaurant_name,
            location=location,
            user_query=user_query,
            limit=limit
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}")

@router.post("/chat/{chat_id}/followup-message")
async def send_followup_message(
    chat_id: str,
    user_query: str = Query(..., description="User's specific follow-up question."),
):
    """
    Handle follow-up messages in an existing chat.
    """
    try:
        # Pass query parameters to the follow-up service function
        return await process_followup_message(chat_id=chat_id, user_query=user_query)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process follow-up message: {str(e)}")
    
@router.get("/chat/{chat_id}")
async def fetch_chat_history(chat_id: str):
    """
    Fetch the full history of a specific chat.
    """
    try:
        return {"messages": await get_chat_history(chat_id)}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/library")
async def fetch_library():
    """
    Fetch all saved chats in the library.
    """
    return await get_library()


# @router.delete("/library/{chat_id}")
# async def delete_library_item_route(chat_id: str):
#     """
#     Delete a specific saved chat from the library.
#     """
    
