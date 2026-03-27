from __future__ import annotations

import csv
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Generator

# ============================================================
# CONSOLIDATED TRADE PIPELINE
#
# Includes:
# - Day 7: frozen PipelineConfig, frozenset config values, timing block
# - Day 8: config passed explicitly to validate_trade and run_pipeline
# - Day 9: Result pattern in parser, match in orchestrator,
#          custom exception hierarchy for infrastructure errors,
#          guard clauses in validator
# ============================================================


# ============================================================
# CONFIG
# ============================================================

@dataclass(frozen=True)
class PipelineConfig:
    valid_symbols: frozenset[str]
    min_quantity: int
    max_quantity: int
    min_price: float
    max_price: float


# True constant: stays global
VALID_SIDES = {"BUY", "SELL"}


# ============================================================
# RESULT TYPES
# ============================================================

@dataclass(frozen=True)
class Ok:
    value: "Trade"


@dataclass(frozen=True)
class Err:
    error: "ValidationError"


ParseResult = Ok | Err


# ============================================================
# DATA MODELS
# ============================================================

@dataclass
class Trade:
    trade_id: str
    symbol: str
    side: str
    quantity: int
    price: float
    timestamp: datetime
    notional: float = field(default=0.0, init=False)


@dataclass
class ValidationError:
    trade_id: str
    reason: str


@dataclass
class PipelineResult:
    valid_trades: list[Trade]
    invalid_trades: list[ValidationError]
    total_parsed: int


@dataclass
class SymbolStats:
    symbol: str
    trade_count: int = 0
    total_volume: int = 0
    total_notional: float = 0.0
    buy_count: int = 0
    sell_count: int = 0
    min_price: float = float("inf")
    max_price: float = float("-inf")

    @property
    def avg_price(self) -> float:
        return self.total_notional / self.total_volume if self.total_volume else 0.0

    @property
    def vwap(self) -> float:
        return self.total_notional / self.total_volume if self.total_volume else 0.0


# ============================================================
# CUSTOM EXCEPTION HIERARCHY
# Infrastructure/system failures only
# ============================================================

class TradePipelineException(Exception):
    """Base class for trade pipeline infrastructure exceptions."""


class TradeFileNotFoundException(TradePipelineException):
    def __init__(self, filepath: str):
        super().__init__(f"Trade input file not found: {filepath}")
        self.filepath = filepath


class TradeFileOpenException(TradePipelineException):
    def __init__(self, filepath: str, reason: str):
        super().__init__(f"Could not open trade input file '{filepath}': {reason}")
        self.filepath = filepath
        self.reason = reason


class TradeReportWriteException(TradePipelineException):
    def __init__(self, destination: str, reason: str):
        super().__init__(f"Could not write report to '{destination}': {reason}")
        self.destination = destination
        self.reason = reason


# ============================================================
# PARSER
# Result pattern: yields Ok[Trade] | Err
# ============================================================

def parse_trades(filepath: str) -> Generator[ParseResult, None, None]:
    path = Path(filepath)

    if not path.exists():
        raise TradeFileNotFoundException(filepath)

    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                try:
                    trade = Trade(
                        trade_id=row["trade_id"].strip(),
                        symbol=row["symbol"].strip(),
                        side=row["side"].strip().upper(),
                        quantity=int(row["quantity"]),
                        price=float(row["price"]),
                        timestamp=datetime.strptime(
                            row["timestamp"].strip(),
                            "%Y-%m-%d %H:%M:%S",
                        ),
                    )
                    yield Ok(trade)

                except (ValueError, KeyError) as e:
                    yield Err(
                        ValidationError(
                            trade_id=row.get("trade_id", "UNKNOWN"),
                            reason=f"Parse error: {e}",
                        )
                    )

    except OSError as e:
        raise TradeFileOpenException(filepath, str(e)) from e


# ============================================================
# VALIDATOR
# Guard clauses + explicit config
# ============================================================

def validate_trade(trade: Trade, config: PipelineConfig) -> ValidationError | None:
    if trade.side not in VALID_SIDES:
        return ValidationError(
            trade.trade_id,
            f"Invalid side '{trade.side}' — must be BUY or SELL",
        )

    if trade.symbol not in config.valid_symbols:
        return ValidationError(
            trade.trade_id,
            f"Unknown symbol '{trade.symbol}'",
        )

    if trade.quantity < config.min_quantity:
        return ValidationError(
            trade.trade_id,
            f"Quantity {trade.quantity} below minimum {config.min_quantity}",
        )

    if trade.quantity > config.max_quantity:
        return ValidationError(
            trade.trade_id,
            f"Quantity {trade.quantity} above maximum {config.max_quantity}",
        )

    if trade.price < config.min_price:
        return ValidationError(
            trade.trade_id,
            f"Price {trade.price} below minimum {config.min_price}",
        )

    if trade.price > config.max_price:
        return ValidationError(
            trade.trade_id,
            f"Price {trade.price} above maximum {config.max_price}",
        )

    return None


# ============================================================
# TRANSFORMER
# ============================================================

def transform_trade(trade: Trade) -> Trade:
    trade.notional = trade.quantity * trade.price
    return trade


# ============================================================
# AGGREGATOR
# ============================================================

def aggregate_trades(trades: list[Trade]) -> dict[str, SymbolStats]:
    stats: dict[str, SymbolStats] = {}

    for trade in trades:
        if trade.symbol not in stats:
            stats[trade.symbol] = SymbolStats(symbol=trade.symbol)

        s = stats[trade.symbol]
        s.trade_count += 1
        s.total_volume += trade.quantity
        s.total_notional += trade.notional
        s.min_price = min(s.min_price, trade.price)
        s.max_price = max(s.max_price, trade.price)

        if trade.side == "BUY":
            s.buy_count += 1
        else:
            s.sell_count += 1

    return stats


# ============================================================
# REPORTER
# ============================================================

def print_report(result: PipelineResult, stats: dict[str, SymbolStats]) -> None:
    width = 60
    print("=" * width)
    print("  TRADE PIPELINE REPORT")
    print("=" * width)

    print(f"\n  {'Total records parsed:':<30} {result.total_parsed}")
    print(f"  {'Valid trades:':<30} {len(result.valid_trades)}")
    print(f"  {'Rejected trades:':<30} {len(result.invalid_trades)}")

    if result.invalid_trades:
        print(f"\n{'─' * width}")
        print("  REJECTED TRADES")
        print(f"{'─' * width}")
        for err in result.invalid_trades:
            print(f"  [{err.trade_id}] {err.reason}")

    print(f"\n{'─' * width}")
    print("  SYMBOL STATISTICS")
    print(f"{'─' * width}")
    print(
        f"  {'Symbol':<8} {'Trades':>6} {'Volume':>8} "
        f"{'VWAP':>10} {'Min':>8} {'Max':>8} {'Buy/Sell':>10}"
    )
    print(f"  {'─'*8} {'─'*6} {'─'*8} {'─'*10} {'─'*8} {'─'*8} {'─'*10}")

    for _, s in sorted(stats.items()):
        print(
            f"  {s.symbol:<8} {s.trade_count:>6} {s.total_volume:>8} "
            f"${s.vwap:>9.2f} ${s.min_price:>7.2f} "
            f"${s.max_price:>7.2f} "
            f"{s.buy_count}B/{s.sell_count}S"
        )

    total_notional = sum(s.total_notional for s in stats.values())
    total_volume = sum(s.total_volume for s in stats.values())

    print(f"{'─' * width}")
    print(f"\n  {'Total notional traded:':<30} ${total_notional:,.2f}")
    print(f"  {'Total shares traded:':<30} {total_volume:,}")
    print(f"\n{'=' * width}\n")


# ============================================================
# ORCHESTRATOR
# match on parser results
# ============================================================

def run_pipeline(
    filepath: str,
    config: PipelineConfig,
    symbol_filter: str | None = None,
) -> None:
    valid_trades: list[Trade] = []
    invalid_trades: list[ValidationError] = []
    total_parsed = 0

    start = time.perf_counter()

    for record in parse_trades(filepath):
        total_parsed += 1

        match record:
            case Ok(value=trade):
                error = validate_trade(trade, config)
                if error is not None:
                    invalid_trades.append(error)
                    continue

                transformed = transform_trade(trade)

                if symbol_filter and transformed.symbol != symbol_filter:
                    continue

                valid_trades.append(transformed)

            case Err(error=err):
                invalid_trades.append(err)

    elapsed = time.perf_counter() - start

    stats = aggregate_trades(valid_trades)

    result = PipelineResult(
        valid_trades=valid_trades,
        invalid_trades=invalid_trades,
        total_parsed=total_parsed,
    )

    print_report(result, stats)
    print(f"Pipeline elapsed time: {elapsed:.6f}s")


# ============================================================
# ENTRY POINT
# ============================================================

def main() -> int:
    csv_path = "trades.csv"
    symbol_filter: str | None = None

    if len(sys.argv) >= 2:
        csv_path = sys.argv[1]

    if len(sys.argv) == 4 and sys.argv[2] == "--symbol":
        symbol_filter = sys.argv[3].upper()

    config = PipelineConfig(
        valid_symbols=frozenset({"AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"}),
        min_quantity=1,
        max_quantity=1_000_000,
        min_price=0.01,
        max_price=100_000.0,
    )

    try:
        run_pipeline(csv_path, config, symbol_filter)
        return 0

    except TradePipelineException as e:
        print(f"Pipeline error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())