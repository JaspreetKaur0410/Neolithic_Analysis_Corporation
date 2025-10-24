
from typing import List
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentAggregator:
    def __init__(self, providers: List, enable: bool = True, fast: bool = False):
        self.providers = providers
        self.enable = enable
        self.fast = fast
        self.sid = SentimentIntensityAnalyzer()
    def score(self, query: str) -> float:
        if not self.enable:
            return 50.0
        titles = []
        for p in self.providers:
            try:
                limit = 10 if self.fast else 30
                titles.extend(p.headlines(f"{query} stock", limit=limit))
            except Exception:
                continue
        if not titles: return 50.0
        seen, uniq = set(), []
        for t in titles:
            k = t.lower().strip()
            if k and k not in seen:
                seen.add(k); uniq.append(t)
        scores = [self.sid.polarity_scores(t)["compound"] for t in uniq]
        avg = float(np.mean(scores)) if scores else 0.0
        return float(np.clip(50 + avg*50, 0, 100))
