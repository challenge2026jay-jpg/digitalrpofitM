import os
import sys
from datetime import datetime, timedelta, timezone
from math import sqrt
from polygon import RESTClient


def get_client():
    api_key = os.getenv("POLYGON_API_KEY")
    if not api_key:
        print("Error: POLYGON_API_KEY not found in environment.")
        sys.exit(1)
    return RESTClient(api_key=api_key)


def fetch_closes(client, ticker, days=30, timespan="day"):
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    aggs = list(client.list_aggs(
        ticker, 1, timespan,
        start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"),
        limit=5000, sort="asc"
    ))
    return [float(a.close) for a in aggs if getattr(a, "close", None) is not None]


def returns(values):
    return [(values[i] / values[i - 1]) - 1 for i in range(1, len(values)) if values[i - 1]]


def pearson(xs, ys):
    n = min(len(xs), len(ys))
    xs, ys = xs[-n:], ys[-n:]
    if n < 3:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    numerator = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    denominator = sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
    return numerator / denominator if denominator else None


def analyze_volume(ticker, timespan="hour", multiplier=1, limit=24):
    client = get_client()
    end = datetime.now(timezone.utc)
    aggs = client.list_aggs(
        ticker, multiplier, timespan,
        (end - timedelta(days=7)).strftime("%Y-%m-%d"),
        end.strftime("%Y-%m-%d"), limit=limit, sort="desc"
    )
    print(f"--- Volume Analysis for {ticker} ---")
    for agg in aggs:
        stamp = getattr(agg, "timestamp", None)
        dt = datetime.fromtimestamp(stamp / 1000, tz=timezone.utc) if stamp else "n/a"
        print(f"{dt} | Close: {agg.close} | Vol: {getattr(agg, 'volume', 'n/a')}")


def check_correlation(ticker1="I:DXY", ticker2="C:XAUUSD", days=30):
    client = get_client()
    first = returns(fetch_closes(client, ticker1, days))
    second = returns(fetch_closes(client, ticker2, days))
    value = pearson(first, second)
    print(f"--- Correlation Check: {ticker1} vs {ticker2} ({days} days) ---")
    if value is None:
        print("Insufficient overlapping data to calculate correlation.")
    else:
        print(f"Pearson correlation of daily returns: {value:.3f}")
        print("Interpretation: inverse bias" if value < -0.2 else "Interpretation: weak or positive relationship")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python polygon_trading.py <volume|correlation> [ticker]")
        sys.exit(1)
    action = sys.argv[1]
    if action == "volume":
        analyze_volume(sys.argv[2] if len(sys.argv) > 2 else "C:XAUUSD")
    elif action == "correlation":
        check_correlation()
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)
