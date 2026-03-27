from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class OrderBase(ABC):
    symbol: str
    quantity: int

    @abstractmethod
    def would_execute(self, market_price: float, now: datetime | None = None) -> bool:
        pass

    @abstractmethod
    def execution_price(self, market_price: float) -> float:
        pass


@dataclass
class MarketOrder(OrderBase):
    def would_execute(self, market_price: float, now: datetime | None = None) -> bool:
        return True

    def execution_price(self, market_price: float) -> float:
        return market_price


@dataclass
class LimitOrder(OrderBase):
    limit_price: float
    side: str

    def would_execute(self, market_price: float, now: datetime | None = None) -> bool:
        if self.side == "BUY":
            return market_price <= self.limit_price
        return market_price >= self.limit_price

    def execution_price(self, market_price: float) -> float:
        return min(market_price, self.limit_price) if self.side == "BUY" else max(market_price, self.limit_price)


@dataclass
class TWAPOrder(OrderBase):
    start_time: datetime
    end_time: datetime
    num_slices: int

    def would_execute(self, market_price: float, now: datetime | None = None) -> bool:
        if now is None:
            now = datetime.now()
        return self.start_time <= now <= self.end_time and self.num_slices > 0

    def execution_price(self, market_price: float) -> float:
        return market_price


def count_executable_orders(orders: list[OrderBase], market_price: float, now: datetime | None = None) -> int:
    return sum(1 for order in orders if order.would_execute(market_price, now))


# Demo
now = datetime.now()
orders: list[OrderBase] = [
    MarketOrder("AAPL", 100),
    LimitOrder("MSFT", 50, 410.0, "BUY"),
    TWAPOrder("GOOGL", 200, now, now.replace(hour=23, minute=59), 10),
]
print(count_executable_orders(orders, 405.0, now))