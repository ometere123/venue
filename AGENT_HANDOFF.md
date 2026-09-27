# VENUE final handoff

Finish VENUE from the existing repository **in place**.

Do not redesign it, restart it, add a frontend, turn it into a full app, or migrate it to Studio-dev.

## Absolute environment

- Network: **Studionet**
- Chain ID: **61999**
- RPC: `https://studio.genlayer.com/api`
- Repository-local GenLayer CLI: **0.39.1**
- Direct Mode GenVM artefact: **v0.2.12**
- Global CLI `0.40.0rc2`: do not use
- Studio-dev / 61997: do not use

## Architecture to preserve

VENUE:

1. creates a routing book;
2. adds bounded venue definitions;
3. seals the full venue set;
4. routes a matter against **every** venue;
5. uses GenLayer consensus only for `MATCH | NO_MATCH | AMBIGUOUS`;
6. deterministically derives `SINGLE | MULTI_SCOPE | NO_VENUE | AMBIGUOUS`;
7. exposes a resolver only for a genuine `SINGLE` result.

Never add model-selected venue priority or caller-selected routing subsets.

## Completion steps

1. Pull latest `main`.
2. Read README, SUBMISSION, ARCHITECTURE, SECURITY, DEPLOYMENT, LIVE_DEMO and REVIEW_EVIDENCE.
3. Run `npm install`.
4. Require `npx genlayer --version` to show exactly `0.39.1`.
5. Run `npm run toolchain:check`.
6. Create/activate a Python venv and install `requirements-test.txt`.
7. Run `python scripts/repo-preflight.py`.
8. Run `pytest tests/direct -v -s` and require the full suite green.
9. Set `studionet`, run `npx genlayer network info`, and verify 61999 plus `https://studio.genlayer.com/api`.
10. Deploy `contracts/venue.py` using the guarded repository deployment path.
11. Call `runtime_chain_id()` and require 61999.
12. Execute the live scenarios in `LIVE_DEMO.md`.
13. Record only genuine finalized evidence in `REVIEW_EVIDENCE.md`.
14. Perform a hostile review for forum-shopping, omitted venues, ambiguous collapse, malicious leader vectors, prompt injection, post-seal mutation, scope overlap and consumer misuse.
15. If a real defect is found, fix it narrowly, add a regression test, rerun the complete suite and repeat affected live paths.
16. Update README/SUBMISSION with observed facts only.
17. Commit and push all legitimate final changes to `ometere123/venue`.

Do not add a frontend.
