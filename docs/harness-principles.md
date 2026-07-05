# Harness 原则

检查日期：2026-07-05 Asia/Shanghai

## 定义

AI agent harness 是围绕模型驱动 agent 的运行时基底。它控制 agent 如何接收任务、观察状态、选择上下文、调用工具、更新记忆、处理错误、引入人工、验证工作并记录证据。

## 好的 Harness 必须明确什么

- 任务契约：目标、约束、输入、预期 artifact、完成标准。
- 状态契约：哪些内容是临时的、持久化的、可恢复的、可重放的。
- 工具契约：可用工具、权限、schema、副作用、审批规则。
- 上下文契约：如何选择、压缩和刷新上下文。
- 验证契约：测试、评分器、不变量、人工审查步骤。
- 证据契约：trace、日志、patch、截图、成本和最终报告。
- 干预契约：人工何时可以审批、重定向、中断或恢复。

## 软件设计原则

详细对比见 [Agent Harness 中的软件设计原则](./software-design-principles-in-agent-harnesses.md)。在本仓库中，后续 harness 设计和评测默认使用这些原则作为检查表：

| 原则 | 对 harness 的要求 |
| --- | --- |
| 可组合性 | 模型、指令、工具、状态、策略、验证、记忆、子 agent 和外部集成可通过稳定契约组合。 |
| 关注点分离 | 上下文选择、工具执行、权限控制、状态持久化、验证、观测、人工干预分层治理。 |
| 单一职责原则 | 指令、工具、状态、权限、编排、观测分别有边界。 |
| 开闭原则 | 新能力通过 MCP、plugin、skill、hook、node、rule 等扩展点接入。 |
| 依赖倒置 | 高层 agent loop 面向 tool/model/runtime/policy 抽象，而不是绑定低层实现。 |
| 观察者 / 事件驱动 | 工具调用、权限请求、状态变化和任务停止等生命周期事件可被订阅和治理。 |
| 显式状态管理 | session、thread、checkpoint、memory、artifact 和验证证据可区分、可恢复。 |
| 最小权限原则 | 默认最小工具、文件、网络和外部系统访问；高风险副作用需要审批。 |
| 可观测性优先 | 运行过程保留 trace、日志、diff、测试输出、成本、延迟和失败归因。 |

## 反模式

- 把 prompt 当作整个 harness。
- 在未固定任务、模型、工具访问和预算的情况下比较 agent。
- 统计成功率却不保留 transcript 和验证证据。
- 让 agent 在工具范围很宽且权限不清晰的情况下运行。
- 在单 agent 循环尚不可度量之前就加入多 agent 编排。
- 把模型自评作为唯一评分器。

## 最小可用 Harness

用于本地实验的第一个有用 harness 需要：

- 结构化任务输入。
- 有边界的 agent 循环。
- 工具注册表。
- workspace 隔离方案。
- Trace log。
- 确定性 verifier。
- 成本和延迟采集。
- 最终 artifact bundle。

## 成熟度阶梯

| 等级 | 描述 | 证据 |
| --- | --- | --- |
| H0 | Prompt 加人工工具使用。 | 只有最终答案。 |
| H1 | 带显式工具和限制的脚本化循环。 | Transcript 和最终 artifact。 |
| H2 | 带 verification 和 failure attribution 的仪表化循环。 | Trace、verifier 输出、成本、失败类别。 |
| H3 | 带 persistence、approvals、rollback 和 eval gates 的生产风格 harness。 | 可重放运行、policy logs、eval history、deployment controls。 |
