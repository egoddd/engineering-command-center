import time
from dataclasses import dataclass

N = 100_000


class InvalidRecordError(Exception):
    pass


@dataclass(frozen=True)
class Ok:
    value: int


@dataclass(frozen=True)
class Err:
    reason: str


def benchmark_exceptions(n: int, invalid_rate: float) -> float:
    start = time.perf_counter()

    for i in range(n):
        try:
            if i / n < invalid_rate:
                raise InvalidRecordError("invalid")
            _ = i * 2
        except InvalidRecordError:
            pass

    return time.perf_counter() - start


def benchmark_results(n: int, invalid_rate: float) -> float:
    start = time.perf_counter()

    for i in range(n):
        if i / n < invalid_rate:
            result = Err("invalid")
        else:
            result = Ok(i * 2)

        match result:
            case Ok(_):
                pass
            case Err(_):
                pass

    return time.perf_counter() - start


def run_case(n: int, invalid_rate: float) -> None:
    exc_time = benchmark_exceptions(n, invalid_rate)
    res_time = benchmark_results(n, invalid_rate)

    print(f"invalid_rate = {invalid_rate:.3f}")
    print(f"Exception version: {exc_time:.6f}s")
    print(f"Result version:    {res_time:.6f}s")
    print(f"Ratio (exc/result): {exc_time / res_time:.2f}x")
    print()


def main() -> None:
    # Heavy failure case
    run_case(N, 0.9)

    # Real-world style rare failure case
    run_case(N, 0.001)


if __name__ == "__main__":
    main()