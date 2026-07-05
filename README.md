# AI Agent Harness 实验室

这个 workspace 是一个面向当前有效 AI agent harness 的实践探索基地。

目标不是收集所有框架，而是建立一种可重复的方法：比较 harness 设计、运行小型实验、保留证据，并把经验转化为可长期使用的工程选择。

## 工作模型

把这个仓库当作持续演进的实验室：

1. 在 `docs/radar.md` 跟踪当前格局。
2. 在 `docs/harness-principles.md` 记录 harness 设计原则。
3. 在 `docs/source-map.md` 维护来源链接和新鲜度说明。
4. 将可运行实验放在 `experiments/` 下。
5. 将评测任务、评分量规、日志和分析放在 `evals/` 下。
6. 将重大决策以 ADR 形式记录在 `adr/` 下。

## 当前重点

初始比较轴包括：

- 运行时与编排：持久执行、状态、重试、中断、human-in-the-loop。
- 工具与环境：文件系统、shell、浏览器、MCP、沙箱、权限边界。
- 记忆与上下文：短期状态、持久会话、检索、压缩。
- 可观测性：trace、日志、span 元数据、可重放 transcript。
- 评测：任务定义、评分器、成本、延迟、通过率、失败归因。
- 生产控制：guardrail、审批、密钥、部署形态、回滚。

## 仓库布局

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

## 基线规则

任何声称某项内容是“latest”“best”或“production-ready”的判断，都必须附带：

- 检查日期。
- 来源 URL。
- 可用时提供版本或提交。
- 一个小型本地复现，或明确说明为什么没有复现。
- 用于判断它的评测标准。
