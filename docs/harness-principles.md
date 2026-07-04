# Harness Principles

Checked: 2026-07-05 Asia/Shanghai

## Definition

An AI agent harness is the runtime substrate around a model-driven agent. It controls how the agent receives a task, observes state, selects context, calls tools, updates memory, handles errors, involves humans, verifies work, and records evidence.

## What A Good Harness Must Make Explicit

- Task contract: objective, constraints, inputs, expected artifacts, done criteria.
- State contract: what is transient, persisted, resumable, and replayable.
- Tool contract: available tools, permissions, schemas, side effects, approval rules.
- Context contract: how context is selected, compressed, and refreshed.
- Verification contract: tests, scorers, invariants, manual review steps.
- Evidence contract: traces, logs, patches, screenshots, costs, and final reports.
- Intervention contract: when humans can approve, redirect, interrupt, or resume.

## Anti-Patterns

- Treating a prompt as the whole harness.
- Comparing agents without fixing task, model, tool access, and budget.
- Counting success without preserving transcripts and verification evidence.
- Letting agents run with broad tools and unclear permissions.
- Adding multi-agent orchestration before the single-agent loop is measurable.
- Relying on model self-assessment as the only scorer.

## Minimum Viable Harness

A useful first harness for local experiments needs:

- Structured task input.
- Bounded agent loop.
- Tool registry.
- Workspace isolation story.
- Trace log.
- Deterministic verifier.
- Cost and latency capture.
- Final artifact bundle.

## Maturity Ladder

| Level | Description | Evidence |
| --- | --- | --- |
| H0 | Prompt plus manual tool use. | Final answer only. |
| H1 | Scripted loop with explicit tools and limits. | Transcript and final artifact. |
| H2 | Instrumented loop with verification and failure attribution. | Trace, verifier output, cost, failure categories. |
| H3 | Production-style harness with persistence, approvals, rollback, and eval gates. | Replayable runs, policy logs, eval history, deployment controls. |

