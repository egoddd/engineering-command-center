from dataclasses import dataclass
from datetime import datetime


class TradePipelineException(Exception):
    """Base class for all trade pipeline exceptions."""
    pass


class TradeParseException(TradePipelineException):
    def __init__(self, trade_id: str, raw_row: dict, field_name: str, reason: str):
        super().__init__(f"Failed to parse trade {trade_id}: field={field_name}, reason={reason}")
        self.trade_id = trade_id
        self.raw_row = raw_row
        self.field_name = field_name
        self.reason = reason


class TradeValidationException(TradePipelineException):
    def __init__(self, trade_id: str, symbol: str, rule: str, value):
        super().__init__(f"Validation failed for trade {trade_id}: {rule} (value={value})")
        self.trade_id = trade_id
        self.symbol = symbol
        self.rule = rule
        self.value = value


class TradeStorageException(TradePipelineException):
    def __init__(self, trade_id: str, destination: str, operation: str, reason: str):
        super().__init__(f"Storage failure for trade {trade_id}: {operation} to {destination} failed: {reason}")
        self.trade_id = trade_id
        self.destination = destination
        self.operation = operation
        self.reason = reason


def test_trade_exceptions() -> None:
    try:
        raise TradeParseException(
            trade_id="T100",
            raw_row={"trade_id": "T100", "price": "abc"},
            field_name="price",
            reason="could not convert string to float"
        )
    except TradeParseException as e:
        print("Caught TradeParseException")
        print(e.trade_id, e.field_name, e.reason)

    try:
        raise TradeValidationException(
            trade_id="T101",
            symbol="TSLA",
            rule="max_quantity",
            value=5_000_000
        )
    except TradeValidationException as e:
        print("Caught TradeValidationException")
        print(e.trade_id, e.symbol, e.rule, e.value)

    try:
        raise TradeStorageException(
            trade_id="T102",
            destination="warehouse/trades.parquet",
            operation="write",
            reason="disk full"
        )
    except TradeStorageException as e:
        print("Caught TradeStorageException")
        print(e.trade_id, e.destination, e.operation, e.reason)


test_trade_exceptions()