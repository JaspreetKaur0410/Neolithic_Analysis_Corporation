
from dataclasses import dataclass
@dataclass
class FusionWeights:
    w_cfa: float; w_quant: float; w_sent: float; macro_tilt: float
class FusionStrategy:
    def weights(self, regime: str) -> FusionWeights:
        if regime == "trend":  return FusionWeights(0.45, 0.40, 0.15, 0.10)
        if regime == "range":  return FusionWeights(0.35, 0.45, 0.20, 0.10)
        if regime == "crash":  return FusionWeights(0.25, 0.55, 0.20, 0.10)
        return FusionWeights(0.40, 0.40, 0.20, 0.10)
    def combine(self, cfa: float, quant: float, sent: float, macro: float, regime: str, user_macro_tilt: float) -> float:
        w = self.weights(regime)
        base = w.w_cfa*cfa + w.w_quant*quant + w.w_sent*sent
        tilt = user_macro_tilt if user_macro_tilt is not None else w.macro_tilt
        return float(max(0, min(100, base + tilt*(macro-50))))
