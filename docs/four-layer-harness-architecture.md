# 四层 Harness 架构模型

检查日期：2026-07-05 Asia/Shanghai

本文把 coding agent harness 拆成四层：

1. 记忆层
2. 扩展层
3. 集成层
4. 编程层

这不是某一家产品的官方架构命名，而是本 workspace 用来分析 Claude Code、Cursor、Codex 以及后续 agent harness 的工作模型。

## 总模型

```text
Agent = Model + Harness
Harness = 记忆层 + 扩展层 + 集成层 + 编程层 + 横切控制
```

模型负责推理、语言、规划和工具调用意图。Harness 负责让这些意图进入真实软件工程环境：装配上下文、暴露工具、执行动作、限制权限、验证结果、保留证据，并把可复用经验带入下一次任务。

四层不是严格的调用栈，而是四类职责。一个功能可能横跨多层。例如 MCP 既属于集成层，也会把外部数据变成上下文；hooks 属于扩展层，但常用于约束动作或验证结果。

## 四层定义

| 层 | 解决的问题 | 典型机制 | 产物 |
| --- | --- | --- | --- |
| 记忆层 | Agent 带着什么长期背景进入任务？ | `CLAUDE.md`、`AGENTS.md`、Rules、memories、session history、compaction。 | 持久指令、偏好、项目知识、历史摘要。 |
| 扩展层 | Agent 如何获得额外能力和可复用工作流？ | Skills、plugins、subagents、hooks、custom agents、slash commands。 | 可复用流程、专门 agent、生命周期自动化。 |
| 集成层 | Agent 如何连接外部系统和运行环境？ | MCP、IDE、CLI、Browser、GitHub、Slack、Jira、CI、cloud workers。 | 外部工具、数据源、授权动作、环境入口。 |
| 编程层 | Agent 如何实际完成代码任务？ | Read/search/edit、shell、patch、test、review、browser verification、git。 | 代码变更、测试结果、diff、artifact、报告。 |

## 记忆层

记忆层决定 agent 在任务开始时和任务过程中拥有哪些长期上下文。

它包含三类内容：

- 人写的持久指令：`CLAUDE.md`、`AGENTS.md`、Cursor Rules、项目文档。
- 系统生成的记忆：Claude Code auto memory、Codex memories、Chronicle 等。
- 会话状态：thread/session history、任务计划、工具输出摘要、context compaction。

记忆层的核心约束是：记忆通常是上下文，不是强制规则。模型可能忽略、误解或与其他上下文冲突。因此团队关键规则应放在已提交文档、规则文件或 managed policy 中；真正需要阻断的行为应交给权限、sandbox 或 hook。

好的记忆层应该回答：

1. 哪些内容每次自动加载？
2. 哪些内容按路径、文件或任务按需加载？
3. 哪些内容由人维护，哪些由系统生成？
4. 是否有大小限制、优先级和冲突规则？
5. 记忆是否可审查、可删除、可迁移？

## 扩展层

扩展层决定 agent 如何获得超出默认能力的流程、角色和自动化。

典型机制包括：

- Skills：把某类任务的步骤、参考资料、脚本和约束打包。
- Plugins：把 skills、MCP、hooks、commands、assets 和配置打包分发。
- Subagents/custom agents：用独立上下文或不同工具面处理子任务。
- Hooks：在生命周期事件上执行确定性逻辑或额外判断。
- Slash commands/custom prompts：把重复提示变成入口。

扩展层的关键价值是减少重复提示，并让成功流程可复用。它的风险是能力蔓延：过多扩展会让上下文、权限和调试路径变复杂。

好的扩展层应该回答：

1. 什么时候加载扩展？
2. 扩展是否能修改文件、运行命令或调用外部服务？
3. 扩展是否被版本控制、签名、审核或 managed policy 管理？
4. Subagent 是否继承主 agent 的 sandbox 和审批策略？
5. Hook 是阻塞式、异步式，还是只记录观察？

## 集成层

集成层决定 agent 能进入哪些外部系统，以及这些系统如何变成上下文或工具。

典型入口包括：

- MCP servers：把外部工具、数据源、resources、prompts、apps 暴露给 agent。
- IDE：打开文件、选区、诊断、代码索引、diff review。
- CLI：本地 shell、git、测试命令、脚本环境。
- Browser：截图、交互、UI 验证、网页调试。
- Cloud/CI/GitHub/Slack/Jira：远程任务、PR review、issue triage、通知和审批。

集成层的核心问题是授权和边界。外部系统通常包含真实数据和真实副作用，所以集成层必须和权限、审批、日志、密钥管理一起设计。

好的集成层应该回答：

1. 外部系统提供的是只读上下文，还是可写动作？
2. 权限来自用户本地凭证、OAuth、服务账号，还是团队策略？
3. 工具调用是否需要审批？
4. 外部输出是否会进入记忆或训练/日志路径？
5. 某个集成失败时是否会隔离失败，还是影响整个 agent loop？

## 编程层

编程层是 agent 真正完成软件工程任务的地方。

它包含基本 coding loop：

```text
理解任务
  -> 收集上下文
  -> 规划
  -> 读/搜/改/运行命令
  -> 观察结果
  -> 修正
  -> 验证
  -> 汇报
```

典型能力包括：

- 文件读取、代码搜索、语义搜索。
- 文件编辑、patch 生成、重构。
- Shell 命令、测试、lint、typecheck、build。
- Git diff、commit、PR review。
- Browser/UI 验证。
- Artifact 生成和结果报告。

编程层的质量取决于任务契约和验证契约。如果用户只给模糊目标，agent 可能完成一个看似合理但不可验证的结果。好的 harness 应把 done criteria、测试命令、回滚方式和证据保留变成默认工作流。

好的编程层应该回答：

1. 任务完成的可验证标准是什么？
2. 修改前是否建立 checkpoint 或 git baseline？
3. 最小必要测试是什么？
4. 失败时如何归因：上下文错、工具错、权限错、模型判断错，还是环境错？
5. 最终交付物包括哪些证据？

## 横切控制

四层之外，还有一组横切控制贯穿所有层：

- 权限：哪些文件、命令、网络、MCP 工具可用。
- 沙箱：工具执行是否有 OS-level 边界。
- 审批：哪些动作必须问人。
- 观测：trace、log、tool transcript、cost、latency。
- 恢复：resume、compaction、checkpoint、rollback。
- 策略：team/enterprise managed policy。
- 安全：secret handling、prompt injection 防护、外部内容隔离。

横切控制决定 harness 是否可用于真实工程环境。没有这些控制，四层只是一组便利功能；有了这些控制，才可能成为生产级 agent runtime。

## 四层如何协作

一次典型 coding-agent 任务可以这样流动：

```text
用户任务
  -> 记忆层加载项目规则、历史偏好、会话上下文
  -> 编程层开始 agent loop，读取代码并形成计划
  -> 集成层提供外部系统数据或工具，如 MCP、IDE、Browser、CI
  -> 扩展层按需注入 skill、subagent、hook 或 plugin
  -> 编程层执行修改、运行命令、收集结果
  -> 横切控制决定哪些动作自动运行、哪些需要审批、哪些被阻断
  -> 编程层完成验证并生成报告
  -> 记忆层或扩展层沉淀可复用经验
```

层之间的关键依赖：

- 记忆层影响编程层的判断，但不应单独承担强制约束。
- 扩展层复用经验，但需要集成层提供外部能力，且需要横切控制限制副作用。
- 集成层扩大可见性和行动范围，也扩大风险面。
- 编程层产出实际变更，是验证和证据保留的主要来源。

## 与三类产品的映射

| 产品 | 记忆层重点 | 扩展层重点 | 集成层重点 | 编程层重点 |
| --- | --- | --- | --- | --- |
| Claude Code | `CLAUDE.md`、auto memory、session/compaction。 | Hooks、skills、subagents、Agent SDK。 | MCP、CLI、IDE、Desktop、Web、channels。 | Shell-first 本地工程循环，hook 驱动验证和自动化。 |
| Cursor | Rules、`AGENTS.md`、打开文件、选区、codebase index。 | Rules、MCP plugins、agent modes。 | IDE、Browser、MCP、terminal、Git providers。 | IDE-native 编辑、搜索、browser verification、checkpoints。 |
| Codex | `AGENTS.md`、threads、memories、Chronicle、compaction。 | Skills、plugins、hooks、subagents/custom agents。 | MCP、app connectors、CLI、IDE、cloud、Browser/Computer Use。 | Policy-aware coding loop、sandbox/approval、review、evidence capture。 |

## 设计原则

1. 先定义编程层的任务契约，再选择扩展层。
2. 把团队关键规则放进持久指令或 managed policy，不依赖 generated memory。
3. 给集成层最小必要权限，默认把外部内容视为不可信。
4. 能用确定性 verifier 的地方，不用模型自评作为唯一判断。
5. 每个可写工具都要有对应的约束、日志和回滚方案。
6. Subagent 增加并行度，也增加成本、上下文污染和调试难度。
7. Hook 适合机械约束和生命周期自动化，但要避免隐藏复杂副作用。
8. Memory 应可审查、可删除、可迁移，并有明确适用范围。

## 实验检查表

在本 workspace 中评估一个 harness 时，按四层记录：

| 层 | 必填记录 |
| --- | --- |
| 记忆层 | 自动加载的文件、生成记忆机制、context 限制、冲突规则。 |
| 扩展层 | 使用的 skills/plugins/hooks/subagents、触发条件、权限范围。 |
| 集成层 | MCP/IDE/CLI/Browser/CI 等连接方式、凭证来源、审批要求。 |
| 编程层 | 任务、工具调用、修改文件、验证命令、最终 artifact。 |
| 横切控制 | Sandbox、approval、logs、rollback、cost、failure attribution。 |

## 相关文档

- [Harness 原则](./harness-principles.md)
- [Coding Agent Harness 比较](./coding-agent-harness-comparison.md)
- [来源地图](./source-map.md)
