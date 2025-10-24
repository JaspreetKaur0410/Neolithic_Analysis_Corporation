"""End-to-end smoke test for Analyzer with fake providers."""
from neolithic.features.sentiment import SentimentAggregator
from neolithic.pipeline.analyzer import Analyzer

def test_pipeline_smoke(fakes):
    sent = SentimentAggregator(fakes["news_providers"], enable=True, fast=True)
    analyzer = Analyzer(
        market=fakes["market"],
        macro=fakes["macro"],
        sent=sent,
        fast_mode=True,
        macro_tilt=0.10
    )
    row = analyzer.analyze_one("AAPL", capital=10000.0, risk_pct=1.0)
    assert row["Verdict"] in {"BUY","HOLD","SELL"}
    assert 0 <= row["CFA"] <= 100
    assert 0 <= row["Quant"] <= 100
    assert 0 <= row["Sentiment"] <= 100
    assert 0 <= row["Macro"] <= 100
    assert 0 <= row["Final"] <= 100
    assert row["LastClose"] > 0
    assert row["ATR"] > 0
