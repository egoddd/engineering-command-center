from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Order:
    symbol: str
    quantity: int
    price: float
    position_after: int


class RiskCheck(ABC):
    @abstractmethod
    def check(self, order: Order) -> bool:
        pass

    def check_with_logging(self, order: Order) -> bool:
        result = self.check(order)
        print(f"{self.__class__.__name__}: {result} for {order.symbol}")
        return result


class PositionLimitCheck(RiskCheck):
    def __init__(self, max_position: int):
        self.max_position = max_position

    def check(self, order: Order) -> bool:
        return abs(order.position_after) <= self.max_position


class NotionalLimitCheck(RiskCheck):
    def __init__(self, max_notional: float):
        self.max_notional = max_notional

    def check(self, order: Order) -> bool:
        return abs(order.quantity * order.price) <= self.max_notional


class SymbolAllowlistCheck(RiskCheck):
    def __init__(self, allowed_symbols: set[str]):
        self.allowed_symbols = allowed_symbols

    def check(self, order: Order) -> bool:
        return order.symbol in self.allowed_symbols


class RiskEngine:
    def __init__(self, checks: list[RiskCheck]):
        self.checks = checks

    # ✅ FIX: return which check failed
    def run(self, order: Order) -> tuple[bool, str | None]:
        for check in self.checks:
            if not check.check_with_logging(order):
                return False, check.__class__.__name__

        return True, None


# Demo
engine = RiskEngine([
    PositionLimitCheck(1000),
    NotionalLimitCheck(100_000),
    SymbolAllowlistCheck({"AAPL", "MSFT", "GOOGL"}),
])

order = Order("AAPL", 100, 180.0, 500)
print(engine.run(order))