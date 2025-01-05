from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

class DishModel(BaseModel):
    name: str
    dish_name: str
    restaurant_name: Optional[str] = None
    location: Optional[str] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    summarized_reviews: List[str]
    insights: List[str]
    source: str
    customizations: Optional[List[str]] = []
    ingredients: Optional[List[str]] = []

# Cache Response Schema
class CachedRecommendation(BaseModel):
    id: str = Field(alias="_id")  # MongoDB uses _id for primary keys
    location: str
    dish_type: Optional[str] = None
    data: List[DishModel]
    expires_at: datetime
