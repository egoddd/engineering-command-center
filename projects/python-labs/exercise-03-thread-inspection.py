import os
import threading
import time

def worker(index: int) -> None:
    print(f"Worker {index} thread ID: {threading.current_thread().ident}")
    time.sleep(60)

print(f"PID: {os.getpid()}")

threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()