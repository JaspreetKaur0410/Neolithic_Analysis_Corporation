
class FundamentalEngine:
    def score(self, info: dict, market_pe: float = 20.0) -> dict:
        pe = info.get("trailingPE") or info.get("forwardPE")
        peg = info.get("pegRatio"); roe = info.get("returnOnEquity")
        rg  = info.get("revenueGrowth"); d2e = info.get("debtToEquity")
        dy  = info.get("dividendYield"); pm  = info.get("profitMargins")
        score = 50.0
        if pe is not None:
            if pe < 10: score += 8
            elif pe > 40: score -= 6
        if peg is not None:
            if peg < 1.0: score += 6
            elif peg > 2.0: score -= 6
        if roe is not None:
            if roe > 0.20: score += 6
            elif roe < 0:  score -= 6
        if rg is not None:
            if rg > 0.08: score += 6
            elif rg < 0:  score -= 6
        if d2e is not None:
            if d2e < 0.5: score += 4
            elif d2e > 2: score -= 4
        if pm is not None:
            if pm > 0.20: score += 4
            elif pm < 0.02: score -= 3
        if dy is not None and dy > 0.03:
            score += 3
        return {"score": float(max(0,min(100,score)))}
