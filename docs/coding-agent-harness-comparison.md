# Coding Agent Harness 比较

检查日期：2026-07-12 Asia/Shanghai

本文将 Claude Code、Cursor 和 Codex 作为 coding-agent harness 进行比较。比较围绕五个问题：

1. 上下文如何进入 agent。
2. 工具如何暴露和使用。
3. 行动如何受到约束。
4. 结果如何被验证。
5. 经验如何跨 session 延续。

## 核心模型

使用这个工作定义：

```text
Agent = Model + Harness
```

模型提供推理、语言、规划和工具调用意图。Harness 提供围绕模型的运行时：上下文组装、工具执行、权限策略、沙箱、session 管理、验证、记忆、集成、日志、diff 和 artifact。

Cursor 最直接地说明了这一点：它的 Agent 由 instructions、tools 和所选模型构成。Claude Code 和 Codex 通过 memory、tools、permissions、hooks、sessions 和 integrations 暴露出同样的实践结构。

## 摘要

| 维度 | Claude Code | Cursor | Codex |
| --- | --- | --- | --- |
| 上下文入口 | `CLAUDE.md`、auto memory、session context、文件读取、MCP、IDE/CLI/Desktop/Web surfaces。 | Prompt、打开或选中的编辑器文件、codebase index、Rules、`AGENTS.md`、MCP、Browser screenshots。 | Prompt、`@` 文件和图片、IDE 打开的文件和选择、`AGENTS.md`、工具输出、MCP、skills、plugins、memories、Chronicle。 |
| 工具使用 | 读取/编辑/搜索、Bash 或 PowerShell、MCP、hooks、subagents、Agent SDK。 | Semantic search、文件搜索/读取/编辑、terminal、web、Browser、MCP、image generation。 | 文件读写、shell、patching、web、MCP、plugins、skills、subagents，以及根据界面而定的 Browser 或 Computer Use。 |
| 行动约束 | Permission rules、settings、managed policy、sandbox、`PreToolUse` hooks。 | Run Modes、Auto-review classifier、allowlist、`permissions.json`、`sandbox.json`、team controls。 | Approval policy、sandbox mode 或 permission profile、文件系统和网络规则、hooks、managed requirements、继承的 subagent policy。 |
| 验证 | 用户指定的测试和命令；hooks 可在工具使用后或停止前验证；agent hooks 可检查文件并运行测试。 | Terminal checks、Browser UI verification、Agent Review、用于回滚的 checkpoints。 | Repro steps、tests、lint、pre-commit checks、`/review`、Codex Security validation、用于 workflow checks 的 hooks 和 skills。 |
| 跨 session 经验 | 人工编写的 `CLAUDE.md` 加 auto memory；settings、skills、hooks、MCP config。 | Project/User/Team Rules、`AGENTS.md`、MCP config、session 内 checkpoints。 | `AGENTS.md`、opt-in memories、threads 和 resume、compaction、skills、plugins、config、Chronicle。 |

## Claude Code

Claude Code 是 memory-first。每个 session 都从新的上下文窗口开始，随后持久上下文主要通过 `CLAUDE.md` 文件和 auto memory 进入。

`CLAUDE.md` 文件可以存在于 organization、user、project、local 和嵌套目录范围。工作目录之上的文件会在启动时加载；子目录文件会在 Claude 读取该目录中的文件时按需加载。`CLAUDE.md` 可以用 `@path` 语法导入其他文件。

Auto memory 允许 Claude 根据纠正和偏好写入笔记。`CLAUDE.md` 和 auto memory 都是上下文，而不是强制配置。若要机械地阻止某个行动，应使用 permissions 或 hooks。

工具层包括文件读取和编辑、搜索、shell 命令、MCP tools、subagents、hooks、background agents 和 Agent SDK workflows。MCP 是主要的外部集成机制。

约束通过 settings、permission rules、sandboxing、managed policy 和 lifecycle hooks 分层施加。`PreToolUse` hooks 可以在工具调用执行前拒绝它。`Stop` hooks 可以要求 Claude 在结束前完成额外工作。Agent hooks 可以启动一个带工具的 subagent 来检查文件或运行测试。Claude Code 与 Codex 的事件和控制能力详见[独立生命周期对比](./claude-code-codex-hook-lifecycle.md)。

Claude Code 最强的差异点是 persistent memory 与丰富 hook lifecycle 的组合。

## Cursor

Cursor 是 IDE-context-first。上下文通过 prompt text、打开文件、选中文本、codebase indexing、file search、Rules、`AGENTS.md`、MCP 和 Browser state 进入。

Cursor Rules 是持久的 prompt-level context。Project Rules 以 `.mdc` 文件形式位于 `.cursor/rules`。Rules 可以始终生效、对匹配文件生效、被手动提及，或由 agent 根据描述选择。User Rules 跨项目生效。Team Rules 可以集中管理，并可选择强制执行。

Cursor 也支持项目根目录和子目录中的 `AGENTS.md`。嵌套文件会与父级文件合并，更具体的说明优先。

工具层包括 semantic search、文件和文件夹搜索、web search、rule fetching、文件读取、文件编辑、terminal execution、Browser control、MCP、image generation 和 clarification questions。

Cursor 的主要本地自主性控制是 Run Modes：

- Auto-review：allowlisted 调用会立即运行；其他 shell 命令在可能时使用 sandbox；更高风险调用通过 classifier。
- Allowlist：allowlisted actions 无需审批即可运行，对支持的 shell 命令可选择启用 sandboxing。
- Run Everything：所有工具调用自动运行。

`permissions.json` 引导 Auto-review 决策。`sandbox.json` 控制 sandbox 可达范围，包括网络域名和额外可读或可写路径。Cursor 明确指出 Auto-review 不是安全边界；对于 terminal commands，sandboxing 是更强的运行时边界。

验证绑定在 IDE 和 browser loop 上：terminal checks、Browser screenshots and interaction、Agent Review 和 checkpoints。Checkpoints 是本地回滚辅助，不是永久版本控制或正确性证明。

## Codex

Codex 是 repo-instruction and policy-first。上下文通过 prompts、`@` 提及的文件和图片、IDE 打开的文件和选区、`AGENTS.md`、发现的文件内容、工具输出、MCP、skills、plugins、memories 和 Chronicle 进入。

Codex threads 是包含 prompts、模型输出和工具调用的 sessions。Threads 可以恢复。长时间运行的工作可以通过 automatic compaction 继续：Codex 会总结相关上下文，并丢弃相关性较低的细节。

工具层是一个 model-tool loop：模型提出行动，harness 执行文件读取、编辑、shell 命令、patching、web access、MCP calls 或其他界面特定工具。Codex 可以通过 skills、plugins、MCP servers、app connectors、subagents 和 custom agents 扩展。

Codex 拥有最显式的 sandbox 和 approval 模型：

- Approval policy 控制 Codex 何时必须在行动前询问。
- Sandbox mode 或 permission profiles 控制文件系统和网络访问。
- 默认本地行为会关闭网络访问，并将写入限制在 workspace 内。
- 文件和网络规则可以定义精确的 read、write、deny 和 domain policy。
- Hooks 可以围绕当前公开的 10 个 lifecycle events 运行，但 command handler 是唯一实际执行的类型，且工具拦截路径尚不完整；因此它是 guardrail，不是 sandbox 的替代品。
- Managed requirements 可以限制 sandbox modes、approvals、web search modes、hooks、MCP 等。
- 除非显式配置，subagents 会继承 sandbox policy。

验证围绕 task contracts 构建：复现问题、添加或更新测试、运行 lint/type checks/focused suites、确认行为并审查 diffs。Codex Security 是一个专门示例：它在 sandbox 中运行 validation，并保留 commands、exit codes、stdout、stderr、test results、diffs 和 artifacts 作为证据。

跨 session 经验来自 `AGENTS.md`、opt-in memories、thread history、resume、compaction、skills、plugins、config files 和 Chronicle。必需的团队指导应放在 `AGENTS.md` 或已提交文档中；生成的 memory 是有用的召回信息，但不应是规则的唯一来源。

## 比较结论

Claude Code 是 memory-first：当长期项目约定和重复纠正很重要时有用。

Cursor 是 IDE-context-first：当打开文件、选区、codebase index 和 browser verification 应主导循环时有用。

Codex 是 policy-first：当 task contracts、repo guidance、sandboxing、approvals、resumable threads 和 auditability 都应显式化时有用。

对于团队关键行为，优先使用已提交的 instruction files 或 managed policy，而不是 generated memory。对于正确性，三者都不提供自动证明：verification 必须被设计进任务或 harness。

## Harness 评测问题

在为某类工作负载采用 harness 前，先使用这些问题：

1. 哪些上下文会自动加载，哪些必须手动附加？
2. 上下文加载能否按路径、文件类型或任务限定范围？
3. 哪些工具可以改变状态？
4. 哪些工具调用需要审批？
5. 是否存在 OS-level sandbox，还是只有 prompt/classifier-level guidance？
6. policy 能否为团队集中强制执行？
7. verification 能否阻止完成？
8. 原始日志、diff、命令输出和 artifact 是否会被保留？
9. 任务能否在中断或 context compaction 后恢复？
10. 什么内容会跨 session 持久保存，由谁控制？

## 来源

- Claude Code overview：https://code.claude.com/docs/en/overview
- Claude Code memory：https://code.claude.com/docs/en/memory
- Claude Code hooks：https://code.claude.com/docs/en/hooks
- Claude Code settings：https://code.claude.com/docs/en/settings
- Claude Code MCP：https://code.claude.com/docs/en/mcp
- Cursor Agent overview：https://cursor.com/docs/agent/overview.md
- Cursor Rules：https://cursor.com/docs/rules.md
- Cursor Run Modes：https://cursor.com/docs/agent/security/run-modes.md
- Cursor MCP：https://cursor.com/docs/mcp.md
- Codex manual：https://developers.openai.com/codex/codex-manual.md
