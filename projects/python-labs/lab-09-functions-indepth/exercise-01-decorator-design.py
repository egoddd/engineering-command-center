import inspect
from functools import wraps


def validate_inputs(func):
    signature = inspect.signature(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = signature.bind(*args, **kwargs)
        bound.apply_defaults()

        for name, value in bound.arguments.items():
            if value is None:
                raise ValueError(f"Parameter '{name}' was None")

        return func(*args, **kwargs)

    return wrapper


@validate_inputs
def add(a, b):
    return a + b


@validate_inputs
def place_order(symbol, quantity, side="BUY"):
    return f"{side} {quantity} of {symbol}"


print(add(2, 3))
print(place_order("AAPL", 100))
# print(add(None, 3))                  # raises ValueError
# print(place_order("AAPL", None))     # raises ValueError