from motor.motor_asyncio import AsyncIOMotorClient
from utils.time_utils import calculate_ttl
from utils.error_utils import handle_cache_miss
from models.dish_model import CachedRecommendation
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)

# Select the database properly
db_name = os.getenv("MONGO_DB", "default_db_name")  # Fallback to 'default_db_name' if env var is missing
db = client[db_name]  # Use the Mongo client to select the database

# Collections
chat_collection = db["chats"]
library_collection = db["library"]