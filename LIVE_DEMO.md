# VENUE live demo

Use only stable **Studionet 61999**.

## Book

Create a routing book with three venues:

### Venue 1 — Software

Scope: software delivery, APIs, implementation, defects and software-service behaviour.

Exclusions: pure privacy and pure physical-shipping matters unless software is also materially involved.

### Venue 2 — Privacy

Scope: personal data, privacy obligations, processing, disclosure, retention and transfer.

Exclusions: pure software-quality or shipping matters with no material personal-data issue.

### Venue 3 — Logistics

Scope: physical shipment, custody, carriage, delivery, cargo handling and transport delay.

Exclusions: pure software/data-processing matters with no physical-shipment issue.

Seal the book before routing anything.

## Scenario A — SINGLE

Matter:

> The supplier delivered the API implementation, but the software returns an incorrect calculation result. No personal data or physical shipment is involved.

Expected:

```text
Software  MATCH
Privacy   NO_MATCH
Logistics NO_MATCH

status = SINGLE
single_venue_id = Software
```

Prove `single_resolver(route_id)` returns the Software resolver.

## Scenario B — MULTI_SCOPE

Matter:

> The software service exported a customer's personal profile to an unauthorised external API. The dispute concerns both the software service behaviour and disclosure of personal data; no physical shipment is involved.

Expected:

```text
Software  MATCH
Privacy   MATCH
Logistics NO_MATCH

status = MULTI_SCOPE
matched = [Software, Privacy]
single_venue_id = 0
```

Prove `single_resolver(route_id)` refuses this result.

## Scenario C — NO_VENUE

Matter:

> The parties disagree about royalty terms for a music performance licence. The matter does not concern software, personal data, or physical shipment.

Expected:

```text
Software  NO_MATCH
Privacy   NO_MATCH
Logistics NO_MATCH

status = NO_VENUE
```

## Scenario D — AMBIGUOUS

Use a deliberately underspecified matter where one venue's applicability cannot safely be resolved.

Expected:

```text
at least one AMBIGUOUS
status = AMBIGUOUS
single_venue_id = 0
```

Do not tune the prompt merely to force this result. Record actual live consensus behaviour.

## Evidence to capture

For each scenario record:

- transaction hash;
- finality;
- route ID;
- `get_route(route_id)` output;
- matched venue IDs;
- ambiguous venue IDs;
- evaluated count;
- route status;
- `single_resolver` result or refusal where relevant.

Also record the routing-book and venue creation transactions and the final contract address.
