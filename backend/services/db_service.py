from motor.motor_asyncio import AsyncIOMotorClient
import redis
from utils.time_utils import calculate_ttl
from utils.error_utils import handle_cache_miss
from models.dish_model import CachedRecommendation
import os
from dotenv import load_dotenv

# # Load .env variables
# load_dotenv()

# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
# client = AsyncIOMotorClient(MONGO_URI)

# # Select the database properly
# db_name = os.getenv("MONGO_DB", "default_db_name")  # Fallback to 'default_db_name' if env var is missing
# db = client[db_name]  # Use the Mongo client to select the database


# Load environment variables from .env
load_dotenv()

# MongoDB Configuration
MONGO_HOST = os.getenv("MONGO_HOST", "mongo")  # Default to 'mongo' service name
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB = os.getenv("MONGO_DB", "fastapi_db")

MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}"
client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]  # Use the correct database

# Redis Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "redis")  # Default to 'redis' service name
REDIS_PORT = os.getenv("REDIS_PORT", 6379)

try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    r.ping()  # Test Redis connection
except redis.ConnectionError as e:
    print(f"Unable to connect to Redis: {e}")

# Collections
chat_collection = db["chats"]
library_collection = db["library"]