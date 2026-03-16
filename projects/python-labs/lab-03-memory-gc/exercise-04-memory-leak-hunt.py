import tracemalloc
import gc

class Node:
    def __init__(self):
        self.other = None

def leak():
    items = []
    for _ in range(10_000):
        a = Node()
        b = Node()
        a.other = b
        b.other = a
        items.append((a, b))
    return items

def fixed():
    items = []
    for _ in range(10_000):
        a = Node()
        b = Node()
        a.other = b
        b.other = None
        items.append((a, b))
    return items
pytho
tracemalloc.start()

leaked = leak()
current, peak = tracemalloc.get_traced_memory()
print(f"After leak() - Current: {current}, Peak: {peak}")

del leaked
gc.collect()

current, peak = tracemalloc.get_traced_memory()
print(f"After deleting leaked objects - Current: {current}, Peak: {peak}")

fixed_items = fixed()
current, peak = tracemalloc.get_traced_memory()
print(f"After fixed() - Current: {current}, Peak: {peak}")

del fixed_items
gc.collect()

current, peak = tracemalloc.get_traced_memory()
print(f"After deleting fixed objects - Current: {current}, Peak: {peak}")