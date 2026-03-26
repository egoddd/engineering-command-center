# trade_pipeline.py — Refactored with Frozen Config

from __future__ import annotations
import csv
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Generator

# ─────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────

@dataclass(frozen=True)
class PipelineConfig:
    valid_symbols: set[str]
    min_quantity: int
    max_quantity: int
    min_price: float
    max_price: float

# ─────────────────────────────────────────────────────
# DATA MODELS
# ─────────────────────────────────────────────────────

@dataclass
class Trade:
    trade_id:  str
    symbol:    str
    side:      str
    quantity:  int
    price:     float
    timestamp: datetime
    notional:  float = field(default=0.0, init=False)

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
# CONSTANTS (true constants stay global)
# ─────────────────────────────────────────────────────

VALID_SIDES = {'BUY', 'SELL'}

# ─────────────────────────────────────────────────────
# PARSER
# ─────────────────────────────────────────────────────

def parse_trades(filepath: str) -> Generator[Trade | ValidationError, None, None]:
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
# VALIDATOR (now uses config)
# ─────────────────────────────────────────────────────

def validate_trade(trade: Trade, config: PipelineConfig) -> ValidationError | None:
    if trade.side not in VALID_SIDES:
        return ValidationError(trade.trade_id,
               f"Invalid side '{trade.side}' — must be BUY or SELL")

    if trade.symbol not in config.valid_symbols:
        return ValidationError(trade.trade_id,
               f"Unknown symbol '{trade.symbol}'")

    if not (config.min_quantity <= trade.quantity <= config.max_quantity):
        return ValidationError(trade.trade_id,
               f"Quantity {trade.quantity} out of range "
               f"[{config.min_quantity}, {config.max_quantity}]")

    if not (config.min_price <= trade.price <= config.max_price):
        return ValidationError(trade.trade_id,
               f"Price {trade.price} out of range "
               f"[{config.min_price}, {config.max_price}]")

    return None

# ─────────────────────────────────────────────────────
# TRANSFORMER
# ─────────────────────────────────────────────────────

def transform_trade(trade: Trade) -> Trade:
    trade.notional = trade.quantity * trade.price
    return trade

# ─────────────────────────────────────────────────────
# AGGREGATOR
# ─────────────────────────────────────────────────────

@dataclass
class SymbolStats:
    symbol:         str
    trade_count:    int   = 0
    total_volume:   int   = 0
    total_notional: float = 0.0
    buy_count:      int   = 0
    sell_count:     int   = 0
    min_price:      float = float('inf')
    max_price:      float = float('-inf')

    @property
    def vwap(self) -> float:
        return self.total_notional / self.total_volume if self.total_volume else 0.0

def aggregate_trades(trades: list[Trade]) -> dict[str, SymbolStats]:
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
# REPORTER
# ─────────────────────────────────────────────────────

def print_report(result: PipelineResult,
                 stats: dict[str, SymbolStats]) -> None:

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

    for symbol, s in sorted(stats.items()):
        print(f"{symbol}: trades={s.trade_count}, volume={s.total_volume}, "
              f"vwap={s.vwap:.2f}")

# ─────────────────────────────────────────────────────
# PIPELINE
# ─────────────────────────────────────────────────────

def run_pipeline(filepath: str,
                 config: PipelineConfig,
                 symbol_filter: str | None = None) -> None:

    valid_trades:   list[Trade]           = []
    invalid_trades: list[ValidationError] = []
    total_parsed:   int                   = 0

    for record in parse_trades(filepath):
        total_parsed += 1

        if isinstance(record, ValidationError):
            invalid_trades.append(record)
            continue

        error = validate_trade(record, config)
        if error:
            invalid_trades.append(error)
            continue

        trade = transform_trade(record)

        if symbol_filter and trade.symbol != symbol_filter:
            continue

        valid_trades.append(trade)

    stats = aggregate_trades(valid_trades)

    result = PipelineResult(
        valid_trades=valid_trades,
        invalid_trades=invalid_trades,
        total_parsed=total_parsed,
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

    config = PipelineConfig(
        valid_symbols={'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'},
        min_quantity=1,
        max_quantity=1_000_000,
        min_price=0.01,
        max_price=100_000.0
    )

    run_pipeline(csv_path, config, symbol_filter)