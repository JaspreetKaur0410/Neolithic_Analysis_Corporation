
from typing import Protocol, Optional
import pandas as pd

class MarketDataProvider(Protocol):
    def candles(self, ticker: str, period: str = "24mo", interval: str = "1d") -> pd.DataFrame: ...
    def info(self, ticker: str) -> dict: ...

class MacroDataProvider(Protocol):
    def pct_change(self, symbol: str, period: str = "5d") -> Optional[float]: ...
