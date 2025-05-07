# Import FastAPI for creating the API server
from fastapi import FastAPI

# Initialize the FastAPI app
app = FastAPI()

# Define a simple root endpoint to verify the server is running
@app.get("/")
async def root():
    """Return a welcome message to confirm the API is operational."""
    return {"message": "News Aggregator API is running!"}