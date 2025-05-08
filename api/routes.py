# API layer: FastAPI routes for serving articles
from fastapi import APIRouter, HTTPException
from typing import List
from domain.article import Article
from application.feed_service import process_rss_feed

# Initialize router
router = APIRouter()

# Define supported feeds
FEEDS = {
    'skynews': 'https://feeds.skynews.com/feeds/rss/home.xml',
    'bbc': 'https://feeds.bbci.co.uk/news/rss.xml',
    'guardian': 'https://www.theguardian.com/world/rss'
}

@router.get("/articles", response_model=List[Article])
async def get_articles(feed: str, max_articles: int = 5):
    """Fetch and summarize articles for a given feed."""
    if feed not in FEEDS:
        raise HTTPException(status_code=400, detail=f"Invalid feed. Supported feeds: {list(FEEDS.keys())}")
    try:
        articles = process_rss_feed(FEEDS[feed], max_articles)
        if not articles:
            raise HTTPException(status_code=404, detail=f"No articles found for feed: {feed}")
        return articles
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing feed {feed}: {str(e)}")