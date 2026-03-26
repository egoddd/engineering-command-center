# Week 1 — Computational Foundations
### Human LLM Engineering Training — Month 1

---

> *"The engineer who understands the machine beneath the language
> writes code that is not just correct — but inevitable."*

---

## Table of Contents

1. [Day 1 — How Computers Execute Code](#day-1)
2. [Day 2 — Processes, Threads, and the OS](#day-2)
3. [Day 3 — Memory Management and Garbage Collection](#day-3)
4. [Day 4 — Data Types and Memory Representation](#day-4)
5. [Day 5 — Control Flow, Functions, and the Call Stack](#day-5)
6. [Day 6 — Project: Trade Data Pipeline](#day-6)
7. [Week 1 Mental Model Map](#mental-model-map)
8. [Key Analogies Reference](#analogies)
9. [Python vs C# Comparison Table](#comparison)
10. [Vocabulary Reference](#vocabulary)

---

<a name="day-1"></a>
## Day 1 — How Computers Execute Code

### The Core Loop

Every program that has ever run on any computer reduces to one loop:

```
┌─────────────────────────────────────────────┐
│                                             │
│   FETCH → DECODE → EXECUTE → WRITEBACK      │
│      ↑                           │          │
│      └───────────────────────────┘          │
│                                             │
│   Repeats ~3,000,000,000 times per second   │
└─────────────────────────────────────────────┘
```

This is the **fetch-decode-execute cycle**. Everything — web servers, games, trading engines — is this loop running billions of times.

---

### The Factory Analogy

```
┌─────────────────────────────────────────────────────────┐
│                    THE FACTORY                          │
│                                                         │
│  ┌──────────┐    ┌──────────────┐    ┌───────────────┐  │
│  │  Worker  │    │  Workbench   │    │   Warehouse   │  │
│  │  (CPU)   │◄──►│  (Registers) │    │    (RAM)      │  │
│  └──────────┘    └──────────────┘    └───────────────┘  │
│       ▲               ▲                    ▲            │
│  Does the        Holds what           Stores all        │
│  actual work     is being             program data      │
│                  worked on NOW                          │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Instruction Cards (Machine Code)                │   │
│  │  ADD  MOV  CMP  JMP  CALL  RET ...               │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

### Python vs C# Execution Path

```
PYTHON                              C#
──────────────────────────────────────────────────────────
Your .py file                       Your .cs file
     │                                   │
     ▼                                   ▼
CPython reads source             Roslyn compiler
     │                                   │
     ▼                                   ▼
Bytecode (.pyc)              IL (Intermediate Language)
     │                           stored in .dll / .exe
     ▼                                   │
Python Virtual Machine                   ▼
interprets bytecode           CLR JIT compiles to
     │                        native machine code
     ▼                        on first method call
Machine Code                             │
(via C extensions)                       ▼
                                  Native Machine Code
                                  runs directly on CPU

RESULT: Python is ~10-100x slower for CPU-bound loops
        C# runs at near-native speed after JIT warmup
```

---

### The Memory Hierarchy

```
Speed ◄────────────────────────────────────► Capacity

┌─────────────┐  < 1ns      Registers        ~KB
├─────────────┤  1-4ns      L1 Cache         ~64 KB
├─────────────┤  4-12ns     L2 Cache         ~256 KB
├─────────────┤  12-50ns    L3 Cache         ~32 MB
├─────────────┤  50-100ns   RAM              ~GBs
├─────────────┤  50-150μs   SSD              ~TBs
└─────────────┘  5-10ms     HDD              ~TBs

Analogy:
  Registers  = what is in your hand right now
  L1 Cache   = your desk
  L2 Cache   = filing cabinet behind you
  RAM        = supply room down the hall
  SSD        = warehouse across the street
  HDD        = warehouse in another city
```

---

### Stack vs Heap

```
PROCESS MEMORY LAYOUT
─────────────────────
HIGH ADDRESS
┌─────────────────┐
│     STACK       │  • Function calls, local variables
│        ↓        │  • Grows downward
│                 │  • LIFO — last in, first out
│   (free space)  │  • Fixed size (~1-8 MB per thread)
│                 │  • Allocation = pointer move = FREE
│        ↑        │
│      HEAP       │  • Dynamic allocations (objects)
│                 │  • Grows upward
├─────────────────┤  • GC managed
│      BSS        │  • Large but slower
├─────────────────┤
│      Data       │
├─────────────────┤
│      Text       │  Your compiled code
└─────────────────┘
LOW ADDRESS

Stack analogy: A notepad you write on and tear off during a meeting
Heap analogy:  A rented storage unit — things stay until removed
```

---

### Key Takeaways — Day 1

- The CPU executes one instruction at a time, billions of times per second
- Python translates code at runtime (slow). C# JIT-compiles to native code (fast)
- Registers are the fastest storage. RAM is 100x slower. SSD is 100,000x slower
- Stack allocation is free. Heap allocation has real cost
- Cache-friendly memory access patterns can make the same code 10x faster

---

<a name="day-2"></a>
## Day 2 — Processes, Threads, and the Operating System

### The Restaurant Analogy

```
┌─────────────────────────────────────────────────────────┐
│                    THE RESTAURANT                       │
│                                                         │
│  Head Chef (OS)        Kitchen (CPU)                    │
│  ┌──────────┐          ┌────────────────────────────┐   │
│  │Schedules │          │ Cook 1  Cook 2  Cook 3      │   │
│  │assigns   │─────────►│(Thread)(Thread)(Thread)    │   │
│  │manages   │          └────────────────────────────┘   │
│  └──────────┘                                           │
│                                                         │
│  Orders (Processes)     Shared kitchen tools (Heap)     │
│  ┌───────┐ ┌───────┐   ┌──────────────────────────┐    │
│  │Table 1│ │Table 2│   │ Fridge, counters,         │    │
│  │Process│ │Process│   │ equipment — shared by     │    │
│  └───────┘ └───────┘   │ all cooks in same order   │    │
│                         └──────────────────────────┘    │
│  Each table = isolated process                          │
│  Each cook  = thread within a process                   │
└─────────────────────────────────────────────────────────┘
```

---

### Process vs Thread

```
┌─────────────────────────────────────────────────────────┐
│                      PROCESS                            │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │              SHARED MEMORY (HEAP)                │   │
│  │  globals, objects, open files, code segment      │   │
│  └──────────────────────────────────────────────────┘   │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ Thread 1 │  │ Thread 2 │  │ Thread 3 │              │
│  │          │  │          │  │          │              │
│  │ own stack│  │ own stack│  │ own stack│              │
│  │ own regs │  │ own regs │  │ own regs │              │
│  │ own PC   │  │ own PC   │  │ own PC   │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘

Process isolation: crash in one process ≠ crash in others
Thread sharing:    bug in one thread CAN crash entire process
```

---

### The GIL — Python's Critical Limitation

```
PYTHON WITH 8 THREADS ON 8 CORES
──────────────────────────────────────────────────────────
Core 1: ████ Thread A executes  ◄── only ONE thread runs
Core 2: ░░░░ idle                   Python bytecode
Core 3: ░░░░ idle                   at any moment
Core 4: ░░░░ idle
...
Core 8: ░░░░ idle

WHY? The Global Interpreter Lock (GIL) protects CPython's
     reference counting from thread-unsafe corruption.

CONSEQUENCE:
  CPU-bound Python threads = no parallelism
  I/O-bound Python threads = works fine (GIL released during I/O)

FIX FOR CPU WORK:
  Use multiprocessing — each process has its own GIL
──────────────────────────────────────────────────────────
C# WITH 8 THREADS ON 8 CORES
──────────────────────────────────────────────────────────
Core 1: ████ Thread A executes
Core 2: ████ Thread B executes   ◄── ALL threads run
Core 3: ████ Thread C executes       simultaneously
Core 4: ████ Thread D executes
...
Core 8: ████ Thread H executes

NO GIL. True parallelism. Near-linear scaling for CPU work.
```

---

### OS Scheduling — Time Slicing

```
TIME ──────────────────────────────────────────────────►

Thread A  ████░░░░████░░░░████░░░░
Thread B  ░░░░████░░░░████░░░░████
Thread C  ░░░░░░░░░░░░░░░░░░░░░░░░  (waiting for I/O)
               ↑
          context switch
          (~microseconds overhead)

Each thread gets a time slice (1-10ms)
OS saves state, loads next thread's state, jumps
This is why 10,000 threads is NOT a valid architecture
```

---

### Process vs Thread — Decision Matrix

```
┌─────────────────┬──────────────────┬──────────────────┐
│ Property        │ Process          │ Thread           │
├─────────────────┼──────────────────┼──────────────────┤
│ Memory          │ Isolated         │ Shared           │
│ Creation cost   │ High             │ Low              │
│ Crash impact    │ Contained        │ Kills process    │
│ Communication   │ IPC / pipes      │ Shared heap      │
│ Python CPU work │ TRUE parallel    │ FAKE parallel    │
│ C# CPU work     │ TRUE parallel    │ TRUE parallel    │
│ Best for        │ Isolation/safety │ Shared state     │
└─────────────────┴──────────────────┴──────────────────┘
```

---

### Key Takeaways — Day 2

- A process is an isolated program instance. A thread is a unit of execution within a process
- The OS scheduler gives each thread a time slice — this creates the illusion of simultaneous execution
- Python's GIL prevents CPU-bound threads from running in parallel — use `multiprocessing` instead
- C# has no GIL — threads run truly in parallel on multiple cores
- Every `threading.Thread` in Python maps to one real OS kernel thread (~1MB stack each)

---

<a name="day-3"></a>
## Day 3 — Memory Management and Garbage Collection

### The Hotel Analogy

```
┌─────────────────────────────────────────────────────────┐
│                      THE HOTEL                          │
│                                                         │
│  Front Desk (Allocator)                                 │
│  "You need memory? Here's room 0x4A2F, key is yours."   │
│                                                         │
│  ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐             │
│  │██│ │  │ │██│ │██│ │  │ │██│ │  │ │██│  ROOMS       │
│  └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘  (memory)   │
│  used free used used free used free used               │
│                                                         │
│  Problem: guests forget to check out → memory leak     │
│                                                         │
│  Python solution: housekeeper counts key holders       │
│                   0 holders = immediate reclaim        │
│                                                         │
│  C# solution:     cleaning crew runs periodically      │
│                   finds unreachable rooms, reclaims all │
└─────────────────────────────────────────────────────────┘
```

---

### Python — Reference Counting

```python
x = [1, 2, 3]    # refcount = 1  ──► object alive
y = x             # refcount = 2  ──► object alive
z = x             # refcount = 3  ──► object alive
del z             # refcount = 2  ──► object alive
del y             # refcount = 1  ──► object alive
del x             # refcount = 0  ──► IMMEDIATELY DEALLOCATED
                  #                   no GC needed, instant
```

**The Fatal Flaw — Circular References:**
```
a = {}
b = {}
a['ref'] = b   ──► b refcount = 2 (b + a's reference)
b['ref'] = a   ──► a refcount = 2 (a + b's reference)

del a          ──► a refcount = 1  (b still holds it) ≠ 0
del b          ──► b refcount = 1  (a still holds it) ≠ 0

Neither reaches 0. Both are leaked.
Solution: Python's cyclic GC runs periodically to detect cycles.
```

---

### Generational GC — The Key Insight

```
EMPIRICAL OBSERVATION: Most objects die young.
─────────────────────────────────────────────────────────

                    GENERATIONS
         ┌──────────┬──────────┬──────────┐
         │  Gen 0   │  Gen 1   │  Gen 2   │
         │  (new)   │(survived)│  (old)   │
         │          │          │          │
Collected│frequently│sometimes │  rarely  │
         │          │          │          │
Objects  │loop vars │mid-lived │  caches  │
         │temp str  │ objects  │  conns   │
         │one-use   │          │  pools   │
         └──────────┴──────────┴──────────┘
              ▼           ▼           ▼
         Promote if   Promote if   Stay here
         survives     survives     until dead

C# equivalent:  Gen 0 → Gen 1 → Gen 2 → LOH (>85KB objects)
Python:         Gen 0 → Gen 1 → Gen 2
```

---

### GC Pause — The Production Risk

```
TIMELINE — C# service with heavy allocation:

t=0ms   ──── normal execution ────────────────────────────
t=50ms  ──── normal execution ────────────────────────────
t=100ms ──── GC PAUSE BEGINS ─────────────────────────────
             ████████████████████  (all threads stopped)
             Gen 2 collection
             traces entire object graph
t=180ms ──── GC PAUSE ENDS ───────────────────────────────
t=180ms ──── normal execution ────────────────────────────

80ms pause on a system with 100μs latency target = DISASTER

MITIGATIONS:
• Reduce heap allocations — less garbage = GC runs less
• Use structs (stack) instead of classes (heap)
• Object pooling — reuse objects, avoid allocator entirely
• GCSettings.LatencyMode = SustainedLowLatency
• Avoid LOH allocations (objects >85KB)
```

---

### Stack vs Heap Allocation Cost

```
STACK ALLOCATION
─────────────────
Before call:  [frame A][frame B] ↑ SP

After call:   [frame A][frame B][frame C] ↑ SP
                                  ↑
                       Just moved a pointer. FREE.

After return: [frame A][frame B] ↑ SP
                       Frame C gone. FREE.

HEAP ALLOCATION
─────────────────
1. Call allocator
2. Allocator searches free list for suitable block
3. Split block, update free list metadata
4. Return pointer
5. Eventually: GC must find, trace, and reclaim
= REAL COST at every step
```

---

### Key Takeaways — Day 3

- Python uses reference counting (immediate) + cyclic GC (periodic) for memory management
- C# uses tracing GC — marks reachable objects, collects everything else
- Circular references defeat reference counting — always need the cyclic GC backstop
- Generational GC exploits the fact that most objects die young
- GC pauses are a latency tax — in financial systems, they can be catastrophic
- Stack allocation is free. Heap allocation has allocator + GC cost. Prefer stack when possible
- Memory leaks exist in managed languages — any reachable-but-unused reference is a leak

---

<a name="day-4"></a>
## Day 4 — Data Types and Memory Representation

### Everything Is Bits

```
The same 8 bits mean different things depending on how you read them:

01000001

  Read as unsigned integer:  65
  Read as ASCII character:   'A'
  Read as part of float:     depends on position

The TYPE SYSTEM is the agreement about interpretation.
Type confusion = reading the same bits differently = silent corruption.
```

---

### Integers — Two's Complement

```
8-BIT SIGNED INTEGER RANGE: -128 to +127

Positive: normal binary
  0  = 00000000
  1  = 00000001
  42 = 00101010
  127= 01111111

Negative: flip all bits, add 1
  -1  = 11111111   (flip 00000001 → 11111110, add 1 → 11111111)
  -42 = 11010110
  -128= 10000000

WHY TWO'S COMPLEMENT?
Addition works identically for positive AND negative:

  00000001  (+1)
+ 11111111  (-1)
──────────
  00000000  (0, carry discarded) ✓

One addition circuit handles all cases. No special sign logic needed.
```

---

### Floating Point — IEEE 754

```
64-BIT DOUBLE LAYOUT:
┌──┬───────────┬────────────────────────────────────────┐
│ S │  Exponent │              Mantissa                  │
│ 1 │  11 bits  │              52 bits                   │
└──┴───────────┴────────────────────────────────────────┘

Value = sign × mantissa × 2^exponent

THE FUNDAMENTAL PROBLEM:
  0.1 in decimal = 0.000110011001100... in binary (infinite!)
  Hardware stores the closest finite approximation
  Approximation error accumulates

CONSEQUENCE:
  0.1 + 0.2 = 0.30000000000000004  (not 0.3)
  0.1 + 0.2 == 0.3 → FALSE

RULE: NEVER use float/double for money.
      Use decimal (C#) or Decimal (Python) for financial values.
      Or store as integer cents: $19.99 → 1999 (int)
```

---

### String Encoding

```
TEXT IS NUMBERS. The encoding is the agreement.

CHARACTER   UTF-8 BYTES    UTF-16 BYTES   NOTE
─────────────────────────────────────────────────────────
'A'         41             41 00          ASCII: 1 byte UTF-8
'é'         C3 A9          E9 00          2 bytes UTF-8
'中'        E4 B8 AD       2D 4E          3 bytes UTF-8, 2 UTF-16
'📈'        F0 9F 93 88    3C D8 88 DC    4 bytes both (surrogate pair)

PYTHON internals: flexible (Latin-1 / UCS-2 / UCS-4)
C# internals:     always UTF-16

C# TRAP: "📈".Length == 2  (counts UTF-16 code units, not characters)
Python:   len("📈") == 1   (counts Unicode code points)
```

---

### Value Types vs Reference Types

```
VALUE TYPE                    REFERENCE TYPE
──────────────────────────────────────────────────────────
Variable CONTAINS the value   Variable POINTS to the value

int x = 42;                   int[] arr = {1,2,3};

Stack: [42]                   Stack: [0x4A2F] ──► Heap: [1][2][3]
        ↑                              ↑
        x IS the value                x is a pointer

ASSIGNMENT:                   ASSIGNMENT:
int a = 42;                   int[] x = {1,2,3};
int b = a;  // copy           int[] y = x;  // same object!
b = 99;                       y[0] = 99;
// a still 42                 // x[0] is NOW 99

C# structs  = value type      C# classes = reference type
Python:     EVERYTHING is a reference type (heap objects)
```

---

### Struct Layout and Alignment Padding

```
UNOPTIMIZED FIELD ORDER:

struct Bad {
    byte   Flag;    // 1 byte
    // [3 bytes padding — int must align to 4-byte boundary]
    int    Value;   // 4 bytes
    byte   Status;  // 1 byte
    // [7 bytes padding — double must align to 8-byte boundary]
    double Amount;  // 8 bytes
}
Total: 24 bytes  (only 14 bytes of real data — 10 wasted)

OPTIMIZED — largest fields first:

struct Good {
    double Amount;  // 8 bytes  (8-byte aligned, no padding needed)
    int    Value;   // 4 bytes  (4-byte aligned, no padding needed)
    byte   Flag;    // 1 byte
    byte   Status;  // 1 byte
    // [2 bytes natural end padding]
}
Total: 16 bytes  (14 bytes data + 2 bytes end padding)

RULE: Order fields largest → smallest to minimize padding.
```

---

### Key Takeaways — Day 4

- All data is bits — the type system determines how to interpret them
- Two's complement lets CPUs use one addition circuit for all signed arithmetic
- Floating point cannot represent most decimals exactly — never use for money
- Use `decimal` (C#) or `Decimal` (Python) for financial calculations
- Value types copy data. Reference types copy pointers. Know which you're using
- Python's `is` checks identity (same object). `==` checks value. Never confuse them
- Struct field order affects memory size through alignment padding — order largest to smallest
- Python integers are 28 bytes because they carry refcount, type pointer, and value metadata

---

<a name="day-5"></a>
## Day 5 — Control Flow, Functions, and the Call Stack

### Control Flow = Compare + Jump

```
EVERYTHING compiles to two CPU instructions:

if x > 0:           CMP  rax, 0      ← compare, sets CPU flags
    result = x      JLE  skip        ← jump if ≤ 0 (conditional)
                    MOV  rbx, rax    ← result = x
                skip:

for i in range(n):  MOV  rcx, 0     ← i = 0
    ...             loop_top:
                    CMP  rcx, n     ← compare i with n
                    JGE  loop_end   ← if i >= n, exit
                    ; loop body
                    INC  rcx        ← i++
                    JMP  loop_top   ← unconditional jump back
                    loop_end:

There is no magic. Every if/for/while is compare + jump.
```

---

### The Call Stack — Frame by Frame

```
WHEN function_a CALLS function_b CALLS function_c:

HIGH ADDRESS
┌─────────────────────────────┐
│  function_a frame           │  ← pushed first
│  • return address           │
│  • saved registers          │
│  • local variables          │
│  • parameters               │
├─────────────────────────────┤
│  function_b frame           │  ← pushed when a calls b
│  • return address (→ a)     │
│  • local variables          │
├─────────────────────────────┤
│  function_c frame           │  ← stack pointer here
│  • return address (→ b)     │     (top of stack)
│  • local variables          │
└─────────────────────────────┘
LOW ADDRESS

When function_c returns:
1. Return value → register
2. Stack pointer moves up (frame_c gone instantly)
3. CPU jumps to saved return address in frame_b
4. function_b continues from where it left off
```

---

### Closures — Captured Variables

```python
def make_accumulator(initial):
    total = initial          # lives in make_accumulator's frame

    def add(amount):
        nonlocal total
        total += amount      # references 'total' from enclosing scope
        return total

    return add
# make_accumulator returns → its stack frame is GONE
# But 'total' is still alive — Python moved it to a CELL OBJECT on the heap
# 'add' holds a reference to this cell
# The cell lives as long as 'add' lives

account = make_accumulator(1000)
account(500)   # → 1500   (total on heap = 1500)
account(-200)  # → 1300   (total on heap = 1300)
```

```
MEMORY LAYOUT OF A CLOSURE:

Stack (make_accumulator frame — GONE after return)
  [was: total=1000]

Heap:
  ┌──────────────────┐     ┌─────────────────┐
  │  function object │────►│  cell object    │
  │  'add'           │     │  total = 1300   │
  └──────────────────┘     └─────────────────┘
  ↑
  'account' variable (on stack of caller) points here
```

---

### Recursion — The Stack as Data Structure

```
factorial(4) — call stack builds up:

┌────────────────┐
│ factorial(4)   │  waiting for factorial(3)...
├────────────────┤
│ factorial(3)   │  waiting for factorial(2)...
├────────────────┤
│ factorial(2)   │  waiting for factorial(1)...
├────────────────┤
│ factorial(1)   │  BASE CASE → returns 1
└────────────────┘

Unwind:
  factorial(1) → 1
  factorial(2) → 2 × 1 = 2       frame popped
  factorial(3) → 3 × 2 = 6       frame popped
  factorial(4) → 4 × 6 = 24      frame popped

DEPTH LIMIT: Stack is finite (~8MB typical)
             1000 frames = Python's default recursion limit
             Equivalent iterative loop = no limit (just a counter)
```

---

### Generators — Suspended Frames

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a          # SUSPEND: save frame state, return value
        a, b = b, a + b  # RESUME here on next next()

gen = fibonacci()
next(gen)  # → 0   (runs until yield, suspends)
next(gen)  # → 1   (resumes from yield, runs until yield again)
next(gen)  # → 1
next(gen)  # → 2

KEY INSIGHT:
  Normal function: frame created on call, DESTROYED on return
  Generator:       frame created on call, KEPT ALIVE on yield
                   Frame lives on the HEAP between yields
                   This is why generators enable infinite lazy sequences
```

---

### Key Takeaways — Day 5

- All control flow (if/for/while) compiles to compare + conditional jump at the CPU level
- A stack frame holds: return address, saved registers, parameters, local variables
- Functions are first-class objects in Python — they live on the heap, can be passed and returned
- Closures capture variables from enclosing scope by moving them to heap-allocated cell objects
- Recursion uses the call stack as an implicit data structure — one frame per recursive call
- Python has a ~1000 frame recursion limit to prevent stack overflow
- Generator frames are heap-allocated and survive between `yield` calls — enabling lazy sequences
- Inlining eliminates function call overhead — critical for hot paths in performance code

---

<a name="day-6"></a>
## Day 6 — Project: Trade Data Pipeline

### Architecture Overview

```
trades.csv
    │
    ▼
┌─────────────────────────────────────────────────────┐
│                   PIPELINE                          │
│                                                     │
│  ┌──────────┐    ┌──────────┐    ┌──────────────┐  │
│  │  PARSER  │───►│VALIDATOR │───►│ TRANSFORMER  │  │
│  │          │    │          │    │              │  │
│  │CSV rows  │    │Business  │    │ Calculate    │  │
│  │→ Trade   │    │rules     │    │ notional     │  │
│  │objects   │    │Pure fn   │    │ = qty×price  │  │
│  │Generator │    │No state  │    │              │  │
│  └──────────┘    └──────────┘    └──────────────┘  │
│       │               │                 │           │
│  ValidationErrors  Rejected         Valid trades    │
│       │           appended              │           │
│       ▼                                ▼            │
│  ┌─────────────────────────────────────────────┐   │
│  │              AGGREGATOR                     │   │
│  │  Per-symbol: trade count, volume, VWAP,     │   │
│  │  min/max price, buy count, sell count       │   │
│  └─────────────────────────────────────────────┘   │
│                        │                            │
│                        ▼                            │
│  ┌─────────────────────────────────────────────┐   │
│  │               REPORTER                      │   │
│  │  Formats and prints terminal output         │   │
│  │  Separated from all business logic          │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

### Design Principles Applied

```
Principle               How it appeared in the pipeline
──────────────────────────────────────────────────────────
Separation of concerns  Parser / Validator / Aggregator /
                        Reporter are independent modules

Pure functions          validate_trade() has no side effects
                        Same input always → same output
                        Easy to test in isolation

Generator-based I/O     parse_trades() yields one record
                        at a time — O(1) memory regardless
                        of file size

Explicit error types    ValidationError is a first-class
                        type, not an exception — errors are
                        data, not exceptional events

Typed data models       Trade dataclass — all fields typed
                        Catches bugs at the boundary
```

---

### VWAP — Volume Weighted Average Price

```
VWAP = Total Notional Value / Total Volume

Where:
  Notional Value = quantity × price   (per trade)
  Total Notional = sum of all notionals
  Total Volume   = sum of all quantities

Example (AAPL):
  T001: 100 × $189.50 = $18,950
  T003: 200 × $189.75 = $37,950
  T006: 150 × $190.20 = $28,530
  T009: 300 × $189.90 = $56,970
  T011: 500 × $188.50 = $94,250
  ─────────────────────────────
  Total notional: $236,650
  Total volume:   1,250 shares
  VWAP: $236,650 / 1,250 = $189.32

VWAP is the standard benchmark for execution quality
in institutional trading. "Did I buy near VWAP?"
```

---

### Week 1 Concepts in the Pipeline

```
Day 1 concept → Pipeline appearance
  • Python execution model → generator parser
  • Stack vs heap → Trade objects on heap, loop counters on stack

Day 2 concept → Pipeline appearance
  • Processes → pipeline could be distributed across workers

Day 3 concept → Pipeline appearance
  • GC pressure → generator avoids loading all records into memory
  • Object creation → one Trade per valid record

Day 4 concept → Pipeline appearance
  • Data types → Trade fields: str, int, float, datetime
  • Float for analytics → explicitly noted, Decimal for accounting

Day 5 concept → Pipeline appearance
  • Control flow → validation if/elif chains
  • Pure functions → validate_trade, transform_trade
  • Generators → parse_trades yields one at a time
  • First-class functions → pipeline stages passed and composed
```

---

<a name="mental-model-map"></a>
## Week 1 Mental Model Map

```
                    YOUR CODE
                       │
                       ▼
           ┌───────────────────────┐
           │   LANGUAGE RUNTIME    │
           │  Python VM / CLR JIT  │
           └───────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
    ┌─────────┐  ┌──────────┐  ┌──────────┐
    │  STACK  │  │   HEAP   │  │   CODE   │
    │ frames  │  │ objects  │  │ segment  │
    │ locals  │  │  GC mgd  │  │ machine  │
    │ fast    │  │  slower  │  │  code    │
    └─────────┘  └──────────┘  └──────────┘
         │             │
         └──────┬───────┘
                ▼
    ┌───────────────────────┐
    │   OPERATING SYSTEM    │
    │  process management   │
    │  thread scheduling    │
    │  memory mapping       │
    │  I/O management       │
    └───────────────────────┘
                │
                ▼
    ┌───────────────────────┐
    │      HARDWARE         │
    │  CPU cores            │
    │  CPU cache hierarchy  │
    │  RAM                  │
    │  Storage              │
    └───────────────────────┘
```

---

<a name="analogies"></a>
## Key Analogies Reference

| Concept | Analogy | Core Insight |
|---|---|---|
| CPU | Factory worker | Executes one instruction card at a time, billions/sec |
| Registers | Worker's hands | Fastest storage, holds exactly what's being used NOW |
| RAM | Warehouse | Stores everything, slower than cache |
| Memory hierarchy | Distance from desk | Farther away = slower access |
| Stack | Notepad during a meeting | Write, use, tear off — instant, automatic |
| Heap | Rented storage unit | Flexible, persists, someone must clean it up |
| Process | Separate restaurant | Own kitchen, own staff, fire in one doesn't spread |
| Thread | Cook in a kitchen | Shares the kitchen (heap), own notepad (stack) |
| GIL | Head chef who only talks to one cook at a time | Serializes Python bytecode execution |
| GC generations | Hotel floors | New guests checked frequently, long-stay guests rarely |
| Context switch | Chef swapping between orders | Necessary overhead — too many switches = inefficiency |
| Closure | Chef taking a sub-recipe's ingredients home | Captured variables survive the enclosing scope |
| Generator | Chef pausing a recipe mid-step | Frame suspended, resumes exactly where it left off |
| Call stack | Chef's notepad pages | One page per active sub-recipe, torn off on return |

---

<a name="comparison"></a>
## Python vs C# — Week 1 Comparison

| Concept | Python | C# |
|---|---|---|
| Execution | Bytecode → PVM interprets | IL → JIT → native machine code |
| Speed (CPU) | ~10-100x slower | Near-native |
| Integer size | Unlimited (arbitrary precision) | Fixed (int=4B, long=8B) |
| Integer overflow | Never (grows automatically) | Silent wrap-around (use `checked`) |
| Typing | Dynamic — type on the object | Static — type on the variable |
| Memory model | Everything is a heap reference | Value types (stack) + reference types (heap) |
| GC | Reference counting + cyclic GC | Tracing generational GC |
| GC pauses | Usually small (refcounting is immediate) | Stop-the-world possible (Gen 2) |
| Threading | 1:1 OS threads, GIL prevents CPU parallelism | 1:1 OS threads, true CPU parallelism |
| CPU parallel | Use `multiprocessing` | Use `Task.Run` / thread pool |
| Struct equivalent | `dataclass` (heap) | `struct` (stack when local) |
| Float precision | `float` = 64-bit double | `float`=32-bit, `double`=64-bit |
| Exact decimal | `decimal.Decimal` | `decimal` (128-bit, base-10) |
| String encoding | Flexible internal (Latin-1/UCS-2/UCS-4) | Always UTF-16 internally |
| First-class functions | Yes — functions are objects | Yes — delegates, `Func<T>`, lambdas |
| Generators | `yield` in functions | `yield return` in iterator methods |
| Closures | Captured vars → cell objects on heap | Captured vars → compiler-generated class on heap |
| Recursion limit | ~1000 frames (configurable) | Limited by stack size (~1MB default) |

---

<a name="vocabulary"></a>
## Vocabulary Reference

| Term | Definition |
|---|---|
| **Fetch-decode-execute** | The CPU's fundamental loop: load instruction, interpret it, run it |
| **JIT compilation** | Just-In-Time: compile to native code at runtime on first use, cache result |
| **Bytecode** | Intermediate compiled form — not machine code, not source — Python's .pyc |
| **IL / CIL** | Intermediate Language — C#'s bytecode equivalent, stored in assemblies |
| **Stack frame** | A block of memory on the stack holding a function's locals, args, return address |
| **Heap** | Region of memory for dynamic allocation — GC managed in Python and C# |
| **GC** | Garbage Collector — runtime system that reclaims unreachable memory |
| **Reference counting** | Python's primary GC: track how many variables point to each object |
| **Tracing GC** | C#'s approach: start from roots, mark all reachable objects, collect the rest |
| **Generational GC** | Collect young objects frequently, old objects rarely — exploits object mortality |
| **Stop-the-world** | GC pause where all application threads halt while GC traces |
| **GIL** | Global Interpreter Lock — Python mutex allowing only one thread to execute bytecode |
| **Process** | An isolated running program instance with its own memory space |
| **Thread** | A unit of execution within a process — shares heap, has own stack |
| **Context switch** | OS saves current thread state, loads another thread's state to run it |
| **Value type** | Variable contains data directly (C# struct, int, double) |
| **Reference type** | Variable contains a pointer to heap-allocated data (C# class, Python everything) |
| **Two's complement** | Binary encoding of signed integers — enables unified addition circuit |
| **IEEE 754** | Standard for floating-point binary representation — source of 0.1+0.2≠0.3 |
| **VWAP** | Volume-Weighted Average Price — total notional / total volume |
| **Closure** | Function that captures variables from its enclosing scope |
| **Generator** | Function that suspends at `yield`, preserving frame state on the heap |
| **Inlining** | Compiler optimization replacing a function call with the function body |
| **Cache miss** | CPU needs data not in cache — must fetch from RAM, 100x slower |
| **Alignment padding** | Bytes inserted between struct fields to satisfy CPU alignment requirements |
| **LOH** | Large Object Heap — C# allocates objects >85KB here, collected with Gen 2 |
| **Object pooling** | Reusing pre-allocated objects instead of creating new ones — eliminates GC pressure |
| **Notional value** | The total dollar value of a trade: quantity × price |

---

## Week 1 in One Paragraph

A computer is a worker executing one instruction per cycle, billions of times per second, reading from a memory hierarchy where speed decreases and capacity increases as you move from registers to cache to RAM. Your Python source code is translated by the CPython interpreter to bytecode at runtime — one layer of indirection that costs 10-100x in speed versus C#, which compiles to IL and then JIT-compiles to native machine code. The OS creates processes (isolated memory containers) and threads (execution units within processes), scheduling them via time-slicing across CPU cores. Python's GIL prevents CPU-bound threads from running in parallel — use multiprocessing instead. Memory is managed through reference counting and cyclic GC in Python, and generational tracing GC in C# — both can produce pauses that matter in latency-sensitive systems. All data is ultimately bits: integers in two's complement, floats in IEEE 754 approximation, text as numeric encodings. Control flow is compare-plus-jump at the CPU level. Function calls build stack frames. Closures move captured variables to the heap. Generators suspend stack frames between yields. Every concept from this week appeared in the trade pipeline: typed data models, generator-based parsing, pure validation functions, aggregation, and a reporter cleanly separated from all business logic.

---

*End of Week 1 Notes — Engineering Command Center*
*Next: Week 2 — Programming Mechanics*
