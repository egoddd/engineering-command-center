class Position:
    def __init__(self, symbol: str, quantity: int, average_price: float):
        if quantity is None:
            raise ValueError("quantity cannot be None")
        if average_price < 0:
            raise ValueError("average_price must be non-negative")

        self._symbol = symbol
        self._quantity = quantity
        self._average_price = average_price

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def quantity(self) -> int:
        return self._quantity

    @property
    def average_price(self) -> float:
        return self._average_price

    def add_trade(self, side: str, quantity: int, price: float) -> None:
        if side not in {"BUY", "SELL"}:
            raise ValueError("side must be BUY or SELL")
        if quantity <= 0:
            raise ValueError("trade quantity must be positive")
        if price < 0:
            raise ValueError("price must be non-negative")

        signed_qty = quantity if side == "BUY" else -quantity
        new_quantity = self._quantity + signed_qty

        if self._quantity == 0:
            self._quantity = new_quantity
            self._average_price = 0.0 if new_quantity == 0 else price
            return

        # ✅ FIX: explicit parentheses
        if ((self._quantity > 0 and signed_qty > 0) or
            (self._quantity < 0 and signed_qty < 0)):
            total_abs_qty = abs(self._quantity) + abs(signed_qty)
            weighted_cost = (abs(self._quantity) * self._average_price) + (abs(signed_qty) * price)
            self._quantity = new_quantity
            self._average_price = weighted_cost / total_abs_qty
            return

        if abs(signed_qty) < abs(self._quantity):
            self._quantity = new_quantity
            return

        if new_quantity == 0:
            self._quantity = 0
            self._average_price = 0.0
            return

        self._quantity = new_quantity
        self._average_price = price

    def market_value(self, current_price: float) -> float:
        if current_price < 0:
            raise ValueError("current_price must be non-negative")
        return self._quantity * current_price