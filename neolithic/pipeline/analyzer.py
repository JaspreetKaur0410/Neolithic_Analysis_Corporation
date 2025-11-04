
from typing import Dict
from ..data.base import MarketDataProvider
from ..features.technical import TechnicalEngine
from ..features.fundamentals import FundamentalEngine
from ..features.macro import MacroEngine
from ..features.sentiment import SentimentAggregator
from ..features.candles import CandlePatternDetector
from ..scoring.regimes import RegimeDetector
from ..scoring.fusion import FusionStrategy
from ..risk.stops import StopTargetEngine
from ..risk.position import PositionSizer

class Analyzer:
    def __init__(self, market: MarketDataProvider, macro, sent: SentimentAggregator, fast_mode: bool = False, macro_tilt: float = 0.10):
        self.market = market
        self.macro_engine = MacroEngine(macro)
        self.sent = sent
        self.fast = fast_mode
        self.macro_tilt = macro_tilt
        self.tech = TechnicalEngine()
        self.fund = FundamentalEngine()
        self.candles = CandlePatternDetector()
        self.regimes = RegimeDetector()
        self.fusion = FusionStrategy()
        self.stops = StopTargetEngine()
        self.sizer = PositionSizer()

    def analyze_one(self, ticker: str, capital: float, risk_pct: float) -> Dict[str, object]:
        df = self.market.candles(ticker)
        info = self.market.info(ticker)
        if df is None or df.empty:
            raise RuntimeError(f"No data for {ticker}")
        df_ta, m = self.tech.compute(df)
        cfa = self.fund.score(info)["score"]
        regime = self.regimes.detect(df_ta)
        macro = self.macro_engine.score()
        sent = self.sent.score(ticker)
        quant = 50.0
        if m["rsi"] == m["rsi"]:
            quant += (m["rsi"] - 50) * 0.3
        if m["sma20"] and m["sma50"] and m["sma200"]:
            quant += (10 if m["close"] > m["sma20"] else -5)
            quant += (10 if m["close"] > m["sma50"] else -5)
            quant += (10 if m["close"] > m["sma200"] else -5)
        quant = float(max(0, min(100, quant)))
        final = self.fusion.combine(cfa, quant, sent, macro, regime, self.macro_tilt)
        verdict = "BUY" if final >= 66 else ("SELL" if final <= 44 else "HOLD")
        atr = m["atr"] if (m["atr"] == m["atr"] and m["atr"] > 0) else 0.02*m["close"]
        tg = self.stops.compute(m["close"], atr, m["sma20"], m["sma50"], m["sma200"], regime, cfa)
        shares, rps = self.sizer.shares(capital, risk_pct, atr)
        return {
            "Timestamp": "",
            "Ticker": ticker,
            "Sector": info.get("sector",""),
            "Regime": regime,
            "CFA": round(cfa,1),
            "Quant": round(quant,1),
            "Sentiment": round(sent,1),
            "Macro": round(macro,1),
            "Final": round(final,1),
            "Verdict": verdict,
            "LastClose": round(m["close"],2),
            "RSI14": round(m["rsi"],1) if m["rsi"]==m["rsi"] else "",
            "ATR": round(atr,3),
            "ST_Stop": tg["short"]["stop"], "ST_Target": tg["short"]["target"],
            "MT_Stop": tg["medium"]["stop"], "MT_Target": tg["medium"]["target"],
            "LT_Stop": tg["long"]["stop"], "LT_Target": tg["long"]["target"],
            "Shares": shares, "Risk/Share": round(rps,2)
        }
