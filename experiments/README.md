# 实验

每个实验都应小到可以重新运行。

使用这个结构：

```text
experiments/YYYY-MM-DD-short-name/
├── README.md
├── setup.md
├── run.md
├── results.md
└── artifacts/
```

## 实验模板

包含：

- 问题。
- 被测试的 harness 或框架。
- 模型和版本。
- 任务。
- 预算。
- 命令。
- 原始输出位置。
- 结果。
- 失败笔记。
- 下一步决策。

## 当前实验

- [2026-07-12 Claude Code hooks 工程实战](./2026-07-12-claude-code-hooks-engineering/README.md)：安全防护、代码质量自动化与子智能体精确上下文管理；包含可执行 handlers、JSON policies、fixtures 和原始结果。
