# VENUE reviewer evidence

Only observed local-test and finalized Studionet evidence is recorded here.

## Toolchain

- Repository-local GenLayer CLI: **0.39.1**
- Network: **Studionet**
- Chain ID: **61999**
- RPC: `https://studio.genlayer.com/api`
- Direct Mode: **23/23 passed in Linux**
- Contract source commit used for deployment: `8dd4c3bf5f325d3a64f5392ebf1790dd9bbe1d9b`
- Deployed source: 28,078 bytes, SHA-256 `eb4032c777ebfe660c9cf28067294874061ce641ba29d908e2021c04a167b70b`

## Current canonical deployment

- Contract: `0xa189d4c85d75164c266435003d7501A7F6942109`
- Deployment transaction: `0x54512cd85d7ffde8b5098da353f52684ec2b93002345baab4b25c4cfce49290a`
- Final result: `FINALIZED / ACCEPTED / MAJORITY_AGREE / SUCCESS`
- `runtime_chain_id()`: `61999`
- Explorer: https://explorer-studio.genlayer.com/address/0xa189d4c85d75164c266435003d7501A7F6942109

## Current provenance proof

- Book ID: `1`
- Book creation: `0xb01e5d37e437df335155a7d8dca2ec7dd9415ea15947ce3ffdcd165f53d30499`
- Venue 1 Software: `0x799956154668bc5edddc92f67dd39a28f95190869626a99c4bcfdc77600c412a`
- Venue 2 Privacy: `0x6b69e304c460c178883586f2bd3ef892aa94c23e4363627debde27f8516f6aed`
- Venue 3 Logistics: `0x0c21257493c9b16beb0487f30d2314c676527a52707acd745f9d2cfc79e7649a`
- Seal: `0x1c6401206dccfea42dd2cdaa5dcda2ad49f8ac61828576838785a9ba100bcf25`
- Sealed readback: `status=1`, `venue_ids=[1,2,3]`
- Constitution hash: `dba6686bbcca1faf05b7619203bc5c69ef14a1c255c73b3f2cab0d0a68c42ddd`

### SINGLE route

- Transaction: `0x164de81c321825f94b85c707026b5bd785c0e48f26369de2ff930949e8d3dd13`
- Route ID: `1`
- Final result: `FINALIZED / ACCEPTED / MAJORITY_AGREE / SUCCESS`
- Readback: `status=SINGLE`, `matched_venue_ids=[1]`, `ambiguous_venue_ids=[]`, `evaluated_count=3`, `no_match_count=2`, `single_venue_id=1`
- Matter hash: `522aa04c996f133faafee20c7a5a0c8f3603fb6e865bde43f21d71c2b41ce7cb`
- Verdict hash: `0a4e99925310523c1edabf9c76bcb9869495dfdabf68d92fa9e9304565ff025a`
- Receipt hash: `43938648c94205c3d73442c71ea029bfcf2c7cffa25fdc63041802a8865d5597`
- `is_route_receipt(1, constitution_hash, matter_hash, receipt_hash)`: `true`
- `single_resolver_for(1, constitution_hash, matter_hash)`: `0xb29ead15b1e8a2420fae84de974088f67a15ccc2`
- Explorer: https://explorer-studio.genlayer.com/tx/0x164de81c321825f94b85c707026b5bd785c0e48f26369de2ff930949e8d3dd13

The receipt demonstrates that the complete ordered venue set was evaluated and
that the result is cryptographically bound to the sealed constitution, exact
matter, ordered verdict vector and deterministic route outcome. Resolver
addresses are included in the constitution hash but excluded from the semantic
classification payload.

## Superseded deployment

The earlier contract `0x8bf3F317ecCF760F7380d2427e8a22Ba06aeAc92` and its
associated 61999 evidence remain historical migration evidence. The current
canonical contract is the address listed above.

## Tooling note

Static lint passed. The Windows combined GenVM SDK check encountered a corrupted
compressed runner cache; Linux Direct Mode remains the authoritative behavioural
verification and passed 23/23. This is a local tooling/download limitation, not
a live contract execution failure.

The malformed diagnostic call that supplied a pseudo `str` token is not counted
as lifecycle evidence; the clean live calls above used plain CLI arguments.

No private keys, wallet exports or secrets are included.
