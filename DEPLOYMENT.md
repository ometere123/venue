# VENUE deployment — stable Studionet 61999

VENUE is intentionally pinned to stable **Studionet**, chain ID **61999**.

Do not use Studio-dev or chain 61997.

## 1. Install the repository-local CLI

```bash
npm install
npx genlayer --version
npm run toolchain:check
```

Required CLI version:

```text
0.39.1
```

The repository must not rely on a globally installed `0.40.0rc2`.

## 2. Run Direct Mode

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-test.txt
python scripts/repo-preflight.py
pytest tests/direct -v -s
```

Direct Mode tests explicitly pin stable GenVM `v0.2.12`.

Do not deploy while tests are red.

## 3. Confirm the network

```bash
npx genlayer network set studionet
npx genlayer network info
```

Require:

- Studionet
- chain ID `61999`
- RPC `https://studio.genlayer.com/api`

Stop immediately if any active configuration points to Studio-dev or 61997.

## 4. Deploy

Use:

```bash
npm run deploy:studionet
```

Record the contract address, deployment transaction, finality and exact source commit.

## 5. Verify chain identity

Call:

```text
runtime_chain_id()
```

Expected:

```text
61999
```

## 6. Run live lifecycle

```bash
gltest tests/integration -v -s --network studionet
```

The main live demonstration is documented in `LIVE_DEMO.md`.

## 7. Record evidence

Fill `REVIEW_EVIDENCE.md` only with observed values.

Capture:

- final commit;
- CLI output;
- network info;
- Direct Mode result;
- deployment address/transaction;
- finalized SINGLE route;
- finalized MULTI_SCOPE route;
- finalized NO_VENUE route;
- an AMBIGUOUS result if live consensus produces one reliably;
- route receipt views;
- explorer links where available.

Never fabricate evidence.

## Verified Studionet evidence

Source used for deployment: commit `92efa0ed796f3a8de5373e23c0515959c8849ded`.
The deployed `contracts/venue.py` is 20,833 bytes with SHA-256
`96ccd7a57de0dee1a685c9b5775edf557663da00346c4dadfbee412e4b2eabe3`.

Contract: `0x8bf3F317ecCF760F7380d2427e8a22Ba06aeAc92`

Deployment transaction: `0x8f39d1680a2bd49f62c584ee2ed3a7fb52ec97b9a27e7c6f6150a1390e04de6b`

Deployment result: `ACCEPTED / MAJORITY_AGREE / SUCCESS`.
`runtime_chain_id()` returned `61999`.

Routing book `1` was created and sealed with venue IDs `1` (Software), `2`
(Privacy) and `3` (Logistics). Creation transaction:
`0xf1c763c34d7b8c7f995fc6edd75ca111a6e9f2cdb0fd91c813bb7055bbc10474`.
Venue transactions, in ID order:

- Software: `0xa19ff8333a2141d96034b54c733c0b5f220021d1c3c962231f6c9f79902fd596`
- Privacy: `0x06d4461f41c499fa1d4fd5cdb10e82380cbf34b9e2078412248399a33843c575`
- Logistics: `0x0a3ab6bbb305a80acefa9161f9c0dff2c22d12a75450013c74233ca56577aab0`
- Seal: `0x19c1481c09b9f4b92435b778246cdc3f61c4ae8ddb204f5761613faafcdc2cfd`

All five writes finalized with accepted consensus and successful execution.
The live route transactions also finalized with accepted consensus and successful
execution:

| Scenario | Tx hash | Route/readback |
|---|---|---|
| SINGLE | `0x37cfabd7ebaf368419960fc975b8705fb84014ed9e85dd598fa5158896bddf3c` | Route `1`; status `SINGLE`; matched `[1]`; ambiguous `[]`; evaluated `3`; `is_single_route=true`; `single_resolver=0xb29Ead15B1E8A2420faE84de974088f67a15ccC2` |
| MULTI_SCOPE | `0xec5ba811df578e900da975659bf50e88e9dce080e10c50ba2156d94a792a6092` | Route `2`; status `MULTI_SCOPE`; matched `[1,2]`; ambiguous `[]`; evaluated `3`; `is_matched_venue(2,1)=true`; `is_matched_venue(2,2)=true`; `single_resolver` refused |
| NO_VENUE | `0xb8b87a085f3c49e9cf0baa657b0da98e51c4bf3a2d0a9297c1e80a440dd5ecd7` | Route `3`; status `NO_VENUE`; matched `[]`; ambiguous `[]`; no-match `3`; evaluated `3`; `single_resolver` refused |
| AMBIGUOUS | `0x6b5a43b3eed8253b519a0a8eb98468a55903750384bad397fbb92ea123333e41` | Route `4`; status `AMBIGUOUS`; matched `[]`; ambiguous `[1,2,3]`; evaluated `3`; finalized `ACCEPTED / MAJORITY_AGREE / SUCCESS` |

Explorer base: `https://explorer-studio.genlayer.com`.

The route method accepts only `book_id` and `matter`; no caller-selected venue
subset, preferred resolver or priority is present. The four live receipts all
show `evaluated_count=3`, proving complete-set evaluation for this sealed book.
