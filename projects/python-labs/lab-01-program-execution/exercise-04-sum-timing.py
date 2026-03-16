import time


def sum_to_n(n: int) -> int:
    total = 0
    for i in range(1, n + 1):
        total += i
    return total


start = time.perf_counter()
result = sum_to_n(10_000_000)
end = time.perf_counter()

print(f"Result: {result}")
print(f"Elapsed time: {end - start:.6f} seconds")