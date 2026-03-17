import random
from collections import deque


def price_stream():
    price = 100.0

    while True:
        price += random.uniform(-0.5, 0.5)
        yield price


def filter_prices(stream, threshold):
    for price in stream:
        if price > threshold:
            yield price


def moving_average(stream, window):
    history = deque(maxlen=window)

    for price in stream:
        history.append(price)

        if len(history) == window:
            yield sum(history) / window


stream = price_stream()
filtered = filter_prices(stream, 99.5)
avg = moving_average(filtered, 5)

for _ in range(20):
    print(next(avg))