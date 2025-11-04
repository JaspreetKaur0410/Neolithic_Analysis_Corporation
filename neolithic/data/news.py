
from typing import List
import requests, feedparser

class GoogleNewsRSS:
    def headlines(self, query: str, limit: int = 30) -> List[str]:
        try:
            url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
            text = requests.get(url, timeout=10).text
            feed = feedparser.parse(text)
            out, seen = [], set()
            for e in feed.entries[:limit]:
                t = (e.title or "").strip()
                if t and t.lower() not in seen:
                    seen.add(t.lower()); out.append(t)
            return out
        except Exception:
            return []

class NewsAPIProvider:
    def __init__(self, api_key: str):
        self.api_key = api_key
    def headlines(self, query: str, limit: int = 30) -> List[str]:
        try:
            url = f"https://newsapi.org/v2/everything?q={query}&pageSize={limit}"
            r = requests.get(url, headers={"X-Api-Key": self.api_key}, timeout=10)
            r.raise_for_status()
            js = r.json()
            return [a.get("title","") for a in js.get("articles", []) if a.get("title")]
        except Exception:
            return []
