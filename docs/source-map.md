# 来源地图

检查日期：2026-07-05 Asia/Shanghai

使用这个文件保持外部事实性判断的新鲜度。优先使用一手来源。

## 框架与运行时

| 主题 | 来源 | 说明 |
| --- | --- | --- |
| Claude Code | https://code.claude.com/docs/en/overview | Agentic coding tool；通过 `CLAUDE.md` 和 auto memory 提供记忆；包含 hooks、MCP、permissions 和多个使用界面。 |
| Cursor Agent | https://cursor.com/docs/agent/overview.md | Agent 模型：instructions、tools 和 model；IDE 原生工具、checkpoints、browser 和 terminal。 |
| Codex | https://developers.openai.com/codex/codex-manual.md | Coding agent 手册，覆盖 threads、context、`AGENTS.md`、sandboxing、approvals、skills、plugins、MCP、hooks、memories 和 surfaces。 |
| OpenAI Agents SDK | https://openai.github.io/openai-agents-python/ | Agent loop、handoffs、guardrails、sessions、tracing、MCP、sandbox agents。 |
| LangGraph | https://docs.langchain.com/oss/python/langgraph/overview | 有状态编排运行时；durable execution、streaming、human-in-the-loop、persistence。 |
| AutoGen | https://microsoft.github.io/autogen/stable/ | AgentChat、Core、Extensions、Studio；多 agent 应用框架。 |
| Inspect AI | https://inspect.aisi.org.uk/ | 评测框架，包含 tasks、datasets、solvers、scorers、tools、agents、sandboxing、logs。 |
| SWE-bench | https://www.swebench.com/ 和 https://github.com/swe-bench/SWE-bench | Coding-agent 基准契约和排行榜。 |

## Coding Agent Harness 比较

| 主题 | 来源 | 说明 |
| --- | --- | --- |
| Agent harness software design principles | ./software-design-principles-in-agent-harnesses.md | 本地分析模型：可组合性、关注点分离、单一职责、开闭、依赖倒置、事件驱动、显式状态、最小权限、可观测性优先。 |
| Agentic Loop Java backend practice | ./agentic-loop-java-backend-practice.md | 本地实践模型：Agentic Loop 的机制、最佳实践与 Java 后端日常工作流。 |
| Four-layer harness architecture | ./four-layer-harness-architecture.md | 本地工作模型：记忆层、扩展层、集成层、编程层。 |
| Claude Code memory | https://code.claude.com/docs/en/memory | `CLAUDE.md`、auto memory、加载顺序、imports，以及 memory-as-context 区分。 |
| Claude Code hooks | https://code.claude.com/docs/en/hooks | Lifecycle hooks、`PreToolUse`、`Stop`、compaction、permission、prompt 和 agent hooks。 |
| Claude Code settings | https://code.claude.com/docs/en/settings | Settings scopes、permissions、managed policy、sandbox、hooks、MCP 和 tool behavior。 |
| Claude Code MCP | https://code.claude.com/docs/en/mcp | 外部工具和数据集成。 |
| Cursor rules | https://cursor.com/docs/rules.md | Project、user 和 team rules；`AGENTS.md`；rule activation 和 precedence。 |
| Cursor run modes | https://cursor.com/docs/agent/security/run-modes.md | Auto-review、Allowlist、Run Everything、sandboxing、`permissions.json` 和 `sandbox.json`。 |
| Cursor MCP | https://cursor.com/docs/mcp.md | MCP transports、tools、resources、apps、approval、enterprise controls 和 security notes。 |

## 近期 Harness 研究

| 主题 | 来源 | 说明 |
| --- | --- | --- |
| AI Harness Engineering | https://arxiv.org/abs/2605.13357 | 将 harness 视为运行时基底；model-harness-environment 框架。 |
| Claw-SWE-Bench | https://arxiv.org/abs/2606.12344 | 用于在 coding tasks 上比较 agent harness 的基准和 adapter protocol。 |
| HarnessForge | https://arxiv.org/abs/2606.01779 | harness 与 policy 联合适配研究。 |
| Natural-Language Agent Harnesses | https://arxiv.org/abs/2603.25723 | 将 harness 行为外部化为可移植的自然语言 artifact。 |

## 刷新协议

更新本仓库时：

1. 重新检查官方文档和仓库。
2. 添加检查日期。
3. 为实验记录精确 package version 或 commit SHA。
4. 链接来自 `experiments/` 或 `evals/` 的原始结果。
5. 将过时判断移入 notes，而不是删除证据。
