Exercise 6 — Design Question

Should you model this with inheritance or composition? Why or why not?
Use inheritance for the shared instrument identity and interface, and composition for variable behaviors and relationships. A small class hierarchy makes sense because all instruments share symbol, exchange, currency, and calculate_margin(quantity, price). But not everything should be pushed into inheritance, because some features vary orthogonally. For example, pricing models, settlement rules, and margin policies are often better as composed components rather than hardcoded in subclasses.

What should go in the base class vs what belongs in subclasses?
The base class should contain only the fields and behavior that are truly universal:

symbol
exchange
currency
abstract calculate_margin(quantity, price)

Subclasses should contain only their specific state:

Option: strike, expiry, option type, underlying
Bond: coupon, maturity
Future: delivery date, contract size
Equity: maybe no extra fields beyond the base
FXPair: base currency, quote currency, pip size

Options can be on equities, on futures, or on indices. How does this affect your design?
This is a strong sign you need composition/association, not just inheritance. An option should probably have an underlying reference to another instrument or to an UnderlyingAsset abstraction. That way an option can point to an equity, a future, or an index without exploding the hierarchy into classes like EquityOption, FuturesOption, IndexOption, plus more combinations later.

A colleague suggests a single Instrument class with optional fields for all instrument types. What are the trade-offs of this approach vs a class hierarchy?
A single “god object” is simpler at first, but it creates major problems:

many fields are irrelevant for most instances
invalid combinations become easy (coupon on an equity, strike on an FX spot)
logic becomes full of if instrument.type == ...
type safety gets worse
maintenance gets harder as products grow

A class hierarchy is more structured:

better invariants
cleaner behavior placement
fewer invalid states
easier extension

The downside of a hierarchy is more classes and a bit more upfront design. In practice, the best design is often a small hierarchy plus composition, not a giant inheritance tree and not a single class with dozens of optional fields.