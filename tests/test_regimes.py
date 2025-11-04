"""Smoke tests for regime detection wiring."""
from neolithic.scoring.regimes import RegimeDetector
from neolithic.features.technical import TechnicalEngine

def test_regime_detector_trend(fakes):
    df = fakes["market"].candles("AAPL")
    tech = TechnicalEngine()
    d, _ = tech.compute(df)
    regime = RegimeDetector().detect(d)
    assert regime in {"trend","neutral","range","crash"}
