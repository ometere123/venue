# VENUE reviewer evidence

Populate this file only with observed local-test or finalized Studionet evidence.

## Source

- Source commit used for deployment: `92efa0ed796f3a8de5373e23c0515959c8849ded`
- Evidence commit: reported as the final Git SHA after push
- Direct Mode result: **20/20 passed in Linux**

## Toolchain

- Repository-local GenLayer CLI: **0.39.1**
- Network: **Studionet**
- Chain ID: **61999**
- RPC: `https://studio.genlayer.com/api`

## Deployment

- Contract address: `0x8bf3F317ecCF760F7380d2427e8a22Ba06aeAc92`
- Deployment transaction: `0x8f39d1680a2bd49f62c584ee2ed3a7fb52ec97b9a27e7c6f6150a1390e04de6b`
- Deployment finality/result: `FINALIZED / ACCEPTED / MAJORITY_AGREE / SUCCESS`
- `runtime_chain_id()`: `61999`
- Explorer: https://explorer-studio.genlayer.com/address/0x8bf3F317ecCF760F7380d2427e8a22Ba06aeAc92

## Routing book

- Book ID: `1`
- Book creation transaction: `0xf1c763c34d7b8c7f995fc6edd75ca111a6e9f2cdb0fd91c813bb7055bbc10474`
- Software venue ID: `1`; transaction `0xa19ff8333a2141d96034b54c733c0b5f220021d1c3c962231f6c9f79902fd596`
- Privacy venue ID: `2`; transaction `0x06d4461f41c499fa1d4fd5cdb10e82380cbf34b9e2078412248399a33843c575`
- Logistics venue ID: `3`; transaction `0x0a3ab6bbb305a80acefa9161f9c0dff2c22d12a75450013c74233ca56577aab0`
- Seal transaction: `0x19c1481c09b9f4b92435b778246cdc3f61c4ae8ddb204f5761613faafcdc2cfd`
- Sealed readback: `status=1`, `venue_ids=[1,2,3]`

## Scenario A — SINGLE

- Transaction: `0x37cfabd7ebaf368419960fc975b8705fb84014ed9e85dd598fa5158896bddf3c`
- Route ID: `1`
- Status: `SINGLE`
- Matched venues: `[1]`; ambiguous venues: `[]`; single venue: `1`
- Evaluated count: `3`; no-match count: `2`
- Resolver proof: `is_single_route=true`, `single_resolver=0xb29Ead15B1E8A2420faE84de974088f67a15ccC2`

## Scenario B — MULTI_SCOPE

- Transaction: `0xec5ba811df578e900da975659bf50e88e9dce080e10c50ba2156d94a792a6092`
- Route ID: `2`
- Status: `MULTI_SCOPE`
- Matched venues: `[1,2]`; ambiguous venues: `[]`; evaluated count: `3`
- `is_matched_venue(2,1)=true`, `is_matched_venue(2,2)=true`; `single_resolver` refused

## Scenario C — NO_VENUE

- Transaction: `0xb8b87a085f3c49e9cf0baa657b0da98e51c4bf3a2d0a9297c1e80a440dd5ecd7`
- Route ID: `3`
- Status: `NO_VENUE`
- Matched venues: `[]`; ambiguous venues: `[]`; no-match count: `3`; evaluated count: `3`
- `single_resolver` refused

## Scenario D — AMBIGUOUS

- Transaction/evidence: `0x6b5a43b3eed8253b519a0a8eb98468a55903750384bad397fbb92ea123333e41`
- Route ID: `4`
- Status: `AMBIGUOUS`
- Ambiguous venues: `[1,2,3]`; matched venues: `[]`; evaluated count: `3`
- Finalized result: `ACCEPTED / MAJORITY_AGREE / SUCCESS`

## Explorer links

- Contract: https://explorer-studio.genlayer.com/address/0x8bf3F317ecCF760F7380d2427e8a22Ba06aeAc92
- Deployment: https://explorer-studio.genlayer.com/tx/0x8f39d1680a2bd49f62c584ee2ed3a7fb52ec97b9a27e7c6f6150a1390e04de6b
- SINGLE: https://explorer-studio.genlayer.com/tx/0x37cfabd7ebaf368419960fc975b8705fb84014ed9e85dd598fa5158896bddf3c
- MULTI_SCOPE: https://explorer-studio.genlayer.com/tx/0xec5ba811df578e900da975659bf50e88e9dce080e10c50ba2156d94a792a6092
- NO_VENUE: https://explorer-studio.genlayer.com/tx/0xb8b87a085f3c49e9cf0baa657b0da98e51c4bf3a2d0a9297c1e80a440dd5ecd7
- AMBIGUOUS: https://explorer-studio.genlayer.com/tx/0x6b5a43b3eed8253b519a0a8eb98468a55903750384bad397fbb92ea123333e41

## Tooling note

`genvm-linter 0.11.0` static lint passed its three checks. Its SDK validation
attempt on this Windows host failed while reading a compressed runner download;
Linux Direct Mode remained the authoritative local behavioural check and passed
20/20. This is a tooling/download issue, not a contract execution failure.

Do not fabricate transaction hashes, addresses, finality or consensus outputs.
