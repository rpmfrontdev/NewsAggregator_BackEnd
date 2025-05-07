# Infrastructure layer: Fetch and clean RSS feeds
import feedparser
from bs4 import BeautifulSoup
from typing import List, Optional
from domain.article import Article

def clean_text(html_text: str) -> str:
    """Remove HTML tags and clean text."""
    if not html_text:
        return ""
    soup = BeautifulSoup(html_text, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    return text

def fetch_rss_feed(feed_url: str, max_articles: int = 5) -> List[Article]:
    """Fetch and parse an RSS feed into a list of Articles."""
    try:
        feed = feedparser.parse(feed_url)
        articles = []
        for entry in feed.entries[:max_articles]:
            title = entry.get('title', '')
            description = clean_text(entry.get('description', '') or entry.get('summary', ''))
            link = entry.get('link', '')
            pub_date = entry.get('published', '') or entry.get('updated', '')
            # Extract thumbnail (varies by feed)
            thumbnail = None
            if 'media_thumbnail' in entry:
                thumbnail = entry.media_thumbnail[0].get('url')
            elif 'media_content' in entry:
                for content in entry.media_content:
                    if content.get('medium') == 'image':
                        thumbnail = content.get('url')
                        break
            articles.append(Article(
                title=title,
                summary=description,  # Will be summarized later
                link=link,
                pub_date=pub_date,
                thumbnail=thumbnail
            ))
        return articles
    except Exception as e:
        print(f"Error fetching feed {feed_url}: {e}")
        return []