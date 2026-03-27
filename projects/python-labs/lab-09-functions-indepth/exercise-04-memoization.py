import time
from functools import lru_cache


def symbol_metadata_uncached(symbol: str) -> dict:
    time.sleep(0.01)  # 10ms
    return {
        "symbol": symbol,
        "exchange": "NASDAQ",
        "lot_size": 100,
        "currency": "USD",
    }


@lru_cache(maxsize=None)
def symbol_metadata_cached(symbol: str) -> tuple:
    time.sleep(0.01)
    return (
        symbol,
        "NASDAQ",
        100,
        "USD",
    )


def benchmark_uncached():
    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    start = time.perf_counter()

    for i in range(1000):
        symbol_metadata_uncached(symbols[i % 5])

    return time.perf_counter() - start


def benchmark_cached():
    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    start = time.perf_counter()

    for i in range(1000):
        symbol_metadata_cached(symbols[i % 5])

    return time.perf_counter() - start


uncached_time = benchmark_uncached()
cached_time = benchmark_cached()

print(f"Uncached: {uncached_time:.4f}s")
print(f"Cached:   {cached_time:.4f}s")
print(f"Speedup:  {uncached_time / cached_time:.2f}x")