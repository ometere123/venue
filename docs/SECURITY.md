# VENUE security model

## Protected guarantee

VENUE protects one narrow guarantee:

> a stored route is derived from an independently verified semantic classification of the exact matter against the entire immutable venue set of one sealed routing book.

## Threats handled

### Caller forum-shops by selecting venues

The route method accepts only `book_id` and `matter`. It materialises the entire sealed venue list internally. There is no caller-supplied venue subset.

### Resolver identity biases semantic routing

Resolver addresses are not included in the semantic-classification payload. The model cannot prefer or reject a venue based on the identity of its resolver.

### Malicious leader fabricates the verdict vector

Validators independently re-run the full classification and reject a leader vector they do not reproduce.

### Leader omits one venue

Verdict cardinality must exactly equal the sealed venue count.

### Overlap is silently collapsed into one winner

Multiple `MATCH` values deterministically produce `MULTI_SCOPE`. The model never chooses a winner.

### Uncertainty is silently converted into a match or rejection

`AMBIGUOUS` is first-class. Any ambiguous venue makes the overall receipt `AMBIGUOUS`.

### Prompt injection inside matter or venue text

Matter, scope and exclusion strings are serialised as untrusted JSON data. The fixed prompt explicitly forbids obeying instructions found inside them.

### Routing constitution changes after a result

A routing book cannot be modified after sealing. Route receipts therefore remain bound to the exact definitions that were evaluated.

The sealed `constitution_hash` makes that binding explicit, including resolver
addresses while keeping them out of semantic classification. Route receipts
also carry `matter_hash`, the complete ordered `verdict_hash`, and a final
`receipt_hash`. Consumers can use `is_route_receipt` and
`single_resolver_for` to reject a receipt whose constitution or matter does not
match the expected values.

### Consumer treats multi-scope as single

`single_resolver(route_id)` reverts unless the route status is exactly `SINGLE`.

## Deliberate non-goals

VENUE does not prove:

- that a resolver will adjudicate correctly;
- that the routing-book creator wrote fair scopes;
- that the matter author's factual claims are true;
- that the venue definitions reflect real-world law;
- that every conceivable jurisdiction exists in the book;
- that `MATCH` means one venue is superior to another.

VENUE is a routing primitive, not a merits adjudicator or legal opinion engine.

## Liveness trade-off

Exact validator agreement on the full verdict vector is intentionally conservative. Borderline matters may fail to finalise or produce `AMBIGUOUS`. This is preferable to silently routing uncertain matters to a single resolver.

## Bounded computation

Routing books contain at most 8 venues. This bounds prompt size, validator work and receipt storage.

## Network boundary

Active configuration must remain stable Studionet 61999. Studio-dev / 61997 is intentionally excluded.
