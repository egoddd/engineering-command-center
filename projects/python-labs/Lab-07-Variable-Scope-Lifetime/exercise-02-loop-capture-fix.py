# Exercise 2: Loop Capture Fix (Python)

print("Broken loop capture:")
funcs = []

for i in range(3):
    funcs.append(lambda: i)   # captures the variable, not its value at each iteration

for f in funcs:
    print(f())  # wrong: 2, 2, 2


print("\nFixed loop capture with default arguments:")
fixed_funcs = []

for i in range(3):
    fixed_funcs.append(lambda i=i: i)   # default argument stores current value

for f in fixed_funcs:
    print(f())  # correct: 0, 1, 2