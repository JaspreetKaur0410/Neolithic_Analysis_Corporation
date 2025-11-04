"""FastAPI service exposing the Analyzer as a REST endpoint."""
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

from neolithic.data.yahoo import YahooProvider
from neolithic.data.news import GoogleNewsRSS, NewsAPIProvider
from neolithic.features.sentiment import SentimentAggregator
from neolithic.pipeline.analyzer import Analyzer

app = FastAPI(title="Neolithic Analysis API", version="0.1.0")

class AnalyzeRequest(BaseModel):
    """POST body for /analyze endpoint."""
    tickers: List[str]
    capital: float = 10000.0
    risk_pct: float = 1.0
    enable_news: bool = True
    fast_mode: bool = False
    macro_tilt: float = 0.10
    newsapi_key: Optional[str] = None

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    """Run analysis for the provided tickers and return JSON results."""
    market = YahooProvider()
    macro = market
    providers = [GoogleNewsRSS()]
    if req.enable_news and req.newsapi_key:
        providers.append(NewsAPIProvider(req.newsapi_key))
    sent = SentimentAggregator(providers, enable=req.enable_news, fast=req.fast_mode)
    analyzer = Analyzer(market=market, macro=macro, sent=sent,
                        fast_mode=req.fast_mode, macro_tilt=req.macro_tilt)

    out = []
    for t in req.tickers:
        row = analyzer.analyze_one(t, capital=req.capital, risk_pct=req.risk_pct)
        out.append(row)
    return {"results": out}

@app.get("/health")
def health():
    """Basic liveness probe."""
    return {"status": "ok"}
