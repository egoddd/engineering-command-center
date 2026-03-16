def safe_equals(a: float, b: float, epsilon: float = 1e-9) -> bool:
    return abs(a - b) < epsilon

examples = [
    (0.1 + 0.2, 0.3),
    (0.1 + 0.1 + 0.1, 0.3),
    (1.1 + 2.2, 3.3),
    (0.15 + 0.15, 0.3),
    (0.7 - 0.6, 0.1),
]

for a, b in examples:
    print(f"a = {a!r}, b = {b!r}")
    print(f"a == b: {a == b}")
    print(f"safe_equals(a, b): {safe_equals(a, b)}")
    print()

# Epsilon comparison is correct because many decimal fractions cannot be represented exactly in binary floating point.