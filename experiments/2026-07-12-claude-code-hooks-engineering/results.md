# 结果记录

运行日期：2026-07-12 Asia/Shanghai

## 结果摘要

| Probe 类别 | Cases | 结果 |
| --- | ---: | --- |
| 安全防护 | 5 | 全部通过 |
| 代码质量 | 4 | 全部通过 |
| 子智能体上下文 | 4 | 全部通过 |
| 合计 | 13 | 全部通过，0 failure |

最终复核运行时间：0.300s。

## 观察结果

- 安全 safe command 不输出 decision；secret prompt 返回顶层 block；destructive command/protected path 返回 `PreToolUse` deny；force push 返回 ask。
- Formatter success 返回 `PostToolUse.additionalContext`。
- Stop check failure 返回顶层 block；`stop_hook_active: true` 时使用 `continue: false` hard stop，避免无限 loop 和虚假成功。
- Explore 启动只收到 Explore policy；缺少 required sections 的输出被要求继续；完整输出可停止。
- 所有 JSON policy/config/fixture 通过 `jq -e` 解析。

## 原始输出

见 [artifacts/test-output.txt](./artifacts/test-output.txt)。

## 失败实验

没有 fixture probe 失败。

Claude Code 端到端 probe 未运行，因为本机没有 `claude` CLI。这是环境限制，不计为通过，也不计为 handler logic failure。

## 已知限制

- 没有验证具体 Claude Code 版本的 matcher、event delivery、UI 或 continuation。
- 没有测量误报率、hook latency tail、模型成功率或 context token savings。
- 测试使用 `/usr/bin/true` 和 `/usr/bin/false` 隔离 quality control flow，没有运行真实项目 formatter/test suite。
- Security patterns 和 subagent section contract 仍需针对实际 workload 校准。

## 下一步决策

1. 在装有 Claude Code 的隔离环境执行 `run.md` 中的低风险端到端探针。
2. 保存 debug log，核对每个 event 的输入与 handler 输出。
3. 选择一个真实代码任务，对比无 hooks、只安全 hooks、完整 hooks 三组的延迟、成功率、人工审批数和 context 使用量。
