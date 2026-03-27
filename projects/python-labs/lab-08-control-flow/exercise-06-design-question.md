1. Should malformed messages be handled with exceptions or a Result type?

Use a Result type for malformed messages.

Why:

malformed messages are expected at a low but steady rate
at 1,000,000 messages per second, 0.1% malformed means about 1,000 bad messages per second
that is not “exceptional” in the runtime sense
if you use exceptions, you are paying exception overhead in a path that happens continuously

The benchmark from Exercise 5 shows the principle: once failures are part of normal flow, Result-style handling is more efficient and more explicit.

Rule of thumb:

use exceptions for infrastructure failures and truly abnormal situations
use Result values for expected per-record validation/parsing failures
2. You catch a NetworkException deep inside a parser. Should you swallow it, log and continue, or re-raise?

Usually: re-raise, or convert it into a higher-level exception with context.

Why:

a network failure is not the same as a malformed message
malformed input is a record-level problem
network failure is a system-level dependency problem

Consequences:

Swallow it

hides real outages
produces silent data loss
makes debugging very hard
downstream code may continue under false assumptions

Log and continue

better than swallowing, but still dangerous if the system cannot actually function correctly
may cause partial processing with missing data
acceptable only if the operation is optional and the caller explicitly allows degradation

Re-raise

preserves failure semantics
lets the orchestrator decide whether to retry, circuit-break, fail over, or stop
keeps error handling at the right level

Best approach:

catch it only to add context, then re-raise
example: raise MarketDataUnavailable(symbol, endpoint) from e
3. A colleague proposes wrapping every function in broad try/except Exception to prevent crashes. What is wrong with this?

This is a bad idea.

Problems:

it catches bugs you do not want to hide, like TypeError, NameError, logic bugs, bad refactors
it destroys observability
it makes failures look like success paths
it encourages silent corruption
it makes root-cause analysis harder because the original error boundary is lost

Most importantly:

“prevent crashes” is not the same as “preserve correctness”

A trading system that silently produces wrong results is worse than one that fails loudly.

What to do instead:

catch specific exceptions at meaningful boundaries
use Result types for expected record-level failures
use targeted exception handling for infrastructure failures
let programmer bugs surface and fail fast
centralize top-level protection at the process boundary, where you can log, alert, and shut down or restart safely

A better structure is:

parser returns Result for malformed messages
network/storage/database layers raise specific exceptions
orchestrator catches specific operational exceptions and decides retry/failover/stop
top-level runner logs any uncaught fatal error and exits cleanly

That gives you resilience without hiding correctness problems.

If you want, I can turn Exercises 1–5 into one consolidated trade_pipeline.py rewrite.