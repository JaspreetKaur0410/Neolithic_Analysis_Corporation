
class PositionSizer:
    def shares(self, capital: float, risk_pct: float, atr_abs: float, atr_mult: float = 2.0):
        risk_dollars = max(0.0, capital) * (risk_pct / 100.0)
        risk_per_share = max(0.5, atr_abs * atr_mult)
        return int(risk_dollars // risk_per_share), risk_per_share
