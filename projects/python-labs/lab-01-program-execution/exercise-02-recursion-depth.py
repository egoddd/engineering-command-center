import sys

def measure_depth(depth: int = 0) -> int:
    try:
        return measure_depth(depth + 1)
    except RecursionError:
        return depth


max_depth = measure_depth()
print(f"Maximum depth before RecursionError: {max_depth}")
print(f"Current recursion limit: {sys.getrecursionlimit()}")
print(sys.setrecursionlimit)