
"""Macro scoring from broad market indicators (ETF-first)."""
class MacroEngine:
    def __init__(self, macro_provider):
        self.pv = macro_provider
    def _pct(self, *symbols):
        for s in symbols:
            v = self.pv.pct_change(s)
            if v is not None:
                return v
        return None
    def score(self) -> float:
        score = 50.0
        dxy = self._pct("UUP", "^DXY")
        tnx = self._pct("^TNX", "IEF")
        vix = self._pct("VIXY", "^VIX")
        spy = self._pct("SPY", "^GSPC")
        if dxy is not None: score += 10 if dxy < 0 else -10
        if tnx is not None: score += 10 if tnx < 0 else -10
        if vix is not None: score += 5 if vix > 0 else -5
        if spy is not None: score += 5 if spy > 0 else -5
        return float(max(0, min(100, score)))
