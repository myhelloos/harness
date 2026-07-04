# Workspace Instructions

This repo is an AI agent harness exploration lab.

## Operating Principles

- Prefer current primary sources: official docs, repos, release notes, benchmark pages, and papers.
- Date all external claims. This field changes quickly.
- Keep experiments reproducible before making broad conclusions.
- Separate observations from recommendations.
- Record failed experiments; they are useful evidence.
- Do not introduce heavy framework dependencies until a concrete experiment needs them.

## Expected Workflow

When making changes here:

1. Read `README.md`, `docs/radar.md`, and relevant experiment or eval notes first.
2. If the task involves current tools, verify official sources before updating claims.
3. Add or update source links in `docs/source-map.md`.
4. For experiments, create a subdirectory under `experiments/` with:
   - `README.md`
   - setup commands
   - run commands
   - result notes
   - known limitations
5. For evaluations, keep task definition, scoring method, raw logs, and analysis separate.

## Quality Bar

- Favor small, runnable probes over large speculative scaffolds.
- Every comparison should name the task class being compared.
- A harness is only "effective" relative to a workload, budget, and risk profile.
- Preserve exact versions and dates for anything benchmark-related.

