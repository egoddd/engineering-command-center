import threading
import multiprocessing
import time

N = 50_000_000

def countdown(n: int) -> None:
    while n > 0:
        n -= 1

# single-thread
start = time.perf_counter()
countdown(N)
countdown(N)
end = time.perf_counter()
print(f"Single-threaded: {end - start:.4f}s")

# threading
start = time.perf_counter()
t1 = threading.Thread(target=countdown, args=(N,))
t2 = threading.Thread(target=countdown, args=(N,))
t1.start()
t2.start()
t1.join()
t2.join()
end = time.perf_counter()
print(f"Two threads: {end - start:.4f}s")

# multiprocessing
start = time.perf_counter()
p1 = multiprocessing.Process(target=countdown, args=(N,))
p2 = multiprocessing.Process(target=countdown, args=(N,))
p1.start()
p2.start()
p1.join()
p2.join()
end = time.perf_counter()
print(f"Two processes: {end - start:.4f}s")