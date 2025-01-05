from pydantic import BaseModel
from typing import List, Optional

# Menu Request Model (For LLM Decoding)
class MenuRequest(BaseModel):
    menu_text: str

# Decoded Dish Model
class DecodedDish(BaseModel):
    name: str
    description: Optional[str] = None
    recommended_addon: Optional[str] = None

# LLM Menu Decoding Response
class MenuDecodeResponse(BaseModel):
    original_menu: str
    decoded_items: List[DecodedDish]
