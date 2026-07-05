# AI Agent Harness 雷达

检查日期：2026-07-05 Asia/Shanghai

这份雷达刻意保持保守。它列出值得测试的工具和想法，而不是背书。

## 近期候选

| 领域 | 候选项 | 重要性 | 第一个探针 |
| --- | --- | --- | --- |
| 托管 agent 运行时 | OpenAI Agents SDK | 为 agent、handoff、guardrail、session、tracing、MCP 和 sandbox agent 提供轻量级原语。 | 构建一个会产出文件的 agent，带 tracing 和一个简单 guardrail。 |
| 有状态编排 | LangGraph | 面向长时间运行、有状态 agent 的低层编排运行时，支持持久执行、streaming、human-in-the-loop 和 persistence。 | 构建一个带 checkpointing 和 interruption 的双节点 graph。 |
| 多 agent 系统 | AutoGen | AgentChat 用于对话式 agent，Core 用于事件驱动的多 agent 系统。 | 构建一个有轮次上限的双 agent reviewer/implementer 循环。 |
| 评测框架 | Inspect AI | 包含 dataset、solver、scorer、agent tool、sandboxing、log 和 external-agent bridge 的评测任务框架。 | 创建一个带确定性评分的小型代码编辑 eval。 |
| 编码基准契约 | SWE-bench | 真实世界 issue 修复基准形态；有助于理解 patch 契约和评分纪律。 | 实现一个迷你 SWE 风格本地任务，包含 patch 提取和测试。 |

## 研究信号

近期以 harness 为中心的研究，把性能看作 model-harness-environment 系统问题，而不仅是模型能力问题。值得跟踪的维度包括：

- 任务规格质量。
- 上下文选择。
- 工具访问与权限。
- 项目记忆。
- 任务状态。
- 可观测性。
- 失败归因。
- 验证。
- 熵与非确定性审计。
- 干预记录。

## 评测轴

除非任务明显需要不同维度，否则跨实验使用相同评测轴：

| 评测轴 | 度量方式 |
| --- | --- |
| 成功 | 通过/失败，加任务特定分数。 |
| 成本 | 模型 token、API 成本估算、墙钟时间、重试次数。 |
| 可靠性 | 多次重复运行之间的方差。 |
| 可调试性 | trace 完整性、可重放性、失败归因质量。 |
| 控制 | 人工审批 hook、权限边界、中断/恢复行为。 |
| 可移植性 | 模型/供应商耦合、框架耦合、环境假设。 |
| 可维护性 | 胶水代码量、状态模型清晰度、可测试性。 |

## 初始假设

对于软件工程 agent，一旦任务需要真实工具、状态或验证，harness 与模型同样重要。因此，第一批有用实验应该比较：

1. 在可行时，用同一模型在不同 harness 上执行同一任务。
2. 用同一 harness 搭配不同模型。
3. 最小循环与带 tracing、verification 和 failure attribution 的仪表化循环。
