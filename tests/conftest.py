"""Pytest fixtures with synthetic market data for fast, deterministic tests."""
import pandas as pd
import numpy as np
import datetime as dt
import pytest

class FakeMarket:
    def __init__(self, trend=True):
        self.trend = trend

    def candles(self, ticker: str, period: str = "24mo", interval: str = "1d") -> pd.DataFrame:
        n = 200
        idx = pd.bdate_range(end=dt.datetime.today(), periods=n)
        base = np.linspace(100, 120, n) if self.trend else np.linspace(110, 90, n)
        noise = np.random.normal(0, 0.5, n)
        close = base + noise
        open_ = close + np.random.normal(0, 0.2, n)
        high = np.maximum(open_, close) + np.abs(np.random.normal(0.2, 0.1, n))
        low  = np.minimum(open_, close) - np.abs(np.random.normal(0.2, 0.1, n))
        vol  = np.random.randint(1000000, 1500000, n)
        df = pd.DataFrame({
            "Open": open_, "High": high, "Low": low, "Close": close, "Volume": vol
        }, index=idx)
        return df

    def info(self, ticker: str) -> dict:
        return {
            "sector": "Technology",
            "trailingPE": 25.0,
            "pegRatio": 1.2,
            "returnOnEquity": 0.20,
            "revenueGrowth": 0.08,
            "debtToEquity": 0.6,
            "dividendYield": 0.01,
            "profitMargins": 0.18
        }

    def pct_change(self, symbol: str, period: str = "5d"):
        return 0.0

class FakeMacro(FakeMarket):
    pass

class FakeNewsProvider:
    def headlines(self, query: str, limit: int = 30):
        return [f"{query} beats earnings expectations", f"{query} launches new product"]

@pytest.fixture
def fakes():
    return {
        "market": FakeMarket(trend=True),
        "macro": FakeMacro(),
        "news_providers": [FakeNewsProvider()]
    }
