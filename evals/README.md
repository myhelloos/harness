# Evaluations

This directory is for reusable evaluation tasks and analysis.

Keep these concerns separate:

- `tasks/`: task definitions and fixtures.
- `scorers/`: deterministic checks, model graders, rubrics.
- `logs/`: raw run logs and transcripts.
- `analysis/`: summaries, comparisons, charts, decisions.

## Evaluation Rule

An eval result is incomplete unless it includes:

- Task version.
- Harness version.
- Model version.
- Tool permissions.
- Runtime budget.
- Scoring method.
- Raw logs.
- Final score.

