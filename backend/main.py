from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router as api_router
from utils.cache_utils import redis


app = FastAPI(
    title="Dish Recommender API",
    description="An API to recommend popular dishes, decode menus, and suggest hidden local favorites.",
    version="1.0.0"
)

# CORS Configuration
origins = [
    "http://localhost:3000",  # Frontend development server
    "http://127.0.0.1:3000",  # Alternative localhost IP
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.on_event("startup")
async def startup_event():
    """
    Event triggered when the application starts.
    Ensures Redis connection is ready.
    """
    try:
        await redis.ping()
        print("[INFO] Connected to Redis.")
    except Exception as e:
        print(f"[ERROR] Unable to connect to Redis: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Event triggered when the application shuts down.
    Closes the Redis connection.
    """
    await redis.close()


# Include the centralized router
app.include_router(api_router)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Dish Recommender API"}
