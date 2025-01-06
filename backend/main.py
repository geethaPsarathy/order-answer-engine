from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import aioredis
import os
import asyncio
from routes import router as api_router

# Load environment variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB", "fastapi_db")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# FastAPI App
app = FastAPI(
    title="Dish Recommender API",
    description="An API to recommend popular dishes, decode menus, and suggest hidden local favorites.",
    version="1.0.0"
)

# CORS Configuration
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global MongoDB and Redis Clients
mongo_client = None
db = None
redis = None


@app.on_event("startup")
async def startup_event():
    global mongo_client, db, redis
    max_retries = 5
    retry_interval = 5  # seconds

    # Connect to MongoDB
    for attempt in range(max_retries):
        try:
            mongo_client = AsyncIOMotorClient(MONGO_URI)
            db = mongo_client[MONGO_DB_NAME]

            # Ensure DB and collections exist
            db_names = await mongo_client.list_database_names()
            if MONGO_DB_NAME not in db_names:
                print(f"[INFO] Creating database '{MONGO_DB_NAME}'...")

            collections = await db.list_collection_names()
            if "chats" not in collections:
                print("[INFO] Creating 'chats' collection...")
                await db.create_collection("chats")

            if "library" not in collections:
                print("[INFO] Creating 'library' collection...")
                await db.create_collection("library")

            print("[INFO] Connected to MongoDB.")
            break
        except Exception as e:
            print(f"[ERROR] MongoDB not ready, retrying in {retry_interval} seconds... (Attempt {attempt + 1}/{max_retries})")
            await asyncio.sleep(retry_interval)
    else:
        print("[ERROR] Unable to connect to MongoDB after multiple attempts.")

    # Connect to Redis
    for attempt in range(max_retries):
        try:
            redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", decode_responses=True)
            await redis.ping()
            print("[INFO] Connected to Redis.")
            break
        except Exception as e:
            print(f"[ERROR] Redis not ready, retrying in {retry_interval} seconds... (Attempt {attempt + 1}/{max_retries})")
            await asyncio.sleep(retry_interval)
    else:
        print("[ERROR] Unable to connect to Redis after multiple attempts.")


@app.on_event("shutdown")
async def shutdown_event():
    global mongo_client, redis
    if mongo_client:
        mongo_client.close()
        print("[INFO] MongoDB connection closed.")
    
    if redis:
        await redis.close()
        print("[INFO] Redis connection closed.")


# Include the centralized router
app.include_router(api_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Dish Recommender API"}
