#Exercises

##Work through these in order. Do not skip.

#Exercise 1 — Bytecode Reading
Write a Python function that computes the factorial of a number using a loop (not recursion). Run dis.dis() on it. Read every bytecode instruction. Write a one-sentence explanation of what each instruction does.

#Exercise 2 — Stack Depth Measurement
Write a Python function that calls itself recursively and counts how deep it gets before hitting RecursionError. Print the maximum depth. Then look up sys.setrecursionlimit() — understand what it does and why Python imposes a limit.

#Exercise 3 — Stack vs Heap in C#
Write a C# program with:

A struct called Vector3 with float X, Y, Z fields
A class called Particle with a Vector3 Position and a float Mass
A method that creates 5 Particle objects and prints their data

Annotate each variable in comments: stack or heap? Why?
Exercise 4 — Timing Python vs C# Execution
Implement the same function in both languages: sum all integers from 1 to 10,000,000. Time both using the high-precision timers shown in the examples above. Record the results. Write 3 sentences explaining why the times differ based on what you learned today.
Exercise 5 — Memory Size Investigation
In Python, use sys.getsizeof() to measure the size of: an int, a float, an empty list, a list with 10 integers, an empty dict, and a str of length 5. Then answer: why does Python's int take 28 bytes when a C int only takes 4?
Exercise 6 — Design Question
You are designing a system that must process 1,000,000 financial transactions per second with a latency requirement of under 100 microseconds per transaction. Based only on what you learned today, answer:

Would you use Python or C# as the core execution engine? Why?
What memory region (stack or heap) should you prefer for the transaction data structure? Why?
What is the biggest threat from the garbage collector in this scenario, and how would you mitigate it?
