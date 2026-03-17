#Exercise 6 — Design Question
Best architecture for 500k updates/sec

##Direct function calls

-validate()
-normalize()
-risk_check()
-transform()
...

###Pros:

-fastest
-no dynamic dispatch
-best CPU branch prediction

###Cons:

-less flexible
-List of function references
for f in pipeline:
    update = f(update)

###Pros:

-configurable pipeline
-easier to extend

###Cons:

-function pointer lookup
-extra indirect jumps
-Slightly slower.
-Generator pipeline

###Pros:

-composable
-good for streaming

###Cons:

-generator overhead
-context switching
-slower than direct calls
-Not ideal for 500k/sec hot path.

###Best choice

For this workload:

-direct function calls
-Closure capturing configuration
-Closure stores reference to config dict.

###Memory cost:

-1 function object
-1 closure cell
-reference to dict

###Performance cost:

-almost zero after creation
-Access is just pointer dereference.
-So closures are safe even in hot paths.

###Debugging implications

-Direct calls
Best debugging.
You can step through each function in stack trace.

-Function list pipeline
Stack trace includes dynamic dispatch.
Slightly harder.

-Generator pipeline
Hardest.
Because execution is split across:

-yield points
-generator frames

Stack traces become fragmented.