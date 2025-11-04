
import pandas as pd
from typing import Dict
class CandlePatternDetector:
    def detect(self, df: pd.DataFrame) -> Dict[str, bool]:
        out = {"bull_engulf":False,"bear_engulf":False,"hammer":False,"shooting_star":False,"doji":False}
        if len(df) < 2: return out
        o1,h1,l1,c1 = [float(df.iloc[-1][x]) for x in ["Open","High","Low","Close"]]
        o2,h2,l2,c2 = [float(df.iloc[-2][x]) for x in ["Open","High","Low","Close"]]
        body1 = abs(c1-o1); rng1 = max(1e-9, h1-l1)
        bull = c1>o1; bear2 = o2>c2
        if bull and bear2 and (min(o1,c1)<=min(o2,c2)) and (max(o1,c1)>=max(o2,c2)) and body1>abs(c2-o2)*0.8:
            out["bull_engulf"]=True
        if rng1>0 and (body1/rng1)<=0.1: out["doji"]=True
        return out
