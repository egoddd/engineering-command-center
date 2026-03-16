import sys
import gc

class Node:
    def __init__(self, name: str):
        self.name = name
        self.other = None

obj = []
print("Initial refcount:", sys.getrefcount(obj))

a = obj
print("After a = obj:", sys.getrefcount(obj))

b = obj
print("After b = obj:", sys.getrefcount(obj))

del a
print("After del a:", sys.getrefcount(obj))

del b
print("After del b:", sys.getrefcount(obj))

n1 = Node("n1")
n2 = Node("n2")
n1.other = n2
n2.other = n1

del n1
del n2

collected = gc.collect()
print("Cyclic GC collected:", collected)