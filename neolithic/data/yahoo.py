
"""Yahoo Finance-backed data provider (quiet, compatible, with fallback)."""
import time, io, contextlib, warnings
import pandas as pd
import yfinance as yf
from typing import Optional
from .base import MarketDataProvider, MacroDataProvider

MAX_RETRIES = 3

def _silent_download(ticker: str, period: str, interval: str) -> pd.DataFrame:
    out = pd.DataFrame()
    buf_out, buf_err = io.StringIO(), io.StringIO()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
            try:
                out = yf.download(
                    tickers=ticker,
                    period=period,
                    interval=interval,
                    progress=False,
                    auto_adjust=True,
                )
            except Exception:
                out = pd.DataFrame()
            if out is None or out.empty:
                try:
                    t = yf.Ticker(ticker)
                    out = t.history(period=period, interval=interval, auto_adjust=True)
                except Exception:
                    out = pd.DataFrame()
    if out is not None and not out.empty and isinstance(out.columns, pd.MultiIndex):
        out.columns = [c[0] for c in out.columns]
    return out if out is not None else pd.DataFrame()

class YahooProvider(MarketDataProvider, MacroDataProvider):
    def candles(self, ticker: str, period: str = "24mo", interval: str = "1d") -> pd.DataFrame:
        for attempt in range(1, MAX_RETRIES + 1):
            df = _silent_download(ticker=ticker, period=period, interval=interval)
            if df is not None and not df.empty:
                return df
            time.sleep(0.5 * attempt)
        df = _silent_download(ticker=ticker, period="6mo", interval="1d")
        return df if df is not None else pd.DataFrame()

    def info(self, ticker: str) -> dict:
        try:
            return yf.Ticker(ticker).info
        except Exception:
            return {}

    def pct_change(self, symbol: str, period: str = "5d") -> Optional[float]:
        df = self.candles(symbol, period=period, interval="1d")
        if df is None or df.empty or "Close" not in df:
            return None
        try:
            c0, c1 = float(df["Close"].iloc[0]), float(df["Close"].iloc[-1])
            return (c1 / c0) - 1.0
        except Exception:
            return None
