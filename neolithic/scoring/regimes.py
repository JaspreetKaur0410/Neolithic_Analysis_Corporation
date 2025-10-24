
import numpy as np, pandas as pd
class RegimeDetector:
    def detect(self, df: pd.DataFrame) -> str:
        if len(df) < 60: return "neutral"
        last = df.iloc[-1]
        s200 = float(last.get("SMA_200", last["Close"]))
        close = float(last["Close"])
        adx = float(last.get("ADX_14", np.nan))
        bbw = float(last.get("BBB_20_2.0", np.nan))
        bbw_med = float(np.nanmedian(df["BBB_20_2.0"].tail(120))) if "BBB_20_2.0" in df else np.nan
        trending = (np.isfinite(adx) and adx >= 25) and (np.isfinite(bbw) and np.isfinite(bbw_med) and bbw > bbw_med)
        ranging = (np.isfinite(adx) and adx <= 18) and (np.isfinite(bbw) and np.isfinite(bbw_med) and bbw < bbw_med)
        crashy  = (close < s200)
        if crashy: return "crash"
        if trending: return "trend"
        if ranging: return "range"
        return "neutral"
