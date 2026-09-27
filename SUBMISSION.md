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

- Direct Mode: **20/20 passed in Linux**
- Contract: `0x8bf3F317ecCF760F7380d2427e8a22Ba06aeAc92`
- Deployment: `0x8f39d1680a2bd49f62c584ee2ed3a7fb52ec97b9a27e7c6f6150a1390e04de6b`
- Runtime chain readback: `61999`
- Live SINGLE route: route `1`, `0x37cfabd7ebaf368419960fc975b8705fb84014ed9e85dd598fa5158896bddf3c`
- Live MULTI_SCOPE route: route `2`, `0xec5ba811df578e900da975659bf50e88e9dce080e10c50ba2156d94a792a6092`
- Live NO_VENUE route: route `3`, `0xb8b87a085f3c49e9cf0baa657b0da98e51c4bf3a2d0a9297c1e80a440dd5ecd7`
- Live AMBIGUOUS route: route `4`, `0x6b5a43b3eed8253b519a0a8eb98468a55903750384bad397fbb92ea123333e41`

See `REVIEW_EVIDENCE.md` for the complete transaction and readback table. All explorer links use `https://explorer-studio.genlayer.com`.

No live evidence is claimed before it exists.
