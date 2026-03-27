1. Should the 8 validators be pure functions or allow side effects? Why?

They should be pure functions whenever possible.

Why:

predictable behavior
easy unit testing
safe composition
no hidden mutation
easier retry and replay
easier parallelization later

A validator should ideally do one thing:

inspect the order
return success/failure
not mutate external state

If validators have side effects, then:

failures become harder to reason about
order of execution matters more
replay may duplicate effects
testing becomes messier
2. How would you compose them into a pipeline without writing a new function that calls each one explicitly?

Put them in a list and iterate.

Example:

from collections.abc import Callable

Validator = Callable[[dict], str | None]


def run_validators(order: dict, validators: list[Validator]) -> str | None:
    for validator in validators:
        error = validator(order)
        if error is not None:
            return error
    return None

Usage:

validators = [
    validate_symbol,
    validate_side,
    validate_quantity,
    validate_price,
    validate_account,
    validate_position_limit,
    validate_risk_limit,
    validate_session,
]

error = run_validators(order, validators)

That gives you a pipeline without hardcoding every call into one giant function.

A more advanced version can use reduce, but the loop is clearer and faster in Python.

3. One validator calls an external risk service that sometimes takes 50ms to respond. How does this affect the pipeline design? What pattern would you use?

That changes the design a lot.

At 200,000 orders per second, a 50ms blocking call in the middle of a sequential validator chain is catastrophic. It will:

destroy throughput
increase queue depth
create tail latency
make the whole pipeline dependent on network jitter

That validator should not behave like a normal in-process pure validator.

Better patterns:

asynchronous I/O if you must call the service inline
bulk/batched validation if the risk service supports it
caching for repeated checks
circuit breaker + timeout + fallback
preloaded in-memory risk state if architecture allows it

Most likely pattern:

keep local validators synchronous and pure
isolate external risk validation behind an async boundary
use timeouts, retries, and circuit breaking
consider a staged pipeline where local validation happens first, and only surviving orders go to the external risk stage

In practice:

run all cheap local validators first
only then call the risk service
do it asynchronously
protect the system with timeout/circuit-breaker logic

If the risk service is critical, you may need a design where orders are paused or rejected when the service is unavailable, rather than letting a slow dependency stall the whole pipeline.