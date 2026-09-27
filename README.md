# VENUE

**Consensus-backed semantic jurisdiction routing without caller-controlled forum shopping.**

VENUE is a standalone GenLayer Intelligent Contract primitive. It intentionally has **no frontend**.

## The primitive

A system may have several specialised resolvers:

```text
software dispute -> Software resolver
privacy dispute  -> Privacy resolver
shipping dispute -> Logistics resolver
```

The naive design lets the caller choose which resolver to invoke.

That is forum shopping.

VENUE instead freezes a **routing book** containing every permitted venue definition. Once sealed, every matter is evaluated against the **entire venue set**.

```text
matter
  |
  v
sealed venue set
  |
  +--> Software  MATCH
  +--> Privacy   MATCH
  +--> Logistics NO_MATCH
  |
  v
deterministic result
MULTI_SCOPE
```

The model never chooses which venue wins. It also never receives resolver addresses during semantic classification, so resolver identity cannot influence the MATCH/NO_MATCH/AMBIGUOUS vector.

## Outcomes

GenLayer validators independently classify every venue using only:

- `MATCH`
- `NO_MATCH`
- `AMBIGUOUS`

Deterministic code then derives:

| Result | Rule |
|---|---|
| `SINGLE` | exactly one MATCH, zero AMBIGUOUS |
| `MULTI_SCOPE` | more than one MATCH, zero AMBIGUOUS |
| `NO_VENUE` | zero MATCH, zero AMBIGUOUS |
| `AMBIGUOUS` | at least one AMBIGUOUS |

If Software and Privacy both apply, VENUE preserves both. It does not ask an LLM which one is "more appropriate".

If Software matches but Privacy is ambiguous, VENUE returns `AMBIGUOUS`, not a convenient single route.

## Anti-forum-shopping invariant

The public write method is:

```text
route_matter(book_id, matter)
```

There is no caller-supplied venue list.

For every route:

```text
evaluated_count == sealed venue count
```

The full verdict vector must also be independently reproduced by validators before route state is written.

## Routing-book lifecycle

```text
OPEN
  |
  +-- add venue definitions
  |
  v
SEALED
  |
  +-- immutable venue set
  +-- routing enabled
```

At least two venues are required; at most eight are allowed.

Each venue contains:

```text
name
scope
exclusions
resolver address
```

## Consumer surface

VENUE declares `IVenue` for downstream Intelligent Contracts.

Useful reads:

```text
get_book(book_id)
get_venue(venue_id)
get_route(route_id)
route_status(route_id)
is_single_route(route_id)
is_matched_venue(route_id, venue_id)
single_resolver(route_id)
runtime_chain_id()
```

`single_resolver` reverts for MULTI_SCOPE, NO_VENUE and AMBIGUOUS receipts.

That means a consumer cannot accidentally treat an unresolved jurisdiction question as a single authoritative venue.

## What VENUE does not claim

VENUE does not decide case merits.

It does not prove venue scopes correspond to real-world law.

It does not claim matter descriptions are truthful.

It does not decide which overlapping venue should win.

It proves a narrower protocol statement:

> against this immutable routing constitution, GenLayer validators independently classified the exact matter against every venue, and the stored route was deterministically derived from that complete vector.

## Network and toolchain

| Setting | Required |
|---|---|
| Network | **Studionet** |
| Chain ID | **61999** |
| RPC | `https://studio.genlayer.com/api` |
| Repository CLI | **GenLayer 0.39.1** |
| Direct Mode GenVM | **v0.2.12** |
| Studio-dev / 61997 | **Not used** |
| Frontend | **None** |

Your globally installed `0.40.0rc2` is intentionally ignored. Repository npm scripts resolve the local `0.39.1` binary.

## Local validation

```bash
npm install
npx genlayer --version
npm run toolchain:check

python -m venv .venv
source .venv/bin/activate
pip install -r requirements-test.txt
python scripts/repo-preflight.py
pytest tests/direct -v -s
```

## Stable Studionet

```bash
npx genlayer network set studionet
npx genlayer network info
npm run deploy:studionet
```

Before any live write, verify:

```text
Studionet
61999
https://studio.genlayer.com/api
```

Then run:

```bash
gltest tests/integration -v -s --network studionet
```

See `LIVE_DEMO.md`, `DEPLOYMENT.md` and `AGENT_HANDOFF.md`.

## Repository layout

```text
contracts/venue.py
tests/direct/
tests/integration/test_venue_studionet.py
docs/ARCHITECTURE.md
docs/SECURITY.md
LIVE_DEMO.md
REVIEW_EVIDENCE.md
DEPLOYMENT.md
SUBMISSION.md
AGENT_HANDOFF.md
scripts/
```

## Current status

Source implementation, Direct Mode suite, CI, deployment guards, live integration scenario and reviewer documentation are included.

Verified locally in Linux Direct Mode: **20/20 tests passed**. The repository-local **GenLayer CLI 0.39.1** and stable Studionet/61999 toolchain guard pass.

The verified Studionet deployment is recorded in `REVIEW_EVIDENCE.md` and `DEPLOYMENT.md`. The live book demonstrates SINGLE, MULTI_SCOPE, NO_VENUE and AMBIGUOUS outcomes against the complete sealed three-venue set.
