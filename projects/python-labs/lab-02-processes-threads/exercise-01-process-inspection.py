import os
import time

print(f"PID: {os.getpid()}")
print(f"Parent PID: {os.getppid()}")
print(f"CPU count: {os.cpu_count()}")

print("Sleeping for 20 seconds...")
time.sleep(20)