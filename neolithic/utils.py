
import numpy as np
import datetime as dt
from dateutil.tz import gettz

def now_str(tz: str = "America/Detroit") -> str:
    return dt.datetime.now(gettz(tz)).strftime("%Y-%m-%d %H:%M")
