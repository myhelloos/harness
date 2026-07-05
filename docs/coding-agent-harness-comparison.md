# Coding Agent Harness Comparison

Checked: 2026-07-05 Asia/Shanghai

This document compares Claude Code, Cursor, and Codex as coding-agent harnesses. It uses five questions:

1. How context enters the agent.
2. How tools are exposed and used.
3. How actions are constrained.
4. How results are verified.
5. How experience carries across sessions.

## Core Model

Use this working definition:

```text
Agent = Model + Harness
```

The model supplies reasoning, language, planning, and tool-call intent. The harness supplies the runtime around the model: context assembly, tool execution, permission policy, sandboxing, session management, verification, memory, integrations, logs, diffs, and artifacts.

Cursor states this most directly: its Agent is built from instructions, tools, and the selected model. Claude Code and Codex expose the same practical structure through memory, tools, permissions, hooks, sessions, and integrations.

## Summary

| Dimension | Claude Code | Cursor | Codex |
| --- | --- | --- | --- |
| Context ingress | `CLAUDE.md`, auto memory, session context, file reads, MCP, IDE/CLI/Desktop/Web surfaces. | Prompt, open or selected editor files, codebase index, Rules, `AGENTS.md`, MCP, Browser screenshots. | Prompt, `@` files and images, IDE open files and selections, `AGENTS.md`, tool output, MCP, skills, plugins, memories, Chronicle. |
| Tool use | Read/edit/search, Bash or PowerShell, MCP, hooks, subagents, Agent SDK. | Semantic search, file search/read/edit, terminal, web, Browser, MCP, image generation. | File read/write, shell, patching, web, MCP, plugins, skills, subagents, Browser or Computer Use depending on surface. |
| Action constraints | Permission rules, settings, managed policy, sandbox, `PreToolUse` hooks. | Run Modes, Auto-review classifier, allowlist, `permissions.json`, `sandbox.json`, team controls. | Approval policy, sandbox mode or permission profile, filesystem and network rules, hooks, managed requirements, inherited subagent policy. |
| Verification | User-directed tests and commands; hooks can verify after tool use or before stop; agent hooks can inspect files and run tests. | Terminal checks, Browser UI verification, Agent Review, checkpoints for rollback. | Repro steps, tests, lint, pre-commit checks, `/review`, Codex Security validation, hooks and skills for workflow checks. |
| Cross-session experience | Human-written `CLAUDE.md` plus auto memory; settings, skills, hooks, MCP config. | Project/User/Team Rules, `AGENTS.md`, MCP config, checkpoints within sessions. | `AGENTS.md`, opt-in memories, threads and resume, compaction, skills, plugins, config, Chronicle. |

## Claude Code

Claude Code is memory-first. Each session starts with a fresh context window, then durable context enters mainly through `CLAUDE.md` files and auto memory.

`CLAUDE.md` files can exist at organization, user, project, local, and nested directory scopes. Files above the working directory load at launch; subdirectory files load on demand when Claude reads files there. `CLAUDE.md` can import other files with `@path` syntax.

Auto memory lets Claude write notes from corrections and preferences. Both `CLAUDE.md` and auto memory are context, not enforced configuration. To mechanically block an action, use permissions or hooks.

The tool layer includes file reading and editing, search, shell commands, MCP tools, subagents, hooks, background agents, and Agent SDK workflows. MCP is the primary external integration mechanism.

Constraints are layered through settings, permission rules, sandboxing, managed policy, and lifecycle hooks. `PreToolUse` hooks can deny a tool call before it executes. `Stop` hooks can require extra work before Claude finishes. Agent hooks can spawn a subagent with tools to inspect files or run tests.

Claude Code's strongest differentiator is the combination of persistent memory and a rich hook lifecycle.

## Cursor

Cursor is IDE-context-first. Context enters through prompt text, open files, selected text, codebase indexing, file search, Rules, `AGENTS.md`, MCP, and Browser state.

Cursor Rules are persistent prompt-level context. Project Rules live in `.cursor/rules` as `.mdc` files. Rules can always apply, apply to matching files, be manually mentioned, or be selected by the agent based on description. User Rules apply across projects. Team Rules can be centrally managed and optionally enforced.

Cursor also supports `AGENTS.md` in project roots and subdirectories. Nested files are combined with parent files, with more specific instructions taking precedence.

The tool layer includes semantic search, file and folder search, web search, rule fetching, file reading, file editing, terminal execution, Browser control, MCP, image generation, and clarifying questions.

Cursor's main local autonomy controls are Run Modes:

- Auto-review: allowlisted calls run immediately; other shell commands use the sandbox when possible; higher-risk calls go through a classifier.
- Allowlist: allowlisted actions run without approval, with optional sandboxing for supported shell commands.
- Run Everything: all tool calls run automatically.

`permissions.json` steers Auto-review decisions. `sandbox.json` controls sandbox reachability, including network domains and extra readable or writable paths. Cursor explicitly notes that Auto-review is not a security boundary; sandboxing is the stronger runtime boundary for terminal commands.

Verification is tied to the IDE and browser loop: terminal checks, Browser screenshots and interaction, Agent Review, and checkpoints. Checkpoints are local rollback aids, not permanent version control or correctness proof.

## Codex

Codex is repo-instruction and policy-first. Context enters through prompts, `@`-mentioned files and images, IDE open files and selections, `AGENTS.md`, discovered file contents, tool outputs, MCP, skills, plugins, memories, and Chronicle.

Codex threads are sessions containing prompts, model outputs, and tool calls. Threads can be resumed. Long-running work can continue through automatic compaction, where Codex summarizes relevant context and discards less relevant details.

The tool layer is a model-tool loop: the model proposes actions and the harness executes file reads, edits, shell commands, patching, web access, MCP calls, or other surface-specific tools. Codex can be extended through skills, plugins, MCP servers, app connectors, subagents, and custom agents.

Codex has the most explicit sandbox and approval model:

- Approval policy controls when Codex must ask before acting.
- Sandbox mode or permission profiles control filesystem and network access.
- Default local behavior keeps network access off and limits writes to the workspace.
- File and network rules can define exact read, write, deny, and domain policy.
- Hooks can run around lifecycle events and tool calls.
- Managed requirements can restrict sandbox modes, approvals, web search modes, hooks, MCP, and more.
- Subagents inherit sandbox policy unless explicitly configured.

Verification is built around task contracts: reproduce the issue, add or update tests, run lint/type checks/focused suites, confirm behavior, and review diffs. Codex Security is a specialized example: it runs validation in a sandbox and preserves commands, exit codes, stdout, stderr, test results, diffs, and artifacts as evidence.

Cross-session experience comes from `AGENTS.md`, opt-in memories, thread history, resume, compaction, skills, plugins, config files, and Chronicle. Required team guidance should live in `AGENTS.md` or checked-in docs; generated memory is useful recall, not the sole source of rules.

## Comparative Takeaways

Claude Code is memory-first: useful when long-lived project conventions and repeated corrections matter.

Cursor is IDE-context-first: useful when open files, selection, codebase index, and browser verification should dominate the loop.

Codex is policy-first: useful when task contracts, repo guidance, sandboxing, approvals, resumable threads, and auditability should be explicit.

For team-critical behavior, prefer checked-in instruction files or managed policy over generated memory. For correctness, none of the three provides automatic proof: verification must be designed into the task or harness.

## Harness Evaluation Questions

Use these questions before adopting a harness for a workload:

1. What context is automatically loaded, and what must be attached manually?
2. Can context loading be scoped by path, file type, or task?
3. Which tools can mutate state?
4. Which tool calls require approval?
5. Is there an OS-level sandbox, or only prompt/classifier-level guidance?
6. Can policy be enforced centrally for a team?
7. Can verification block completion?
8. Are raw logs, diffs, command outputs, and artifacts preserved?
9. Can a task resume after interruption or context compaction?
10. What becomes durable across sessions, and who controls it?

## Sources

- Claude Code overview: https://code.claude.com/docs/en/overview
- Claude Code memory: https://code.claude.com/docs/en/memory
- Claude Code hooks: https://code.claude.com/docs/en/hooks
- Claude Code settings: https://code.claude.com/docs/en/settings
- Claude Code MCP: https://code.claude.com/docs/en/mcp
- Cursor Agent overview: https://cursor.com/docs/agent/overview.md
- Cursor Rules: https://cursor.com/docs/rules.md
- Cursor Run Modes: https://cursor.com/docs/agent/security/run-modes.md
- Cursor MCP: https://cursor.com/docs/mcp.md
- Codex manual: https://developers.openai.com/codex/codex-manual.md

