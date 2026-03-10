from pathlib import Path
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
UNIVERSE_CONFIG_PATH = PROJECT_ROOT / "configs" / "universe.yaml"


def unique_preserve_order(items):
    seen = set()
    out = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def load_tickers(path=UNIVERSE_CONFIG_PATH):
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    if not data:
        return []

    ticker_section = data.get("tickers")

    if isinstance(ticker_section, list):
        return unique_preserve_order(ticker_section)

    if isinstance(ticker_section, dict):
        tickers = []
        for value in ticker_section.values():
            if isinstance(value, list):
                tickers.extend(value)
        return unique_preserve_order(tickers)

    tickers = []
    for value in data.values():
        if isinstance(value, list):
            tickers.extend(value)

    return unique_preserve_order(tickers)


TICKERS = load_tickers()