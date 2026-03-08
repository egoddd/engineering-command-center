import os
import threading
import time

def worker() -> None:
    print(f"[Worker] Thread ID: {threading.get_ident()}")
    time.sleep(1)
    print("[Worker] Finished work.")

def main() -> None:
    print("=== Python Program Execution Demo ===")
    print(f"Process ID: {os.getpid()}")
    print(f"Main Thread ID: {threading.get_ident()}")

    value = 42
    numbers = [1, 2, 3, 4, 5]

    print(f"Value on execution path: {value}")
    print(f"List object in memory: {numbers}")

    thread = threading.Thread(target=worker)
    thread.start()
    thread.join()

    print("Program finished.")

if __name__ == "__main__":
    main()