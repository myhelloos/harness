# Source Map

Checked: 2026-07-05 Asia/Shanghai

Use this file to keep external claims fresh. Prefer primary sources.

## Frameworks And Runtimes

| Topic | Source | Notes |
| --- | --- | --- |
| OpenAI Agents SDK | https://openai.github.io/openai-agents-python/ | Agent loop, handoffs, guardrails, sessions, tracing, MCP, sandbox agents. |
| LangGraph | https://docs.langchain.com/oss/python/langgraph/overview | Stateful orchestration runtime; durable execution, streaming, human-in-the-loop, persistence. |
| AutoGen | https://microsoft.github.io/autogen/stable/ | AgentChat, Core, Extensions, Studio; multi-agent application framework. |
| Inspect AI | https://inspect.aisi.org.uk/ | Evaluation framework with tasks, datasets, solvers, scorers, tools, agents, sandboxing, logs. |
| SWE-bench | https://www.swebench.com/ and https://github.com/swe-bench/SWE-bench | Coding-agent benchmark contract and leaderboards. |

## Recent Harness Research

| Topic | Source | Notes |
| --- | --- | --- |
| AI Harness Engineering | https://arxiv.org/abs/2605.13357 | Harness as runtime substrate; model-harness-environment framing. |
| Claw-SWE-Bench | https://arxiv.org/abs/2606.12344 | Benchmark and adapter protocol for comparing agent harnesses on coding tasks. |
| HarnessForge | https://arxiv.org/abs/2606.01779 | Joint harness and policy adaptation research. |
| Natural-Language Agent Harnesses | https://arxiv.org/abs/2603.25723 | Externalizing harness behavior as portable natural-language artifacts. |

## Refresh Protocol

When updating this repo:

1. Re-check official docs and repos.
2. Add the date checked.
3. Record exact package versions or commit SHAs for experiments.
4. Link raw results from `experiments/` or `evals/`.
5. Move stale claims into notes instead of deleting evidence.

