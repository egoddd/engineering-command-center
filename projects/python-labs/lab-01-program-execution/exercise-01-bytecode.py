import dis


def factorial(n: int) -> int:
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


print("Factorial(5):", factorial(5))
print("\nDisassembly:\n")
dis.dis(factorial)