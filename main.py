# main.py: FastAPI app for News Aggregator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from rss_parser import fetch_rss_feed
import os

app = FastAPI(title="News Aggregator API")

# Add CORS middleware to allow iOS app requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Article(BaseModel):
    link: str
    title: str
    summary: str
    pubDate: str
    thumbnail: Optional[str] = None

@app.get("/")
async def root():
    """Return a welcome message to confirm the API is operational."""
    return {"message": "News Aggregator API is running!"}

@app.get("/articles", response_model=list[Article])
async def get_articles(feed: str = "skynews", max_articles: int = 50, category: str = "all"):
    """
    Fetch articles from the specified feed with optional category filtering.
    """
    articles = await fetch_rss_feed(feed, max_articles, category)
    return articles

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import Optional
# from rss_parser import fetch_rss_feed

# app = FastAPI(title="News Aggregator API")

# class Article(BaseModel):
#     link: str
#     title: str
#     summary: str
#     pubDate: str
#     thumbnail: Optional[str] = None

# @app.get("/")
# async def root():
#     """Return a welcome message to confirm the API is operational."""
#     return {"message": "News Aggregator API is running!"}

# @app.get("/articles", response_model=list[Article])
# async def get_articles(feed: str = "skynews", max_articles: int = 50, category: str = "all"):
#     """
#     Fetch articles from the specified feed with optional category filtering.
#     """
#     articles = await fetch_rss_feed(feed, max_articles, category)
#     return articles