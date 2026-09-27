# VENUE architecture

VENUE is a standalone GenLayer Intelligent Contract primitive for semantic jurisdiction routing.

## Core protocol

A routing-book creator registers a bounded set of venue definitions, each containing:

- a human-readable name;
- an inclusion scope;
- explicit exclusions;
- a resolver address.

The book is then sealed. After sealing, the venue set and definitions are immutable.

Any account can submit a matter. VENUE evaluates the matter against **every venue in the sealed book**. The caller cannot choose a subset of venues to test.

For each venue, GenLayer consensus returns one bounded verdict:

- `MATCH`
- `NO_MATCH`
- `AMBIGUOUS`

Validators independently re-derive the full verdict vector with `run_nondet_unsafe`.

## Deterministic outcome derivation

The model never chooses a winning venue.

After consensus, deterministic code derives:

- `SINGLE`: exactly one venue matches and none are ambiguous;
- `MULTI_SCOPE`: more than one venue matches and none are ambiguous;
- `NO_VENUE`: no venue matches and none are ambiguous;
- `AMBIGUOUS`: at least one venue is ambiguous.

Any ambiguity prevents a single resolver from being exposed.

## Anti-forum-shopping invariant

VENUE's central invariant is:

> every sealed venue is evaluated for every routed matter.

There is no write method that accepts a caller-selected venue list.

A caller therefore cannot obtain a preferred result by asking only the resolver it wants.

This does not prevent the routing-book author from designing biased venue scopes. VENUE treats the sealed routing book as the governing constitution. Governance of that constitution is outside the primitive's scope.

## Overlap preservation

VENUE does not resolve overlapping jurisdictions by priority, specificity, convenience or model preference.

If Software and Privacy both clearly apply, the result is:

```text
MULTI_SCOPE
matched = [Software, Privacy]
```

A downstream system can decide how to handle multi-scope matters using its own predeclared rules.

## Ambiguity preservation

If one venue clearly matches but another venue's applicability is genuinely ambiguous, VENUE returns `AMBIGUOUS`, not `SINGLE`.

This prevents uncertainty from being silently erased in order to produce a convenient route.

## State

### RoutingBook

```text
creator
title
OPEN | SEALED
created_at
sealed_at
route_count
venue_ids[]
```

### VenueDefinition

```text
book_id
name
scope
exclusions
resolver
created_at
```

### RouteReceipt

```text
book_id
reporter
matter
status
created_at
evaluated_count
no_match_count
single_venue_id
matched_venue_ids[]
ambiguous_venue_ids[]
```

## Consumer surface

Downstream Intelligent Contracts can use `IVenue` and read:

- `route_status(route_id)`
- `is_single_route(route_id)`
- `is_matched_venue(route_id, venue_id)`
- `single_resolver(route_id)`

`single_resolver` fails unless the receipt is genuinely `SINGLE`.

## Network target

VENUE targets stable **Studionet, chain ID 61999** only.

The repository-local GenLayer CLI is pinned to **0.39.1**.
