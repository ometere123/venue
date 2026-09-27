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
- `is_route_receipt(route_id, expected_constitution_hash, expected_matter_hash, expected_receipt_hash)`
- `single_resolver_for(route_id, expected_constitution_hash, expected_matter_hash)`

`single_resolver` fails unless the route is exactly `SINGLE`.

The current source also provides immutable provenance hashes: `constitution_hash`
binds the complete ordered book including resolvers, `matter_hash` binds the
normalized submitted matter, `verdict_hash` binds the complete ordered verdict
vector, and `receipt_hash` binds those hashes to the deterministic route result.
The hash-aware consumer methods prevent a valid receipt for a different matter
or constitution from being reused accidentally.

## Network target

- Network: **Studionet**
- Chain ID: **61999**
- RPC: `https://studio.genlayer.com/api`
- Repository-local CLI: **0.39.1**
- Studio-dev / 61997: not used

## Evidence status

- Direct Mode: **23/23 passed in Linux**
- Current contract: `0xa189d4c85d75164c266435003d7501A7F6942109`
- Current deployment: `0x54512cd85d7ffde8b5098da353f52684ec2b93002345baab4b25c4cfce49290a`
- Current source commit identified for deployment: `8dd4c3bf5f325d3a64f5392ebf1790dd9bbe1d9b`
- Deployment-captured working-tree source: 28,078 bytes, SHA-256 `eb4032c777ebfe660c9cf28067294874061ce641ba29d908e2021c04a167b70b`
- Canonical Git blob at that commit: 27,498 bytes, SHA-256 `a7fc1a3cfc7c95dbecbcd91ba09ecb636016bcdb83cbd644ea5cba75cc7334e0`
- The records preserve both observed representations and do not claim raw byte-for-byte parity.
- Current live provenance route: `0x164de81c321825f94b85c707026b5bd785c0e48f26369de2ff930949e8d3dd13`
- Current constitution hash: `dba6686bbcca1faf05b7619203bc5c69ef14a1c255c73b3f2cab0d0a68c42ddd`
- Current receipt hash: `43938648c94205c3d73442c71ea029bfcf2c7cffa25fdc63041802a8865d5597`
- Superseded contract: `0x8bf3F317ecCF760F7380d2427e8a22Ba06aeAc92`
- Runtime chain readback: `61999`
- Live provenance SINGLE route: route `1`, `0x164de81c321825f94b85c707026b5bd785c0e48f26369de2ff930949e8d3dd13`
- Live constitution hash: `dba6686bbcca1faf05b7619203bc5c69ef14a1c255c73b3f2cab0d0a68c42ddd`
- Live receipt verification: `is_route_receipt == true`; `single_resolver_for` returned the configured resolver

See `REVIEW_EVIDENCE.md` for the complete transaction and readback table. All explorer links use `https://explorer-studio.genlayer.com`.

The earlier multi-status scenario receipts belong to the superseded deployment and
are not presented as evidence for the current provenance deployment.

No live evidence is claimed before it exists.
