# main.py: FastAPI app for News Aggregator
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from rss_parser import fetch_rss_feed

app = FastAPI(title="News Aggregator API")

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