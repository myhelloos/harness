# 安装与准备

检查日期：2026-07-12 Asia/Shanghai

## 必需环境

- Python 3.10 或更高版本。
- 不需要第三方 Python package。
- `jq` 仅用于人工查看和校验 JSON，不是 hook runtime 依赖。

检查命令：

```bash
python3 --version
jq --version
```

本次实际环境：

```text
Python 3.14.5
jq-1.8.1
```

## Claude Code 准备

本机未安装 Claude Code，因此本次没有执行真实 lifecycle trigger。具备 Claude CLI 的环境可从仓库根目录临时加载示例配置：

```bash
claude --settings experiments/2026-07-12-claude-code-hooks-engineering/config/settings.example.json --debug-file /tmp/claude-hooks-debug.log
```

示例配置引用当前实验路径，不会自动修改项目 `.claude/settings.json`。正式采用时应把 hooks、policies 和 custom agent 放入团队约定位置，再把配置合并到受版本控制的 project settings；不要覆盖已有 settings。

## 可选 policy override

三个 handler 支持环境变量指向替代 policy：

```text
CLAUDE_HOOK_SECURITY_POLICY
CLAUDE_HOOK_QUALITY_POLICY
CLAUDE_HOOK_SUBAGENT_POLICY
```

这适合测试 fixture；生产环境应优先使用稳定、受 code review 的绝对路径或 repository-relative deployment layout。
