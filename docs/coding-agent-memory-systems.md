# Coding Agent 记忆体系与 `CLAUDE.md` 写作方法

检查日期：2026-07-06 Asia/Shanghai

本文整理本次 session 中关于 coding agent 记忆体系的讨论。重点是 Claude Code 的五层记忆体系、`CLAUDE.md` 的写作方法、团队协作中的分层判断，以及 Codex、LangGraph、AutoGen、Cursor 的对照。

## 核心结论

Claude Code 的“五层记忆体系”可以理解为 4 层人工维护的 `CLAUDE.md` 指导，加 1 层自动沉淀的 auto memory：

1. 组织层 managed `CLAUDE.md`
2. 用户层 `~/.claude/CLAUDE.md`
3. 项目层 `CLAUDE.md` 或 `.claude/CLAUDE.md`
4. 本地层 `CLAUDE.local.md`
5. auto memory

它们共同解决的问题不是“让模型永久记住一切”，而是把跨 session 仍然有价值的上下文，以不同作用域、不同维护责任、不同风险等级组织起来。

关键边界是：`CLAUDE.md` 和 auto memory 是 context，不是硬约束。真正的强制控制应由 settings、permissions、sandbox、hooks、CI、linter、formatter 等机制承担。

## AI 为什么需要记忆

LLM 调用本身没有稳定的跨 session 工作状态。Coding agent 一旦进入真实工程环境，就会遇到以下问题：

- 重复解释成本：构建命令、测试命令、目录约定不应每次重说。
- 一致性：同一 repo 的架构边界、代码风格、PR 标准需要跨任务稳定。
- 工作连续性：长任务、失败实验、调试发现需要可恢复。
- 个性化：不同开发者的沟通风格、验证习惯、工具偏好不同。
- 局部性：monorepo 中不同目录、语言、团队的规则不同。

因此，记忆体系本质上是 agent harness 的上下文管理层：它决定哪些信息进入模型上下文、什么时候进入、由谁维护、能否被覆盖。

## Claude Code 五层记忆体系

| 层级 | 典型位置 | 适合内容 | 不适合内容 |
| --- | --- | --- | --- |
| 组织层 | managed policy `CLAUDE.md` | 公司级安全、合规、数据处理、代码审查底线 | 个人偏好、项目细节 |
| 用户层 | `~/.claude/CLAUDE.md` | 个人沟通风格、默认工作协议、常用偏好 | 团队必须遵守的工程规则 |
| 项目层 | repo `CLAUDE.md` 或 `.claude/CLAUDE.md` | 项目结构、构建测试命令、架构边界、团队共识 | 临时任务背景、本机私有信息 |
| 本地层 | `CLAUDE.local.md` | 本机端口、私有测试账号、个人本地调试流程 | 应提交给团队的公共规则 |
| auto memory | Claude 自动维护的 per-repo memory | 反复纠正后形成的经验、偏好、调试发现 | 必须稳定遵守的团队契约 |

这套体系的价值在于分离责任：

- 组织层回答“所有人都必须遵守什么”。
- 用户层回答“我希望 agent 如何和我协作”。
- 项目层回答“这个 repo 如何正确工作”。
- 本地层回答“我这台机器如何跑起来”。
- auto memory 回答“过去交互中学到了什么”。

## 冲突处理

Claude Code 的记忆冲突不应按程序配置的“确定性覆盖”理解。因为 `CLAUDE.md` 和 auto memory 最终都会进入模型上下文，冲突时模型可能综合判断，也可能选择其中一条。

工程上应采用以下规则避免冲突：

- 硬约束不要只写在 `CLAUDE.md`，应放 settings、permissions、hooks、CI 或 linter。
- 团队契约放项目层，个人偏好放用户层，本机事实放本地层。
- 子系统规则放子目录 `CLAUDE.md` 或 path-scoped rules，不放根文件。
- 过期或互相矛盾的规则要删除，不要保留“历史痕迹”污染上下文。
- 如果同一条规则需要被 code review 执行，它应进入项目层；如果只是个人协作习惯，它不应进入项目层。

一个实用判断：

- 会影响别人 review 我的代码吗？会，倾向项目层。
- 换一个开发者也必须遵守吗？是，倾向项目层或组织层。
- 只是我和 Claude 的协作方式吗？是，放用户层。
- 只是我本机环境吗？是，放本地层。

## `CLAUDE.md` 的“少即是多”

“少即是多”不是信息越少越好，而是只写每个 session 都值得进入上下文的高信号内容。

`CLAUDE.md` 太长会带来四个问题：

- 占用 context window。
- 稀释真正重要的规则。
- 增加冲突和过期概率。
- 让 Claude 的注意力分散到当前任务无关的信息。

因此，根 `CLAUDE.md` 应像 agent 的开工协议，而不是项目百科。大段背景、低频知识、复杂流程应进入普通文档、子目录规则、path-scoped rules 或 skill。

## `CLAUDE.md` 写作的三问框架

### Why：为什么要写

先问这条内容解决什么反复发生的问题。

适合写入的 Why：

- Claude 第二次犯了同类错误。
- 你反复在 chat 里解释同一件事。
- code review 反复指出同一类问题。
- 新同事也需要这条上下文才能正确工作。
- 不写会导致错误命令、错误目录、错误架构边界或错误验证方式。

如果 Why 只是“也许有用”，通常不要写进根 `CLAUDE.md`。

### What：到底写什么

写稳定、具体、跨 session 有用的事实和行为规则：

- 项目结构。
- 构建、测试、lint、格式化命令。
- 代码约定。
- 架构边界。
- 工作流。
- 常见陷阱。
- 完成标准。

不要写：

- 临时任务背景。
- 大段架构文档全文。
- 罕见边缘情况。
- 模糊口号。
- 已由工具强制的格式细节。
- 只适用于某个子目录的规则。
- 多步骤复杂流程。

### How：怎么写

写法要短、具体、可验证。

差的写法：

```md
- 保持代码整洁。
- 充分测试。
- 遵守项目架构。
```

好的写法：

```md
- API handlers live in `src/api/handlers/`.
- Do not edit files under `src/generated/`; update the schema and run `make generate`.
- After changing billing logic, run `npm test -- billing`.
```

判断口诀：

- Why 不强，不写。
- What 不稳定，不写。
- How 不具体，重写。

## 值得写入 `CLAUDE.md` 的内容

### 项目结构

```md
## Project Shape

- `src/api/` contains HTTP handlers.
- `src/domain/` contains business logic and must not import web framework code.
- `src/generated/` is generated output and should not be edited directly.
```

### 命令与验证

```md
## Commands

- Run `npm test` for the full test suite.
- Run `npm run lint` before finalizing changes.
- For API-only changes, run `npm test -- api`.
```

### 架构边界

```md
## Architecture Rules

- `src/domain/` must not import from `src/api/` or `src/ui/`.
- API errors must use `AppError` and the shared response formatter.
```

### 工作流

```md
## Workflow

- Before changing behavior, read the closest existing test.
- For behavior changes, add or update a regression test when feasible.
- In final responses, report commands run and checks not run.
```

### 常见陷阱

```md
## Known Pitfalls

- Do not edit `generated/` files directly; update schema files and run `make generate`.
- Payment fixtures in `tests/fixtures/payments/` are shared by integration tests.
```

## 不适合写入根 `CLAUDE.md` 的内容

| 内容 | 更合适的位置 |
| --- | --- |
| 临时任务上下文 | 当前 prompt |
| 长篇架构解释 | `docs/` 或 ADR |
| 目录局部规则 | 子目录 `CLAUDE.md` 或 path-scoped rules |
| 个人回复偏好 | 用户层 `~/.claude/CLAUDE.md` |
| 本机端口和私有账号 | `CLAUDE.local.md` |
| 可机器强制的格式规则 | formatter、linter、CI |
| 复杂可复用流程 | skill |
| 强制禁止命令 | permissions、settings、hooks、sandbox |

## `CLAUDE.md` 写作流程

1. 用 `/init` 或人工梳理生成初稿。
2. 删除泛泛而谈的内容。
3. 把长背景改成“先读哪里”的路由。
4. 把规则改成触发条件和正确动作。
5. 把目录专属规则下沉到子目录或 `.claude/rules/`。
6. 把可强制内容交给 CI、linter、hook 或 permissions。
7. 在真实失败后追加规则，而不是一次性写百科。

推荐最小结构：

```md
# CLAUDE.md

## Project Shape

- `src/api/` contains HTTP handlers.
- `src/domain/` contains business logic and must not import web framework code.

## Commands

- Run `npm test` for the full test suite.
- Run `npm run lint` before finalizing changes.

## Coding Rules

- Do not edit `generated/` files directly.
- API errors must use the shared `AppError` formatter.

## Verification

- For behavior changes, add or update a regression test when feasible.
- In final responses, report commands run and checks not run.
```

## “犯错 -> 纠正 -> 记忆写入 -> 避免犯错”闭环

良性闭环不是让 Claude 自动记住一切，而是把错误分级处理。

1. 观察错误  
   记录 Claude 做错了什么：错命令、错目录、错架构边界、错测试策略。

2. 即时纠正  
   在当前对话中给出具体反馈。例如：

   ```text
   这里不要改 `generated/`，应改 schema 后运行 `make generate`。
   ```

3. 判断是否值得持久化  
   如果只是一次性任务，不写。  
   如果是重复错误、新同事也会踩、code review 也会指出，就写。

4. 选择写入层  
   团队共享规则写项目层。  
   局部目录规则写子目录或 path-scoped rules。  
   个人习惯写用户层。  
   本机事实写本地层。  
   自动发现的经验可进入 auto memory，但重要团队规则应提升到项目层。

5. 压缩成规则  
   不写长故事，写触发条件和正确动作。

   ```md
   - When changing generated API types, edit `schema/*.yaml` and run `make generate`; do not edit `src/generated/` directly.
   ```

6. 验证闭环  
   下次类似任务让 Claude 先说明会遵循哪些项目规则。若仍犯错，说明规则不够具体、scope 放错，或需要 hook/CI 强制。

## 团队协作中的分歧处理

五层记忆体系可以作为团队分歧的分流器。

| 分歧类型 | 应放层级 | 判断标准 |
| --- | --- | --- |
| 安全、合规、数据处理、禁止行为 | 组织层，硬约束放 settings/hooks/permissions | 所有人都必须遵守，不能被个人覆盖 |
| 架构边界、测试命令、代码风格、PR 标准 | 项目层或 path-scoped rules | 团队 review 会据此要求所有人一致 |
| 子系统特有约定 | 子目录 `CLAUDE.md` 或 path-scoped rules | 只影响某个模块、语言、目录或文件类型 |
| 沟通风格、回复详略、个人常用流程 | 用户层 | 只影响个人和 Claude 的协作方式 |
| 本机端口、私有测试账号、个人 sandbox | 本地层 | 和当前项目有关，但不该提交给团队 |
| 自动学到的经验 | auto memory | 可辅助召回，但重要团队规则应提升为项目层 |

项目层只写“团队愿意 code review、CI 或架构决策背书的规则”。

适合项目层：

```md
- Do not edit files under `src/generated/`; update schema files and run `make generate`.
- API handlers must return errors through `AppError` and the shared formatter.
- For billing changes, run `npm test -- billing`.
- `src/domain/` must not import from `src/api/`.
```

适合用户层：

```md
- Prefer concise explanations unless I ask for detail.
- Before making large edits, give me a short plan.
- In final responses, summarize risks first.
```

适合本地层：

```md
- My local API runs on `http://localhost:4310`.
- Use test tenant `dev-yuanxun` for local smoke checks.
- On my machine, Redis runs via Docker Compose profile `local-cache`.
```

团队还没有达成共识的内容，不应直接写成项目层规则。它应该先进入 issue、ADR 或设计讨论；形成决策后，再提炼成短规则。

## 条件化规则体系

条件化规则体系解决的是根 `CLAUDE.md` 过长和注意力分散的问题。

典型失败模式：

- context 变长，token 成本增加。
- 无关规则干扰当前任务。
- monorepo 中其他团队规则污染当前目录。
- 规则越多越容易冲突。
- 长 `CLAUDE.md` 降低遵循率。

条件化规则的思路是：根文件只放通用高频规则，目录或路径相关内容只在相关文件被处理时加载。

这个方案的优势：

- Markdown 可读，便于 review。
- 路径 glob 足够表达大多数 repo 局部性。
- 懒加载减少 context 噪声。
- 团队可以把所有权和目录边界对齐。

需要注意的是，条件化规则仍然是 context routing，不是权限系统。要禁止危险命令或破坏性行为，仍需 settings、permissions、sandbox、hooks 或 CI。

## Claude Code 约束控制面

`CLAUDE.md` 和 auto memory 解决的是“Claude 应该知道什么、倾向怎么做”。如果目标是“Claude 不能做什么、做之前必须确认什么、运行时必须被拦截什么”，就应使用 Claude Code 的约束控制面。

可以把约束体系理解成 5 层：

| 层 | 机制 | 解决的问题 | 强度 |
| --- | --- | --- | --- |
| 1 | `settings.json` | 默认行为、工具模式、环境变量、插件、hooks、sandbox 参数 | 配置层 |
| 2 | permission rules | 哪些工具、命令、文件、域名、MCP、subagent 可用 | 工具授权层 |
| 3 | sandboxing | Bash 及子进程实际能读写什么、能访问哪些网络 | OS 隔离层 |
| 4 | managed policy/settings | 组织级不可覆盖策略 | 管理强制层 |
| 5 | lifecycle hooks | 在运行时按上下文动态拦截、审计、补充判断 | 事件控制层 |

这几层不是互斥关系，而是 defense-in-depth：

- `CLAUDE.md` 管意图。
- settings 管默认配置。
- permission rules 管工具授权。
- sandboxing 管进程边界。
- managed policy 管组织底线。
- lifecycle hooks 管动态上下文判断。

### settings：配置默认行为

`settings.json` 是 Claude Code 的配置机制，分为 Managed、User、Project、Local 等 scope。

常见位置：

- User：`~/.claude/settings.json`
- Project：`.claude/settings.json`
- Local：`.claude/settings.local.json`
- Managed：server-managed、MDM/registry、系统级 `managed-settings.json` 等

优先级从高到低：

1. Managed settings
2. 命令行参数
3. Local project settings
4. Shared project settings
5. User settings

Managed 最高，不能被用户、项目或命令行覆盖。数组类配置如 `permissions.allow`、`sandbox.filesystem.allowWrite` 通常会跨 scope 合并，而不是简单替换。

示例：

```json
{
  "permissions": {
    "defaultMode": "default",
    "deny": ["Read(./.env)", "Read(./secrets/**)"],
    "allow": ["Bash(npm test *)"]
  },
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true
  }
}
```

settings 是“把约束声明在哪里”的容器；真正的权限判断由 permission rules、permission modes、sandbox 和 hooks 执行。

### permission rules：工具调用授权

permission rules 控制 Claude Code 能不能调用某个工具、命令、文件、`WebFetch` 域名、MCP 工具或 subagent。

三类规则：

- `allow`：允许，不再人工确认。
- `ask`：每次要求确认。
- `deny`：禁止。

评估顺序是 `deny -> ask -> allow`。更具体的 allow 不能绕过更宽泛的 deny。

示例：

```json
{
  "permissions": {
    "allow": [
      "Bash(npm test *)",
      "WebFetch(domain:docs.example.com)"
    ],
    "ask": [
      "Bash(git push *)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./secrets/**)",
      "Bash(curl *)",
      "mcp__*"
    ]
  }
}
```

重要边界：

- `Read` / `Edit` deny 主要约束 Claude Code 识别的内建工具和部分可识别 Bash 文件命令。
- 任意 Python/Node 脚本自己读文件，permission rules 不一定能拦住。
- 需要 OS 级边界时，要配合 sandbox。
- Bash URL 过滤用命令 pattern 很脆弱；更可靠的是禁止 `curl`/`wget`，改用 `WebFetch(domain:...)` 或 `PreToolUse` hook。

### sandboxing：OS 级隔离

sandboxing 解决的是：即使 Claude 试图运行某个 Bash 命令，操作系统也限制这个命令和子进程能访问的文件和网络。

Claude Code 有几类隔离方式：

- Sandboxed Bash tool：只隔离 Bash 命令及其子进程。
- Sandbox runtime：隔离整个 Claude Code 进程，包括 file tools、MCP servers、hooks。
- Dev container / custom container / VM：隔离整个开发环境。
- Claude Code on the web：Anthropic 托管环境。

内置 Bash sandbox 只限制 Bash；内建 file tools、MCP、hooks 仍在 host 上运行。容器、VM 或 whole-process sandbox 才把整个 Claude Code 进程放入隔离边界。

示例：

```json
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,
    "autoAllowBashIfSandboxed": true,
    "allowUnsandboxedCommands": false,
    "filesystem": {
      "denyRead": ["~/.aws/credentials", "~/.ssh/**"],
      "denyWrite": ["/etc", "/usr/local/bin"],
      "allowWrite": ["./", "/tmp/build"]
    },
    "network": {
      "allowedDomains": ["registry.npmjs.org", "github.com"]
    }
  }
}
```

关键理解：

- permissions 控制“Claude Code 是否准备用工具”。
- sandbox 控制“进程实际能不能碰到资源”。
- sandbox 可防 prompt injection 诱导 Bash 访问边界外资源。
- sandbox 不改变发送给模型的内容；Claude 读取并放入上下文的内容仍可能发送给模型。

### managed policy：组织级不可覆盖约束

Managed settings 是企业或组织层的控制面，可以通过 server-managed settings、MDM、registry、系统级文件等方式下发。它们不能被用户或项目设置覆盖。

适合 managed policy 的内容：

- 禁止读取全局 secret 路径。
- 禁止用户启用 bypass permissions。
- 限制可用模型。
- 限制 MCP servers。
- 强制 sandbox。
- 禁止非托管 hooks。
- 禁止用户/项目自定义 permission rules。

示例：

```json
{
  "allowManagedPermissionRulesOnly": true,
  "allowManagedHooksOnly": true,
  "allowManagedMcpServersOnly": true,
  "permissions": {
    "disableBypassPermissionsMode": "disable",
    "deny": [
      "Read(//**/.env)",
      "Read(//**/secrets/**)"
    ]
  },
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,
    "allowUnsandboxedCommands": false
  }
}
```

几个关键 managed-only 开关：

- `allowManagedPermissionRulesOnly`：只允许 managed settings 中的 permission rules 生效。
- `allowManagedHooksOnly`：只加载 managed hooks、SDK hooks，以及 managed 强制启用插件中的 hooks。
- `allowManagedMcpServersOnly`：只尊重管理员定义的 MCP allowlist。
- `sandbox.failIfUnavailable`：sandbox 不可用时直接启动失败，而不是降级为 unsandboxed。

这层适合“不能协商”的安全和合规规则。

### lifecycle hooks：运行时动态约束

hooks 是 Claude Code 生命周期中的自动执行点，可以是 shell command、HTTP endpoint 或 LLM prompt。它们可以在 session、turn、tool call、compaction、file change 等事件上运行。

常用的约束型 hook：

- `UserPromptSubmit`：检查用户 prompt 是否包含敏感信息或不合规请求。
- `PreToolUse`：工具调用前动态判断，能 deny、force prompt 或 allow。
- `PostToolUse`：工具调用后审计输出、记录日志、触发检查。
- `Stop`：Claude 准备结束时检查是否跑了测试、是否漏了验证。
- `ConfigChange`：配置变化时审计。
- `PreCompact` / `PostCompact`：压缩前后保留重要上下文。
- `SessionStart` / `SessionEnd`：初始化或收尾审计。

权限关系：

- `PreToolUse` hook 在 permission prompt 前运行。
- hook 可以 deny 或 force prompt。
- hook 不能绕过 permission deny/ask。
- matching deny 仍然阻止调用，matching ask 仍然提示。
- 阻塞型 hook 可以优先于 allow rule 阻止调用。

适用判断：

- “禁止读取 `.env`”：permission deny。
- “只有当前分支名包含 `release/` 时才允许部署”：`PreToolUse` hook。
- “修改支付代码后必须跑支付测试，否则不能 Stop”：`Stop` hook。
- “每次 `git push` 都要人工确认”：permission ask。
- “任何 `terraform apply` 必须检查 workspace 和账号”：`PreToolUse` hook。

### 分层设计建议

从软到硬设计约束：

1. `CLAUDE.md`：告诉 Claude 应该怎么做。  
   例如“修改 billing 后运行 `npm test -- billing`”。
2. Project settings：团队共享默认权限。  
   例如允许 `npm test`，询问 `git push`，禁止读 `.env`。
3. Sandbox：给 Bash 和子进程划 OS 边界。  
   例如只能写 workspace 和 temp，只能访问允许域名。
4. Hooks：补充运行时规则。  
   例如根据文件路径、分支、命令参数、diff 内容动态阻止或要求确认。
5. Managed policy：组织不可覆盖底线。  
   例如禁用 bypass mode、强制 sandbox、禁止读取 secret、限制 MCP 和 hooks 来源。

一句话：`CLAUDE.md` 管意图，settings 管默认，permission rules 管授权，sandbox 管物理边界，managed policy 管组织底线，lifecycle hooks 管上下文动态判断。

## 解决维护噩梦

维护噩梦通常来自把 `CLAUDE.md` 当知识库。

解决方法：

- 单条规则短小化：一条规则只解决一个问题。
- 按 scope 放置：组织、用户、项目、子目录、本地分开。
- 引用权威文件：不要复制整份架构文档，只写“先读哪里”。
- 定期删规则：过期、重复、冲突的规则比没有规则更糟。
- 可强制的交给工具：格式、lint、安全禁止、测试门禁交给机器机制。
- 给规则保留来源意识：例如“Added after repeated API review feedback, 2026-07”。

## 解决注意力分散

注意力分散来自无关规则进入上下文。

解决方法：

- 根 `CLAUDE.md` 只放通用高频规则。
- 路径相关内容放子目录或 path-scoped rules。
- 大型流程放 skill。
- 临时任务放 prompt。
- 本机事实放 `CLAUDE.local.md`。
- 定期审计 auto memory，避免旧调试经验持续误导。

## 与其他系统的对照

| 系统 | 记忆设计 | 关键差异 |
| --- | --- | --- |
| Claude Code | `CLAUDE.md`、auto memory、imports、path-scoped rules，以及 settings/hooks/permissions 控制面 | 记忆是 context；强制控制需要另走控制面 |
| Codex | `AGENTS.md` 做持久指导；memories 做跨线程本地召回；skills 做可复用工作流；MCP 接外部上下文；rules 控制 sandbox 外命令 | 与 Claude Code 类似，明确区分指导、记忆、技能、外部工具、执行策略 |
| LangGraph | checkpointer 保存 thread graph state；store 保存跨 thread long-term memory | 更像 agent runtime 的显式状态模型，开发者定义 state、checkpoint、store 和检索策略 |
| AutoGen | Agent/Team 可保存和恢复 state；Memory protocol 支持 `add`、`query`、`update_context` 等操作 | 更像多 agent 框架的可插拔记忆接口，记忆通过上下文更新注入 agent |
| Cursor | Project/User/Team Rules、`AGENTS.md`、`.mdc` 规则激活模式、checkpoints | 与 Claude Code 的条件化规则最接近，但更强调 IDE agent 的规则选择和编辑器上下文 |

## 实用清单

写入任何一条 `CLAUDE.md` 规则前，先问：

- 这条规则是否解决重复问题？
- 是否跨 session 有用？
- 是否适用于当前 scope 的大多数任务？
- 是否具体可执行？
- 是否已有工具能强制？
- 是否会很快过期？
- 是否应该下沉到子目录、本地层、用户层或 skill？

如果答案不清楚，先不要写进根 `CLAUDE.md`。

## 来源

| 主题 | 来源 | 本文使用方式 |
| --- | --- | --- |
| Claude Code memory | https://code.claude.com/docs/en/memory | `CLAUDE.md`、auto memory、加载方式、imports、path-scoped rules、memory-as-context |
| Claude Code hooks | https://code.claude.com/docs/en/hooks | 区分 context 记忆和执行控制面 |
| Claude Code settings | https://code.claude.com/docs/en/settings | settings scopes、permissions、managed policy、sandbox |
| Claude Code permissions | https://code.claude.com/docs/en/permissions | permission rules、工具授权、permissions 与 sandboxing 的互补关系 |
| Claude Code sandbox environments | https://code.claude.com/docs/en/sandbox-environments | Sandboxed Bash、sandbox runtime、container、VM、web 的隔离边界对比 |
| Claude Code Bash sandboxing | https://code.claude.com/docs/en/sandboxing | Bash sandbox 模式、auto-allow、filesystem/network 边界 |
| Codex customization | https://developers.openai.com/codex/concepts/customization | `AGENTS.md`、memories、skills、MCP、subagents 的分层 |
| Codex `AGENTS.md` | https://developers.openai.com/codex/guides/agents-md | global/project/nested guidance、precedence 和 discovery |
| Codex rules | https://developers.openai.com/codex/rules | sandbox 外命令的 rules 控制面 |
| Codex memories | https://developers.openai.com/codex/memories | Codex memories 的跨线程上下文定位 |
| LangGraph persistence | https://docs.langchain.com/oss/python/langgraph/persistence | checkpointer、thread state、durable execution |
| LangGraph memory | https://docs.langchain.com/oss/python/langgraph/add-memory | short-term 和 long-term memory |
| AutoGen memory | https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/memory.html | Memory protocol、context update、memory backends |
| AutoGen state | https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/state.html | Agent/Team state save/load |
| Cursor rules | https://cursor.com/docs/rules.md | Project/User/Team rules、`.mdc` activation、`AGENTS.md` |
| Cursor agent overview | https://cursor.com/docs/agent/overview.md | IDE agent 的 instructions、tools、model 与 checkpoints |
