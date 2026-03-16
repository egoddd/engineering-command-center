# trade_pipeline.py
# Day 6 Project — Trade Data Pipeline
# Applies: data types, control flow, functions,
#          closures, generators, memory awareness

from __future__ import annotations
import csv
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Generator

# ─────────────────────────────────────────────────────
# LAYER 1 — DATA MODEL
# A dataclass is a clean way to define a typed record.
# Fields are strongly typed — connects to Day 4.
# ─────────────────────────────────────────────────────

@dataclass
class Trade:
    trade_id:  str
    symbol:    str
    side:      str
    quantity:  int
    price:     float
    timestamp: datetime
    notional:  float = field(default=0.0, init=False)  # derived field

@dataclass
class ValidationError:
    trade_id: str
    reason:   str

@dataclass
class PipelineResult:
    valid_trades:    list[Trade]
    invalid_trades:  list[ValidationError]
    total_parsed:    int

# ─────────────────────────────────────────────────────
# LAYER 2 — PARSER
# Reads raw CSV rows and converts to typed Trade objects.
# Separates I/O from logic — a core design principle.
# ─────────────────────────────────────────────────────

def parse_trades(filepath: str) -> Generator[Trade | ValidationError, None, None]:
    """
    Generator-based parser — yields one record at a time.
    Memory efficient: does not load entire file into memory.
    Connects to Day 5: generators keep their frame alive between yields.
    """
    path = Path(filepath)
    if not path.exists():
        print(f"Error: file not found: {filepath}", file=sys.stderr)
        return

    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                trade = Trade(
                    trade_id  = row['trade_id'].strip(),
                    symbol    = row['symbol'].strip(),
                    side      = row['side'].strip().upper(),
                    quantity  = int(row['quantity']),
                    price     = float(row['price']),
                    timestamp = datetime.strptime(
                                    row['timestamp'].strip(),
                                    '%Y-%m-%d %H:%M:%S'
                                ),
                )
                yield trade
            except (ValueError, KeyError) as e:
                yield ValidationError(
                    trade_id=row.get('trade_id', 'UNKNOWN'),
                    reason=f"Parse error: {e}"
                )

# ─────────────────────────────────────────────────────
# LAYER 3 — VALIDATOR
# Business rules enforced as pure functions.
# Returns None if valid, ValidationError if not.
# ─────────────────────────────────────────────────────

VALID_SIDES   = {'BUY', 'SELL'}
VALID_SYMBOLS = {'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'}
MIN_QUANTITY  = 1
MAX_QUANTITY  = 1_000_000
MIN_PRICE     = 0.01
MAX_PRICE     = 100_000.0

def validate_trade(trade: Trade) -> ValidationError | None:
    """
    Validate a single trade against business rules.
    Pure function — no side effects, no state.
    """
    if trade.side not in VALID_SIDES:
        return ValidationError(trade.trade_id,
               f"Invalid side '{trade.side}' — must be BUY or SELL")

    if trade.symbol not in VALID_SYMBOLS:
        return ValidationError(trade.trade_id,
               f"Unknown symbol '{trade.symbol}'")

    if not (MIN_QUANTITY <= trade.quantity <= MAX_QUANTITY):
        return ValidationError(trade.trade_id,
               f"Quantity {trade.quantity} out of range "
               f"[{MIN_QUANTITY}, {MAX_QUANTITY}]")

    if not (MIN_PRICE <= trade.price <= MAX_PRICE):
        return ValidationError(trade.trade_id,
               f"Price {trade.price} out of range "
               f"[{MIN_PRICE}, {MAX_PRICE}]")

    return None  # valid

# ─────────────────────────────────────────────────────
# LAYER 4 — TRANSFORMER
# Derives calculated fields from validated trades.
# ─────────────────────────────────────────────────────

def transform_trade(trade: Trade) -> Trade:
    """
    Calculate derived fields.
    Notional value = quantity × price — the total dollar value of the trade.
    Note: using float here for in-memory analytics.
    Production financial accounting would use Decimal.
    """
    trade.notional = trade.quantity * trade.price
    return trade

# ─────────────────────────────────────────────────────
# LAYER 5 — AGGREGATOR
# Computes summary statistics across all valid trades.
# ─────────────────────────────────────────────────────

@dataclass
class SymbolStats:
    symbol:         str
    trade_count:    int   = 0
    total_volume:   int   = 0    # total shares traded
    total_notional: float = 0.0  # total dollar value
    buy_count:      int   = 0
    sell_count:     int   = 0
    min_price:      float = float('inf')
    max_price:      float = float('-inf')

    @property
    def avg_price(self) -> float:
        return self.total_notional / self.total_volume if self.total_volume else 0.0

    @property
    def vwap(self) -> float:
        """Volume-Weighted Average Price — standard metric in trading systems."""
        return self.total_notional / self.total_volume if self.total_volume else 0.0

def aggregate_trades(trades: list[Trade]) -> dict[str, SymbolStats]:
    """
    Build per-symbol statistics from a list of valid trades.
    Returns a dict mapping symbol → SymbolStats.
    """
    stats: dict[str, SymbolStats] = {}

    for trade in trades:
        if trade.symbol not in stats:
            stats[trade.symbol] = SymbolStats(symbol=trade.symbol)

        s = stats[trade.symbol]
        s.trade_count    += 1
        s.total_volume   += trade.quantity
        s.total_notional += trade.notional
        s.min_price       = min(s.min_price, trade.price)
        s.max_price       = max(s.max_price, trade.price)

        if trade.side == 'BUY':
            s.buy_count += 1
        else:
            s.sell_count += 1

    return stats

# ─────────────────────────────────────────────────────
# LAYER 6 — REPORTER
# Formats and prints results to terminal.
# Separated from logic — output format can change
# without touching business rules.
# ─────────────────────────────────────────────────────

def print_report(result: PipelineResult,
                 stats: dict[str, SymbolStats]) -> None:

    width = 60
    print("=" * width)
    print("  TRADE PIPELINE REPORT")
    print("=" * width)

    # Pipeline summary
    print(f"\n  {'Total records parsed:':<30} {result.total_parsed}")
    print(f"  {'Valid trades:':<30} {len(result.valid_trades)}")
    print(f"  {'Rejected trades:':<30} {len(result.invalid_trades)}")

    # Validation errors
    if result.invalid_trades:
        print(f"\n{'─' * width}")
        print("  REJECTED TRADES")
        print(f"{'─' * width}")
        for err in result.invalid_trades:
            print(f"  [{err.trade_id}] {err.reason}")

    # Per-symbol statistics
    print(f"\n{'─' * width}")
    print("  SYMBOL STATISTICS")
    print(f"{'─' * width}")
    print(f"  {'Symbol':<8} {'Trades':>6} {'Volume':>8} "
          f"{'VWAP':>10} {'Min':>8} {'Max':>8} {'Buy/Sell':>10}")
    print(f"  {'─'*8} {'─'*6} {'─'*8} {'─'*10} {'─'*8} {'─'*8} {'─'*10}")

    for symbol, s in sorted(stats.items()):
        print(f"  {s.symbol:<8} {s.trade_count:>6} {s.total_volume:>8} "
              f"${s.vwap:>9.2f} ${s.min_price:>7.2f} "
              f"${s.max_price:>7.2f} "
              f"{s.buy_count}B/{s.sell_count}S")

    # Overall totals
    total_notional = sum(s.total_notional for s in stats.values())
    total_volume   = sum(s.total_volume   for s in stats.values())
    print(f"{'─' * width}")
    print(f"\n  {'Total notional traded:':<30} ${total_notional:,.2f}")
    print(f"  {'Total shares traded:':<30} {total_volume:,}")
    print(f"\n{'=' * width}\n")

# ─────────────────────────────────────────────────────
# LAYER 7 — PIPELINE ORCHESTRATOR
# Connects all stages. This is the main entry point.
# ─────────────────────────────────────────────────────

def run_pipeline(filepath: str, symbol_filter: str | None = None) -> None:
    """
    Orchestrate all pipeline stages:
    parse → validate → transform → aggregate → report
    """
    valid_trades:   list[Trade]           = []
    invalid_trades: list[ValidationError] = []
    total_parsed:   int                   = 0

    # Stage 1 + 2 + 3: parse, validate, transform
    # The generator yields one record at a time — O(1) memory per record
    for record in parse_trades(filepath):
        total_parsed += 1

        # If parsing itself failed, record is already a ValidationError
        if isinstance(record, ValidationError):
            invalid_trades.append(record)
            continue

        # Validate business rules
        error = validate_trade(record)
        if error:
            invalid_trades.append(error)
            continue

        # Transform — calculate derived fields
        trade = transform_trade(record)

        if symbol_filter and trade.symbol != symbol_filter:
            continue

        valid_trades.append(trade)

    # Stage 4: aggregate
    stats = aggregate_trades(valid_trades)

    # Stage 5: report
    result = PipelineResult(
        valid_trades   = valid_trades,
        invalid_trades = invalid_trades,
        total_parsed   = total_parsed,
    )
    print_report(result, stats)

# ─────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────

if __name__ == '__main__':
    csv_path = 'trades.csv'
    symbol_filter = None

    if len(sys.argv) >= 2:
        csv_path = sys.argv[1]

    if len(sys.argv) == 4 and sys.argv[2] == "--symbol":
        symbol_filter = sys.argv[3].upper()

    run_pipeline(csv_path, symbol_filter)