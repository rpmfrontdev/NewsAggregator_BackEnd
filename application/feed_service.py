# Application layer:  RSS feed processing
from typing import List
from domain.article import Article, simple_summarize
from infrastructure.rss_repository import fetch_rss_feed

def process_rss_feed(feed_url: str, max_articles: int = 5) -> List[Article]:
    """Fetch, clean, and summarize articles from an RSS feed."""
    articles = fetch_rss_feed(feed_url, max_articles)
    # Summarize descriptions
    for article in articles:
        article.summary = simple_summarize(article.summary, max_sentences=2)
    return articles