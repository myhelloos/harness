# AI Agent Harness Lab

This workspace is a practical exploration base for current, effective AI agent harnesses.

The goal is not to collect every framework. The goal is to build a repeatable way to compare harness designs, run small experiments, preserve evidence, and turn lessons into durable engineering choices.

## Working Model

Use this repo as a living lab:

1. Track the current landscape in `docs/radar.md`.
2. Record harness design principles in `docs/harness-principles.md`.
3. Keep source links and freshness notes in `docs/source-map.md`.
4. Put runnable experiments under `experiments/`.
5. Put evaluation tasks, rubrics, logs, and analysis under `evals/`.
6. Capture major decisions as ADRs under `adr/`.

## Current Focus

The initial comparison axis is:

- Runtime and orchestration: durable execution, state, retries, interruption, human-in-the-loop.
- Tooling and environment: filesystem, shell, browser, MCP, sandboxing, permission boundaries.
- Memory and context: short-term state, persistent sessions, retrieval, compaction.
- Observability: traces, logs, span metadata, replayable transcripts.
- Evaluation: task definitions, scorers, cost, latency, pass rate, failure attribution.
- Production controls: guardrails, approvals, secrets, deployment shape, rollback.

## Repo Layout

```text
.
├── AGENTS.md
├── README.md
├── adr/
├── docs/
├── evals/
├── experiments/
└── templates/
```

## Baseline Rule

Any claim that something is "latest", "best", or "production-ready" must carry:

- Date checked.
- Source URL.
- Version or commit when available.
- A small local reproduction or explicit reason why it was not reproduced.
- Evaluation criteria used to judge it.

