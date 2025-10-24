"""Basic sanity checks for stop/target logic."""
from neolithic.risk.stops import StopTargetEngine

def test_stop_target_basic():
    eng = StopTargetEngine()
    price = 100.0
    atr = 2.0
    out = eng.compute(price, atr, 98.0, 97.0, 95.0, "trend", 70.0)
    assert out["short"]["stop"] > 0
    assert out["short"]["target"] > price
    assert out["medium"]["target"] >= out["short"]["target"]
