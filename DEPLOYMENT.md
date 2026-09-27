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
