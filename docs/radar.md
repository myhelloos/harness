# AI Agent Harness Radar

Checked: 2026-07-05 Asia/Shanghai

This radar is intentionally conservative. It lists tools and ideas worth testing, not endorsements.

## Near-Term Candidates

| Area | Candidate | Why It Matters | First Probe |
| --- | --- | --- | --- |
| Managed agent runtime | OpenAI Agents SDK | Lightweight primitives for agents, handoffs, guardrails, sessions, tracing, MCP, and sandbox agents. | Build a file-producing agent with tracing and a simple guardrail. |
| Stateful orchestration | LangGraph | Low-level orchestration runtime for long-running, stateful agents with durable execution, streaming, human-in-the-loop, and persistence. | Build a two-node graph with checkpointing and interruption. |
| Multi-agent systems | AutoGen | AgentChat for conversational agents and Core for event-driven multi-agent systems. | Build a two-agent reviewer/implementer loop with bounded turns. |
| Evaluation framework | Inspect AI | Evaluation tasks with datasets, solvers, scorers, agent tools, sandboxing, logs, and external-agent bridges. | Create a tiny code-editing eval with deterministic scoring. |
| Coding benchmark contract | SWE-bench | Real-world issue-resolution benchmark shape; useful for understanding patch contracts and scoring discipline. | Implement a mini SWE-style local task with patch extraction and tests. |

## Research Signals

Recent harness-focused work frames performance as a model-harness-environment system rather than only a model capability problem. Useful dimensions to track:

- Task specification quality.
- Context selection.
- Tool access and permissioning.
- Project memory.
- Task state.
- Observability.
- Failure attribution.
- Verification.
- Entropy and nondeterminism auditing.
- Intervention recording.

## Evaluation Axes

Use the same axes across experiments unless a task clearly needs different ones:

| Axis | Measurement |
| --- | --- |
| Success | Pass/fail plus task-specific score. |
| Cost | Model tokens, API cost estimate, wall time, retries. |
| Reliability | Variance across repeated runs. |
| Debuggability | Trace completeness, replayability, failure attribution quality. |
| Control | Human approval hooks, permission boundaries, interrupt/resume behavior. |
| Portability | Model/provider coupling, framework coupling, environment assumptions. |
| Maintainability | Amount of glue code, clarity of state model, testability. |

## Initial Hypothesis

For software-engineering agents, the harness matters as much as the model once the task requires real tools, state, or verification. The first useful experiments should therefore compare:

1. The same task across different harnesses with the same model where possible.
2. The same harness across different models.
3. Minimal loop versus instrumented loop with tracing, verification, and failure attribution.
