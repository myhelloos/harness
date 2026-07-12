# 运行命令

## 全部 fixture probes

```bash
cd experiments/2026-07-12-claude-code-hooks-engineering
python3 tests/run_tests.py
```

## 单独查看安全 deny output

```bash
python3 hooks/security_guard.py < tests/fixtures/security-dangerous-bash.json
```

预期关键字段：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny"
  }
}
```

## 单独查看质量 Stop gate

```bash
CLAUDE_HOOK_QUALITY_POLICY=tests/fixtures/quality-policy-fail.json \
  python3 hooks/quality_automation.py < tests/fixtures/quality-stop.json
```

预期关键字段：

```json
{
  "decision": "block",
  "reason": "Quality gate failed: ..."
}
```

## 单独查看 subagent context

```bash
python3 hooks/subagent_context.py < tests/fixtures/subagent-start-explore.json
```

预期关键字段：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SubagentStart",
    "additionalContext": "Scoped contract for subagent type Explore: ..."
  }
}
```

## 校验 JSON 文件

```bash
find . -name '*.json' -type f -print0 | xargs -0 -n1 jq -e . >/dev/null
```

## Claude Code 端到端探针

在安装了 Claude CLI 的环境中，从仓库根目录运行：

```bash
claude --settings experiments/2026-07-12-claude-code-hooks-engineering/config/settings.example.json --debug-file /tmp/claude-hooks-debug.log
```

依次执行以下低风险任务并检查 debug log：

1. 提交不含 secret 的普通 prompt，确认 `UserPromptSubmit` 通过。
2. 请求 `git status --short`，确认 `PreToolUse` 无决策并进入正常 permission flow。
3. 在临时文件上触发 Write，确认 `PostToolUse` formatter 路由。
4. 启动 Explore subagent，确认只注入 Explore contract。
5. 让 Explore 返回缺少 `Evidence` 的结果，确认 `SubagentStop` 要求补全且最多阻断一次。

不要用真实 secret 或 destructive command 做端到端测试。安全 deny 行为已经可以通过 fixture 验证。
