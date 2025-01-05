from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Message(BaseModel):
    chatId: str
    content: str
    role: str
    createdAt: datetime = Field(default_factory=datetime.now)
    
class Chat(BaseModel):
    chatId: str
    messages: List[Message]

class LibraryItem(BaseModel):
    chatId: str
    title: str  # Title for the saved chat (e.g., first user query)
    createdAt: datetime


class ChatCreateRequest(BaseModel):
    chatId: str = Field(..., description="Unique chat ID (UUID)")
    title: str = Field(..., description="Title for the chat (e.g., first user query)")