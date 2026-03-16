import inspect


def stack_depth():
    frame = inspect.currentframe()
    depth = 0

    while frame:
        depth += 1
        frame = frame.f_back

    return depth


def recursive(n):
    if n == 0:
        print("Stack depth:", stack_depth())
        return

    recursive(n - 1)


recursive(10)