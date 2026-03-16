# Lab 1 — Program Execution

## Core Question
What happens when I run a program?

## What I observed
- Running a program creates a process.
- A process contains at least one thread.
- Code begins on the main thread.
- A program can create additional threads/tasks.
- Variables and objects use memory.
- Python uses an interpreter/runtime.
- C# uses the .NET runtime.

## My current mental model
- Process = factory building
- Thread = worker inside the factory
- Stack = working desk for current task
- Heap = warehouse for objects
- CPU = workers executing instructions
- OS = city government coordinating resources

## What still feels unclear
- exact difference between stack and heap
- how threads are scheduled
- what the runtime really does

## Questions for next lesson
- What exactly is the stack?
- What exactly is the heap?
- How does the CPU execute instructions?

## Exercise Progress

### Exercise 1 — Bytecode Reading
- What I observed:
- What surprised me:
- What bytecode taught me about Python execution:

### Exercise 2 — Stack Depth Measurement
- Maximum recursion depth reached:
- Current recursion limit:
- Why Python imposes a recursion limit:

### Exercise 3 — Stack vs Heap in C#
- What was stack-allocated:
- What was heap-allocated:
- What I learned about value types vs reference types:

### Exercise 4 — Timing Python vs C#
- Python time:
- C# time:
- Why the times differ:

### Exercise 5 — Memory Size Investigation
- int:
- float:
- empty list:
- list with 10 ints:
- empty dict:
- string length 5:
- Why Python objects are larger than raw C values:

### Exercise 6 — Design Reasoning
- Language choice:
- Allocation preference:
- GC risk:
- Mitigation ideas: