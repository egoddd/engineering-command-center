from dataclasses import dataclass

@dataclass
class SimpleTrade:
    side: str
    quantity: int


def classify_trade(trade: SimpleTrade) -> str:
    match trade:
        case SimpleTrade(side="BUY", quantity=q) if q > 500:
            return "large-buy"
        case SimpleTrade(side="SELL", quantity=q) if q > 500:
            return "large-sell"
        case SimpleTrade(side="BUY", quantity=q) if q <= 500:
            return "small-buy"
        case SimpleTrade(side="SELL", quantity=q) if q <= 500:
            return "small-sell"
        case _:
            return "invalid"


def test_classify_trade() -> None:
    trades = [
        SimpleTrade("BUY", 100),    # small-buy
        SimpleTrade("BUY", 900),    # large-buy
        SimpleTrade("SELL", 50),    # small-sell
        SimpleTrade("SELL", 700),   # large-sell
        SimpleTrade("HOLD", 100),   # invalid
        SimpleTrade("BUY", -1),     # small-buy by raw rule; still matches <= 500
    ]

    for t in trades:
        print(t, "->", classify_trade(t))


test_classify_trade()