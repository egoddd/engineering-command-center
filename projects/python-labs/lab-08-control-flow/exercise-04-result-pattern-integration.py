from __future__ import annotations
import csv
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Generator

# ----------------------------
# Result types
# ----------------------------

@dataclass(frozen=True)
class Ok:
    value: object

@dataclass(frozen=True)
class Err:
    error: "ValidationError"

Result = Ok | Err

# ----------------------------
# Existing models
# ----------------------------

@dataclass(frozen=True)
class PipelineConfig:
    valid_symbols: set[str]
    min_quantity: int
    max_quantity: int
    min_price: float
    max_price: float

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
    def vwap(self) -> float:
        return self.total_notional / self.total_volume if self.total_volume else 0.0

VALID_SIDES = {"BUY", "SELL"}

# ----------------------------
# Result-based parser
# ----------------------------

def parse_trades(filepath: str) -> Generator[Result, None, None]:
    path = Path(filepath)
    if not path.exists():
        print(f"Error: file not found: {filepath}", file=sys.stderr)
        return

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
                        "%Y-%m-%d %H:%M:%S"
                    ),
                )
                yield Ok(trade)
            except (ValueError, KeyError) as e:
                yield Err(
                    ValidationError(
                        trade_id=row.get("trade_id", "UNKNOWN"),
                        reason=f"Parse error: {e}"
                    )
                )

def validate_trade(trade: Trade, config: PipelineConfig) -> ValidationError | None:
    if trade.side not in VALID_SIDES:
        return ValidationError(trade.trade_id, f"Invalid side '{trade.side}' — must be BUY or SELL")

    if trade.symbol not in config.valid_symbols:
        return ValidationError(trade.trade_id, f"Unknown symbol '{trade.symbol}'")

    if not (config.min_quantity <= trade.quantity <= config.max_quantity):
        return ValidationError(
            trade.trade_id,
            f"Quantity {trade.quantity} out of range [{config.min_quantity}, {config.max_quantity}]"
        )

    if not (config.min_price <= trade.price <= config.max_price):
        return ValidationError(
            trade.trade_id,
            f"Price {trade.price} out of range [{config.min_price}, {config.max_price}]"
        )

    return None

def transform_trade(trade: Trade) -> Trade:
    trade.notional = trade.quantity * trade.price
    return trade

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

def print_report(result: PipelineResult, stats: dict[str, SymbolStats]) -> None:
    print(f"Total parsed: {result.total_parsed}")
    print(f"Valid trades: {len(result.valid_trades)}")
    print(f"Invalid trades: {len(result.invalid_trades)}")
    for symbol, s in sorted(stats.items()):
        print(symbol, s.trade_count, s.total_volume, round(s.vwap, 2))

def run_pipeline(filepath: str, config: PipelineConfig, symbol_filter: str | None = None) -> None:
    valid_trades: list[Trade] = []
    invalid_trades: list[ValidationError] = []
    total_parsed = 0

    for record in parse_trades(filepath):
        total_parsed += 1

        match record:
            case Ok(value=trade):
                error = validate_trade(trade, config)
                if error:
                    invalid_trades.append(error)
                    continue

                trade = transform_trade(trade)

                if symbol_filter and trade.symbol != symbol_filter:
                    continue

                valid_trades.append(trade)

            case Err(error=err):
                invalid_trades.append(err)

    stats = aggregate_trades(valid_trades)
    result = PipelineResult(valid_trades, invalid_trades, total_parsed)
    print_report(result, stats)