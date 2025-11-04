
import pandas as pd, numpy as np
import pandas_ta as ta
from typing import Tuple, Dict

class TechnicalEngine:
    def compute(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, float]]:
        d = df.copy()
        d.ta.rsi(length=14, append=True)
        d.ta.macd(append=True)
        d.ta.sma(length=20, append=True)
        d.ta.sma(length=50, append=True)
        d.ta.sma(length=200, append=True)
        d.ta.atr(length=14, append=True)
        d.ta.adx(length=14, append=True)
        d.ta.bbands(length=20, std=2, append=True)
        d["OBV"] = ta.obv(d["Close"], d["Volume"])
        tp = (d["High"]+d["Low"]+d["Close"])/3.0
        year = pd.to_datetime(d.index).year
        d["VWAP"] = tp.mul(d["Volume"]).groupby(year).cumsum() / d["Volume"].groupby(year).cumsum()
        d["VWAP_Dist"] = (d["Close"] - d["VWAP"]) / d["Close"]
        last = d.iloc[-1]
        metrics = {
            "close": float(last["Close"]),
            "rsi": float(last.get("RSI_14", np.nan)),
            "atr": float(last.get("ATR_14", np.nan)),
            "sma20": float(last.get("SMA_20", np.nan)),
            "sma50": float(last.get("SMA_50", np.nan)),
            "sma200": float(last.get("SMA_200", np.nan)),
        }
        return d, metrics
