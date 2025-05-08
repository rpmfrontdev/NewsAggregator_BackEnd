# Main entry point: Initialize FastAPI app and include routes
from fastapi import FastAPI
from api.routes import router

# Initialize the FastAPI app
app = FastAPI(title="News Aggregator API")

# Include API routes
app.include_router(router)

# Root endpoint for health check
@app.get("/")
async def root():
    """Return a welcome message to confirm the API is operational."""
    return {"message": "News Aggregator API is running!"}