# Domain layer: Pure business logic for articles and summarization
from dataclasses import dataclass
from typing import Optional
import nltk
from nltk.tokenize import sent_tokenize

# Download NLTK resources (punkt and punkt_tab) if not present
def ensure_nltk_resources():
    """Ensure NLTK punkt and punkt_tab resources are downloaded."""
    for resource in ['punkt', 'punkt_tab']:
        try:
            nltk.data.find(f'tokenizers/{resource}')
        except LookupError:
            print(f"Downloading NLTK resource: {resource}")
            nltk.download(resource, quiet=True)

# Run resource check on module import
ensure_nltk_resources()

@dataclass
class Article:
    """Represents a news article with cleaned and summarized content."""
    title: str
    summary: str
    link: str
    pub_date: str
    thumbnail: Optional[str]

def simple_summarize(text: str, max_sentences: int = 2) -> str:
    """Summarize text by extracting the first few sentences."""
    if not text:
        return ""
    sentences = sent_tokenize(text)
    summary = ' '.join(sentences[:min(max_sentences, len(sentences))])
    return summary.strip()