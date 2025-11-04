
import logging, os
from logging.handlers import RotatingFileHandler

def setup_logging(debug: bool = False) -> logging.Logger:
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger("neolithic")
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    if not logger.handlers:
        fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        fh = RotatingFileHandler("logs/neolithic.log", maxBytes=2_000_000, backupCount=3)
        fh.setFormatter(fmt); fh.setLevel(logging.DEBUG if debug else logging.INFO)
        sh = logging.StreamHandler()
        sh.setFormatter(fmt); sh.setLevel(logging.DEBUG if debug else logging.INFO)
        logger.addHandler(fh); logger.addHandler(sh)

    for noisy in ("yfinance", "urllib3", "fsspec", "numexpr"):
        try:
            logging.getLogger(noisy).setLevel(logging.ERROR)
        except Exception:
            pass

    return logger
