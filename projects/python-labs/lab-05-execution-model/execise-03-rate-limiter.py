import time


def make_rate_limiter(max_calls, period_seconds):
    calls = []

    def allow():
        nonlocal calls
        now = time.time()

        calls = [t for t in calls if now - t < period_seconds]

        if len(calls) < max_calls:
            calls.append(now)
            return True

        return False

    return allow


limiter = make_rate_limiter(3, 5)

for i in range(6):
    print("Call", i, limiter())
    time.sleep(1)