
import argparse, json, os
from .config import AppConfig
from .logging_config import setup_logging
from .data.yahoo import YahooProvider
from .data.news import GoogleNewsRSS, NewsAPIProvider
from .features.sentiment import SentimentAggregator
from .pipeline.analyzer import Analyzer
from .reporting.writer import write_csv
from .reporting.console import verdict_table

def load_config_file(path: str = "config.json") -> dict:
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}

def parse_args():
    ap = argparse.ArgumentParser(description="Neolithic v4.1 Modular Analyzer")
    ap.add_argument("--tickers", nargs="*", help="Override tickers")
    ap.add_argument("--capital", type=float)
    ap.add_argument("--risk-pct", type=float)
    ap.add_argument("--no-news", action="store_true")
    ap.add_argument("--fast", action="store_true")
    ap.add_argument("--macro-tilt", type=float)
    ap.add_argument("--newsapi-key", type=str, default=os.getenv("NEWSAPI_KEY"))
    ap.add_argument("--debug", action="store_true")
    return ap.parse_args()

def main():
    args = parse_args()
    logger = setup_logging(debug=args.debug)

    cfg_raw = load_config_file()
    cfg = AppConfig(**{**AppConfig().model_dump(), **cfg_raw})

    if args.tickers: cfg.tickers = args.tickers
    if args.capital is not None: cfg.capital = args.capital
    if args.risk_pct is not None: cfg.risk_pct = args.risk_pct
    if args.no_news: cfg.enable_news = False
    if args.fast: cfg.fast_mode = True
    if args.macro_tilt is not None: cfg.macro_tilt = args.macro_tilt

    market = YahooProvider()
    macro_provider = market
    providers = [GoogleNewsRSS()]
    if cfg.enable_news and args.newsapi_key:
        providers.append(NewsAPIProvider(args.newsapi_key))
    sent = SentimentAggregator(providers, enable=cfg.enable_news, fast=cfg.fast_mode)

    analyzer = Analyzer(market=market, macro=macro_provider, sent=sent,
                        fast_mode=cfg.fast_mode, macro_tilt=cfg.macro_tilt)

    rows = []
    for t in cfg.tickers:
        try:
            row = analyzer.analyze_one(t, capital=cfg.capital, risk_pct=cfg.risk_pct)
            rows.append(row)
            verdict_table(t, {
                "Sector": row["Sector"],
                "Regime": row["Regime"],
                "CFA": row["CFA"],
                "Quant": row["Quant"],
                "Sentiment": row["Sentiment"],
                "Macro": row["Macro"],
                "Final": row["Final"],
                "Verdict": row["Verdict"],
                "LastClose": row["LastClose"],
                "RSI14": row["RSI14"],
                "ATR": row["ATR"],
                "ST Stop/Target": f"{row['ST_Stop']} / {row['ST_Target']}",
                "MT Stop/Target": f"{row['MT_Stop']} / {row['MT_Target']}",
                "LT Stop/Target": f"{row['LT_Stop']} / {row['LT_Target']}",
                "Sizing (shares) / Risk/Share": f"{row['Shares']} / {row['Risk/Share']}",
            })
        except Exception as e:
            logger.exception(f"Failed {t}: {e}")

    if rows:
        write_csv(rows, out_dir=cfg.out_dir, tz=cfg.timezone)

if __name__ == "__main__":
    main()
