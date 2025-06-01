# rss_parser.py: RSS feed parsing and category filtering
# compatibility with python 3.9 for koyeb deployment
import feedparser
import httpx
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime
import re

# Pydantic model for article
class Article(BaseModel):
    link: str
    title: str
    summary: str
    pubDate: str
    thumbnail: Optional[str] = None

# Feed URLs (updated Sky News and BBC to HTTPS)
FEED_URLS = {
    "skynews": "https://feeds.skynews.com/feeds/rss/home.xml",
    "bbc": "https://feeds.bbci.co.uk/news/rss.xml",
    "guardian": "https://www.theguardian.com/world/rss"
}

# Category keywords for filtering
CATEGORY_KEYWORDS = {
    "politics": [
        "election", "government", "parliament", "policy", "brexit", "congress",
        "president", "prime minister", "legislation", "vote", "democracy", "bill",
        "senate", "campaign", "tax", "diplomacy"
    ],
    "sports": [
        "football", "cricket", "rugby", "tennis", "olympics", "athletics",
        "basketball", "match", "tournament", "score", "team", "champion",
        "sport", "game", "player"
    ],
    "technology": [
        "tech", "software", "hardware", "ai", "artificial intelligence", "gadget",
        "smartphone", "internet", "cybersecurity", "data", "innovation", "app",
        "technology", "digital", "device", "bacteria"  # Space station article
    ]
}

RSS_CATEGORY_MAPPING = {
    "sport": "sports",
    "sports news": "sports",
    "politics": "politics",
    "political": "politics",
    "uk politics": "politics",
    "world politics": "politics",
    "us politics": "politics",
    "technology": "technology",
    "tech": "technology",
    "science/technology": "technology",
    "science": "technology"
}

async def fetch_rss_feed(feed: str, max_articles: int, category: str) -> List[Dict[str, Any]]:
    """
    Fetch articles from an RSS feed and filter by category.
    
    Args:
        feed: News feed source (e.g., skynews, bbc, guardian).
        max_articles: Maximum number of articles to return.
        category: Category to filter (e.g., all, politics, sports, technology).
    
    Returns:
        List of articles in JSON-compatible format.
    """
    print(f"Fetching feed: {feed}, category: {category}")
    if feed not in FEED_URLS:
        print(f"Invalid feed: {feed}")
        return []
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(FEED_URLS[feed], timeout=10.0)
            print(f"Response status: {response.status_code}")
            response.raise_for_status()
            feed_data = feedparser.parse(response.text)
            print(f"Entries found: {len(feed_data.entries)}")
        
        articles = []
        for entry in feed_data.entries[:max_articles]:
            title = entry.get("title", "No title")
            link = entry.get("link", "")
            summary = entry.get("summary", entry.get("description", "No summary"))
            pub_date = entry.get("published", entry.get("updated", datetime.now().isoformat()))
            
            thumbnail = None
            if "media_thumbnail" in entry and entry.media_thumbnail:
                thumbnail = entry.media_thumbnail[0].get("url")
            elif "media_content" in entry and entry.media_content:
                thumbnail = entry.media_content[0].get("url")
            elif "enclosures" in entry and entry.enclosures:
                for enc in entry.enclosures:
                    if enc.get("type", "").startswith("image"):
                        thumbnail = enc.get("href")
            
            summary = re.sub(r"<[^>]+>", "", summary)
            
            article = Article(
                link=link,
                title=title,
                summary=summary[:200],
                pubDate=pub_date,
                thumbnail=thumbnail
            )
            
            print(f"Article: {title}, RSS Categories: {[cat.term for cat in entry.get('tags', [])]}")
            
            if category == "all":
                print(f"Including article (all): {title}")
                articles.append(article.dict())
            else:
                rss_categories = [cat.term.lower() for cat in entry.get("tags", [])]
                mapped_categories = [RSS_CATEGORY_MAPPING.get(cat, cat) for cat in rss_categories]
                text = (title.lower() + " " + summary.lower())
                keywords_match = any(keyword in text for keyword in CATEGORY_KEYWORDS.get(category, []))
                print(f"Checking category {category}: Mapped tags {mapped_categories}, Keywords match: {keywords_match}")
                if category in mapped_categories or keywords_match:
                    print(f"Including article: {title}")
                    articles.append(article.dict())
            
        print(f"Filtered articles: {len(articles)}")
        return articles
    
    except Exception as e:
        print(f"Error fetching RSS feed {feed}: {e}")
        return []

# import feedparser
# import httpx
# from typing import List, Dict, Any
# from pydantic import BaseModel
# from datetime import datetime
# import re

# # Pydantic model for article
# class Article(BaseModel):
#     link: str
#     title: str
#     summary: str
#     pubDate: str
#     thumbnail: str | None = None

# # Feed URLs (updated Sky News and BBC to HTTPS)
# FEED_URLS = {
#     "skynews": "https://feeds.skynews.com/feeds/rss/home.xml",
#     "bbc": "https://feeds.bbci.co.uk/news/rss.xml",
#     "guardian": "https://www.theguardian.com/world/rss"
# }

# # Category keywords for filtering
# CATEGORY_KEYWORDS = {
#     "politics": [
#         "election", "government", "parliament", "policy", "brexit", "congress",
#         "president", "prime minister", "legislation", "vote", "democracy", "bill",
#         "senate", "campaign", "tax", "diplomacy"
#     ],
#     "sports": [
#         "football", "cricket", "rugby", "tennis", "olympics", "athletics",
#         "basketball", "match", "tournament", "score", "team", "champion",
#         "sport", "game", "player"
#     ],
#     "technology": [
#         "tech", "software", "hardware", "ai", "artificial intelligence", "gadget",
#         "smartphone", "internet", "cybersecurity", "data", "innovation", "app",
#         "technology", "digital", "device", "bacteria"  # Space station article
#     ]
# }

# RSS_CATEGORY_MAPPING = {
#     "sport": "sports",
#     "sports news": "sports",
#     "politics": "politics",
#     "political": "politics",
#     "uk politics": "politics",
#     "world politics": "politics",
#     "us politics": "politics",
#     "technology": "technology",
#     "tech": "technology",
#     "science/technology": "technology",
#     "science": "technology"
# }

# async def fetch_rss_feed(feed: str, max_articles: int, category: str) -> List[Dict[str, Any]]:
#     """
#     Fetch articles from an RSS feed and filter by category.
    
#     Args:
#         feed: News feed source (e.g., skynews, bbc, guardian).
#         max_articles: Maximum number of articles to return.
#         category: Category to filter (e.g., all, politics, sports, technology).
    
#     Returns:
#         List of articles in JSON-compatible format.
#     """
#     print(f"Fetching feed: {feed}, category: {category}")
#     if feed not in FEED_URLS:
#         print(f"Invalid feed: {feed}")
#         return []
    
#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.get(FEED_URLS[feed], timeout=10.0)
#             print(f"Response status: {response.status_code}")
#             response.raise_for_status()
#             feed_data = feedparser.parse(response.text)
#             print(f"Entries found: {len(feed_data.entries)}")
        
#         articles = []
#         for entry in feed_data.entries[:max_articles]:
#             title = entry.get("title", "No title")
#             link = entry.get("link", "")
#             summary = entry.get("summary", entry.get("description", "No summary"))
#             pub_date = entry.get("published", entry.get("updated", datetime.now().isoformat()))
            
#             thumbnail = None
#             if "media_thumbnail" in entry and entry.media_thumbnail:
#                 thumbnail = entry.media_thumbnail[0].get("url")
#             elif "media_content" in entry and entry.media_content:
#                 thumbnail = entry.media_content[0].get("url")
#             elif "enclosures" in entry and entry.enclosures:
#                 for enc in entry.enclosures:
#                     if enc.get("type", "").startswith("image"):
#                         thumbnail = enc.get("href")
            
#             summary = re.sub(r"<[^>]+>", "", summary)
            
#             article = Article(
#                 link=link,
#                 title=title,
#                 summary=summary[:200],
#                 pubDate=pub_date,
#                 thumbnail=thumbnail
#             )
            
#             print(f"Article: {title}, RSS Categories: {[cat.term for cat in entry.get('tags', [])]}")
            
#             if category == "all":
#                 print(f"Including article (all): {title}")
#                 articles.append(article.dict())
#             else:
#                 rss_categories = [cat.term.lower() for cat in entry.get("tags", [])]
#                 mapped_categories = [RSS_CATEGORY_MAPPING.get(cat, cat) for cat in rss_categories]
#                 text = (title.lower() + " " + summary.lower())
#                 keywords_match = any(keyword in text for keyword in CATEGORY_KEYWORDS.get(category, []))
#                 print(f"Checking category {category}: Mapped tags {mapped_categories}, Keywords match: {keywords_match}")
#                 if category in mapped_categories or keywords_match:
#                     print(f"Including article: {title}")
#                     articles.append(article.dict())
            
#         print(f"Filtered articles: {len(articles)}")
#         return articles
    
#     except Exception as e:
#         print(f"Error fetching RSS feed {feed}: {e}")
#         return []

    