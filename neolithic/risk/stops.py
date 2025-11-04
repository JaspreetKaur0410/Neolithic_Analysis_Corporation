
class StopTargetEngine:
    def compute(self, price: float, atr: float, sma20: float, sma50: float, sma200: float, regime: str, fund_score: float):
        if atr is None or atr <= 0: atr = max(0.02*price, 0.5)
        st_mult, mt_mult, lt_mult = (2.0, 3.0, 5.0)
        if regime == "range": st_mult, mt_mult, lt_mult = (1.2, 1.8, 3.5)
        if regime == "crash": st_mult, mt_mult, lt_mult = (1.0, 1.5, 3.0)
        st_stop   = max(0.01, price - st_mult*atr)
        st_target = price + st_mult*atr
        mt_stop   = min(sma20 or price, sma50 or price) - (mt_mult-1.0)*atr
        mt_target = max(sma20 or price, sma50 or price) + mt_mult*atr
        lt_stop   = (sma200 or price) - 3*atr
        lt_target = (sma200 or price) + lt_mult*atr
        if fund_score >= 70: lt_target *= 1.10
        elif fund_score <= 40: lt_target *= 0.90
        max_move = 8*atr
        st_target = min(price + max_move, st_target)
        mt_target = min(price + 2*max_move, mt_target)
        lt_target = min(price + 3*max_move, lt_target)
        return {
            "short":  {"stop": round(st_stop,2), "target": round(st_target,2)},
            "medium": {"stop": round(mt_stop,2), "target": round(mt_target,2)},
            "long":   {"stop": round(lt_stop,2), "target": round(lt_target,2)}
        }
