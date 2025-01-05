from fastapi import HTTPException

# Standardize 500 errors for external API failures
def handle_api_error(error: Exception):
    raise HTTPException(
        status_code=500,
        detail=f"External API Error: {str(error)}"
    )

# Handle missing cache scenarios
def handle_cache_miss():
    raise HTTPException(
        status_code=404,
        detail="No cached data available for this query."
    )
