from services.llm_service import generate_response_from_messages
from .menu_service import decode_menu_service
from .db_service import chat_collection, library_collection
from models.chat_models import LibraryItem, Message
from datetime import datetime
from uuid import uuid4
from fastapi import HTTPException


async def create_new_chat(chatId: str, title: str)  -> dict:
    """
    Create a new chat and return a success message.
    """
    try:
        # Initialize the chat with an empty messages list
        await chat_collection.insert_one({"chatId": chatId, "messages": []})
        
        # Create a record in the library collection
        library_item = LibraryItem(
            chatId=chatId,
            title=title,
            createdAt=datetime.utcnow()
        )
        await library_collection.insert_one(library_item.dict())

        # Return success response
        return {"message": "Chat created successfully", "chatId": chatId}

    except Exception as e:
        # Handle any unexpected errors
        raise HTTPException(status_code=500, detail=f"Unexpected Error: {str(e)}")



async def send_message(
    chat_id: str,
    dish_name: str,
    restaurant_name: str = None,
    location: str = "Unknown",
    user_query: str = None,
    limit: int = 10
) -> dict:
    """
    Add a user message to an existing chat and generate an assistant response.
    """
    # Check if the chat exists
    existing_chat = await chat_collection.find_one({"chatId": chat_id})
    if not existing_chat:
        raise ValueError("Chat not found")

    # Create a user message dictionary
    user_message = {
        "messageId": str(uuid4()),
        "createdAt": datetime.now(),
        "content": {
            "dish_name": dish_name,
            "restaurant_name": restaurant_name, 
            "location": location, 
            "user_query": user_query
        },
        "role": "user"
    }

    # Add user message to the chat
    await chat_collection.update_one(
        {"chatId": chat_id},
        {"$push": {"messages": user_message}}
    )

    # Call /decode-menu to process the user's query
    try:
        # Simulate calling /decode-menu with required parameters
        assistant_response = await decode_menu_service(
            dish_name=dish_name,
            restaurant_name=restaurant_name,
            location=location,
            user_query=user_query,
            limit=limit
        )

        # Format assistant's response
        assistant_message = {
            "messageId": str(uuid4()),
            "chatId": chat_id,
            "createdAt": datetime.now(),
            "content": assistant_response,  # Final response from /decode-menu
            "role": "assistant",
        }

        # Add assistant response to the chat
        await chat_collection.update_one(
            {"chatId": chat_id},
            {"$push": {"messages": assistant_message}}
        )

        # Fetch updated messages from the database
        updated_chat = await chat_collection.find_one({"chatId": chat_id})
        return {"messages": updated_chat["messages"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}")


async def process_followup_message(chat_id: str, user_query: str) -> dict:
    """
    Process a follow-up message and generate a response based on chat history.
    """
    # Check if the chat exists
    existing_chat = await chat_collection.find_one({"chatId": chat_id})
    if not existing_chat:
        raise ValueError("Chat not found")

    # Create a user message dictionary
    user_message = {
        "messageId": str(uuid4()),
        "createdAt": datetime.now(),
        "content": {"user_query": user_query},
        "role": "user"
    }

    # Add user message to the chat
    await chat_collection.update_one(
        {"chatId": chat_id},
        {"$push": {"messages": user_message}}
    )

    try:
        # Generate response from chat history using LLM
        print("[INFO] Generating response from chat history...")
        
        # Call the LLM helper function (ensure it's correctly handled)
        assistant_response = await generate_response_from_messages(  # Remove 'await' if not async
            messages=existing_chat["messages"],
            user_query=user_query
        )

        # Format assistant's response
        assistant_message = {
            "messageId": str(uuid4()),
            "chatId": chat_id,
            "createdAt": datetime.now(),
            "content": assistant_response,
            "role": "assistant",
        }

        # Add assistant response to the chat
        await chat_collection.update_one(
            {"chatId": chat_id},
            {"$push": {"messages": assistant_message}}
        )

        # Fetch updated messages from the database
        updated_chat = await chat_collection.find_one({"chatId": chat_id})
        return {"messages": updated_chat["messages"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process follow-up message: {str(e)}")

async def get_chat_history(chat_id: str) -> list:
    """
    Retrieve the full history of a specific chat.
    """
    existing_chat = await chat_collection.find_one({"chatId": chat_id})
    
    if not existing_chat:
        raise ValueError("Chat not found")
    
    return existing_chat["messages"]


# Helper function to convert MongoDB document
def serialize_document(document):
    document["_id"] = str(document["_id"])  # Convert ObjectId to string
    return document


async def get_library() -> list:
    """
    Retrieve all saved chats in the library.
    """
    library_items = await library_collection.find().to_list(length=100)
    
    # Serialize each item to handle ObjectId
    return [serialize_document(item) for item in library_items]

async def delete_library_item(chat_id: str) -> None:
    """
    Delete a specific saved chat from the library and its history.
    """
    # Remove from library collection
    await library_collection.delete_one({"chatId": chat_id})

    # Remove associated messages from chats collection
    await chat_collection.delete_one({"chatId": chat_id})
