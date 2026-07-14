# 来源地图

检查日期：2026-07-15 Asia/Shanghai

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
| Harness 工程化思维 | ./harness-engineering-mindset.md | 本地综合框架：机制因果链、认知/控制/证据三平面、决策载体、分级约束、个人经验到团队公共资产的晋升与治理。形成日期 2026-07-15。 |
| Agent harness software design principles | ./software-design-principles-in-agent-harnesses.md | 本地分析模型：可组合性、关注点分离、单一职责、开闭、依赖倒置、事件驱动、显式状态、最小权限、可观测性优先。 |
| Agentic Loop Java backend practice | ./agentic-loop-java-backend-practice.md | 本地实践模型：Agentic Loop 的机制、最佳实践与 Java 后端日常工作流。 |
| Four-layer harness architecture | ./four-layer-harness-architecture.md | 本地工作模型：记忆层、扩展层、集成层、编程层。 |
| Coding agent memory systems | ./coding-agent-memory-systems.md | 本地综合笔记：Claude Code 五层记忆体系、`CLAUDE.md` 写作方法、团队分歧分层、条件化规则，以及 Codex、LangGraph、AutoGen、Cursor 记忆设计对照。 |
| Codex Skills design guide | ./codex-skills-design-guide.md | 本地综合笔记：Codex Skills 的触发机制、渐进式披露、`SKILL.md` 路由器定位、references/scripts/assets 分层、权限边界、动态上下文和设计模式。 |
| Delegated thinking with subagents | ./delegated-thinking-with-subagents.md | 本地综合笔记：子智能体预加载 Skill、Skill 派生子智能体、委派模板、常见委派类型、主智能体责任边界和现代 AI 工程设计模式。 |
| Claude Code and Codex hook lifecycle | ./claude-code-codex-hook-lifecycle.md | 本地对比：两者公开 hook 事件矩阵、同名事件语义、handler 能力、治理用途与安全边界；核验日期 2026-07-12。 |
| Claude Code hook output protocol | ./claude-code-hook-output-protocol.md | 本地协议说明：hook transport、exit code、通用 JSON、顶层 decision、`hookSpecificOutput`、字段路由、事件 schema、常见错误与调试。核验日期 2026-07-12。 |
| Claude Code hooks engineering practice | ../experiments/2026-07-12-claude-code-hooks-engineering/README.md | 可运行探针：安全防护、代码质量自动化、子智能体精确上下文管理；13 个 fixture cases，Python 标准库实现。实验日期 2026-07-12。 |
| Claude Code hooks execution foundation | ./claude-code-hooks-execution-foundation.md | 本次会话汇总主文档：生命周期、输出协议、三类工程实践，以及从软提示到 harness 内硬约束、capability boundary 和外部治理门禁的分层方法。官方契约核验日期 2026-07-13。 |
| Codex Skills | https://developers.openai.com/codex/skills | Skills 是 `SKILL.md` 加可选 references/scripts/assets 的可复用工作流；覆盖显式/隐式触发、`allow_implicit_invocation`、存放位置和 best practices。 |
| Codex Customization | https://developers.openai.com/codex/concepts/customization | Codex 定制层：`AGENTS.md`、memories、Skills、MCP、subagents 的边界与组合方式。 |
| Codex agent approvals and security | https://developers.openai.com/codex/agent-approvals-security | Codex sandbox、approval policy、network access、危险操作审批和运行时安全边界。 |
| Codex hooks | https://developers.openai.com/codex/hooks | Codex release behavior reference；当前列出 10 个 hook 事件、command handler、trust review、输入输出与尚未实现/未完整覆盖的能力。2026-07-13 复核。 |
| Claude Code memory | https://code.claude.com/docs/en/memory | `CLAUDE.md`、auto memory、加载顺序、imports，以及 memory-as-context 区分。 |
| Claude Code hooks | https://code.claude.com/docs/en/hooks | 当前列出 30 个 lifecycle hook 事件，覆盖 session、turn、tool、subagent/task/team、compaction、runtime、worktree 和 MCP elicitation；含 command、HTTP、MCP tool、prompt、agent handlers。2026-07-13 复核。 |
| Claude Code hooks guide | https://code.claude.com/docs/en/hooks-guide | Hook 自动化示例、exit code/structured output、matcher、并发和故障排查。2026-07-13 复核。 |
| Claude Code settings | https://code.claude.com/docs/en/settings | Settings scopes、permissions、managed policy、sandbox、hooks、MCP 和 tool behavior。 |
| Claude Code permissions | https://code.claude.com/docs/en/permissions | Permission rules、allow/ask/deny、工具访问控制，以及与 sandboxing 的互补关系。 |
| Claude Code sandbox environments | https://code.claude.com/docs/en/sandbox-environments | Sandboxed Bash、sandbox runtime、dev container、custom container、VM 和 Claude Code on the web 的隔离边界。 |
| Claude Code Bash sandboxing | https://code.claude.com/docs/en/sandboxing | Bash sandbox 模式、auto-allow、filesystem/network 约束、unsandboxed command 处理。 |
| Claude Code MCP | https://code.claude.com/docs/en/mcp | 外部工具和数据集成。 |
| Cursor rules | https://cursor.com/docs/rules.md | Project、user 和 team rules；`AGENTS.md`；rule activation 和 precedence。 |
| Cursor run modes | https://cursor.com/docs/agent/security/run-modes.md | Auto-review、Allowlist、Run Everything、sandboxing、`permissions.json` 和 `sandbox.json`。 |
| Cursor MCP | https://cursor.com/docs/mcp.md | MCP transports、tools、resources、apps、approval、enterprise controls 和 security notes。 |

## Spec-driven workflow 与 Plugins

| 主题 | 来源 | 说明 |
| --- | --- | --- |
| 长期演进复杂多服务系统中的 Harness 工程实践 | ./harness-engineering-practice-for-evolving-multiservice-systems.md | 本地综合报告：成本、调试、安全、规模、指令、协作六维实践；边界假设、跨服务变更控制面；OpenSpec + Compound Engineering + grill-me 组合与 2026-07 plugin 建议。外部事实核验日期 2026-07-15。 |
| OpenSpec | https://github.com/Fission-AI/OpenSpec | Spec-driven development；`specs/` 当前事实、`changes/` 拟议 delta、archive 合并。核验版本 `v1.6.0`，发布于 2026-07-10。 |
| OpenSpec Core Concepts | https://github.com/Fission-AI/OpenSpec/blob/main/docs/overview.md | Specs、changes、delta specs、artifact dependency 和 archive 的官方模型。2026-07-15 复核。 |
| OpenSpec Existing Projects | https://github.com/Fission-AI/OpenSpec/blob/main/docs/existing-projects.md | Brownfield-first：按实际变更逐步积累规格，不要求先完整记录整个旧系统。2026-07-15 复核。 |
| OpenSpec Stores beta | https://github.com/Fission-AI/OpenSpec/blob/main/docs/stores-beta/user-guide.md | 跨 repo planning store、read-only references、worksets；官方明确为 beta，命令、flag、文件格式和 JSON 可能变化。2026-07-15 复核。 |
| Compound Engineering | https://github.com/EveryInc/compound-engineering-plugin | Plan/work/review/compound 工作流；核验 release `compound-engineering-v3.19.0`（2026-07-08），提交 `1756c0b9f3cf94493f287ea29ae766ad668fb7cf`。 |
| Compound Engineering philosophy | https://every.to/guides/compound-engineering | 官方理念与 Plan → Work → Review → Compound 循环。2026-07-15 复核。 |
| grill-me plugin | https://github.com/alirezarezvani/claude-skills/tree/main/engineering/grill-me | 逐问题、深度优先、codebase-first 的计划质询插件；核验 plugin `v2.9.0`，仓库提交 `84dc5a4f6ab93df5195805010572d7d0f874dadb`（2026-07-14）。 |
| grill-me original skill | https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me | `alirezarezvani/claude-skills` manifest 声明的 MIT 派生来源。2026-07-15 复核。 |
| Claude Code Plugins | https://code.claude.com/docs/en/plugins | Plugin 适用范围、Skill/agent/hook/MCP/LSP/monitor 结构、测试和版本管理。2026-07-15 复核。 |
| Anthropic official plugin directory | https://github.com/anthropics/claude-plugins-official | Claude Code 官方管理目录；快照提交 `7b8dfeb2d02727ff17b2437c7a00def0cf069972`（2026-07-14）。目录明确要求安装者自行信任审查插件。 |
| Codex Plugins | https://learn.chatgpt.com/docs/plugins | Codex/ChatGPT plugin 的 Skills、Apps、MCP、Browser extensions、Hooks、scheduled templates、权限与卸载边界。2026-07-15 复核。 |
| Codex Security plugin | https://learn.chatgpt.com/docs/security/plugin | 授权代码的本地安全扫描、finding evidence 和可导出的结构化结果。2026-07-15 复核。 |
| Trail of Bits Skills | https://github.com/trailofbits/skills | 安全研究、diff review、static analysis、supply-chain、property-based testing 等按需插件；快照提交 `cfe5d7b1619e47fb5b38b7e2561dad7e5f1e89af`（2026-06-30），无 GitHub release。 |
| OpenTelemetry traces | https://opentelemetry.io/docs/concepts/signals/traces/ | 跨服务 trace、span、context propagation、link 和 attribute。2026-07-15 复核。 |
| OpenTelemetry context propagation | https://opentelemetry.io/docs/concepts/context-propagation/ | 跨服务信号关联及外部传播、Baggage 的安全注意事项。2026-07-15 复核。 |
| Pact contract testing | https://docs.pact.io/ | Consumer/provider contract testing 工作模型。2026-07-15 复核。 |

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
