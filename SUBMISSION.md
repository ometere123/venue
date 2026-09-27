# VENUE submission notes

## Contribution type

**Intelligent Contracts** — standalone reusable primitive. No frontend.

## One-line description

VENUE is a consensus-backed jurisdiction router that classifies one matter against every venue in an immutable routing book and deterministically preserves single-scope, multi-scope, no-venue and ambiguous outcomes.

## Problem

Autonomous systems may have multiple specialised rulebooks or resolvers:

```text
software matters -> Software resolver
privacy matters  -> Privacy resolver
shipping matters -> Logistics resolver
```

If the caller chooses which resolver gets asked, the caller can forum-shop.

VENUE removes that choice. A sealed routing book defines the complete venue set, and every routed matter is evaluated against every venue.

## Semantic boundary

For each venue, GenLayer returns exactly one bounded verdict:

- `MATCH`
- `NO_MATCH`
- `AMBIGUOUS`

Validators independently re-derive the entire verdict vector.

## Deterministic boundary

After consensus:

- zero matches + zero ambiguity -> `NO_VENUE`
- one match + zero ambiguity -> `SINGLE`
- multiple matches + zero ambiguity -> `MULTI_SCOPE`
- any ambiguity -> `AMBIGUOUS`

The LLM cannot:

- choose a preferred resolver;
- apply a venue priority;
- collapse overlapping jurisdictions;
- choose which venues are evaluated;
- suppress ambiguity.

## Anti-forum-shopping property

`route_matter(book_id, matter)` takes no venue subset.

The contract evaluates every venue ID in the sealed book and requires one verdict for every venue.

## Reusable consumer surface

Downstream contracts can query:

- `route_status(route_id)`
- `is_single_route(route_id)`
- `is_matched_venue(route_id, venue_id)`
- `single_resolver(route_id)`

`single_resolver` fails unless the route is exactly `SINGLE`.

## Network target

- Network: **Studionet**
- Chain ID: **61999**
- RPC: `https://studio.genlayer.com/api`
- Repository-local CLI: **0.39.1**
- Studio-dev / 61997: not used

## Evidence status

- Direct Mode: **20/20 passed in GitHub Actions**
- Contract address: `PENDING`
- Deployment transaction: `PENDING`
- Live SINGLE route: `PENDING`
- Live MULTI_SCOPE route: `PENDING`
- Live NO_VENUE route: `PENDING`

No live evidence is claimed before it exists.
