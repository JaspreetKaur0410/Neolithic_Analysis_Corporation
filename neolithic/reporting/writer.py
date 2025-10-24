
import os, csv, datetime as dt
from dateutil.tz import gettz
def write_csv(rows, out_dir: str = "reports", tz: str = "America/Detroit"):
    os.makedirs(out_dir, exist_ok=True)
    day = dt.datetime.now(gettz(tz)).strftime("%Y%m%d")
    daydir = os.path.join(out_dir, day)
    os.makedirs(daydir, exist_ok=True)
    path = os.path.join(daydir, "report.csv")
    header = ["Timestamp","Ticker","Sector","Regime","CFA","Quant","Sentiment","Macro","Final","Verdict",
              "LastClose","RSI14","ATR","ST_Stop","ST_Target","MT_Stop","MT_Target","LT_Stop","LT_Target","Shares","Risk/Share"]
    new = not os.path.exists(path)
    with open(path, "a", newline="") as f:
        w = csv.writer(f)
        if new: w.writerow(header)
        for r in rows: w.writerow([r.get(h,"") for h in header])
