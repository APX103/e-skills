---
name: research
description: Use when asked to conduct long-running research, knowledge production, thought experiments, computer science research, autonomous experiments, evidence-backed investigations, or Chinese requests like 研究, 调研, 思维实验, 知识生产, or 计算机科学研究.
---

# Research

Use this for knowledge production, not ordinary implementation. The goal is to turn an open question into a bounded research loop with evidence, experiments, and a clear report.

## When to Use

Use for requests like:

- "research this", "study this", "investigate deeply", "do a thought experiment"
- computer science research, algorithm comparison, benchmark design, prototype experiments
- open-ended knowledge production where the agent can gather evidence and run tests
- claims that need evidence quality checks, replication, or multiple experiment rounds

Do not use for one-off explanations, direct coding tasks, simple bug fixes, or routine code review. Use `build` for implementation-only work and `think` for standalone reflection on an existing result.

## Core Loop

1. **Create a Research Charter**: If the question, scope, evidence standard, or stop condition is unclear, use `brainstorming` once to clarify the task. Then fill `prompts/charter.md`.
2. **Set up state**: Store all research state in `.agent-log/<YYYY-MM-DD-HHMMSS>-research/`.
3. **Investigate**: Gather the smallest useful evidence set. Use local files first; browse when recency or external sources matter. Use `think --pack investigation` or `assumption-surfacing` when unknowns dominate.
4. **Design experiments**: Use `prompts/experiment.md` or `think --pack next-experiment`. Change one important variable at a time.
5. **Execute**: Run experiments directly when small. Use `build` when the experiment requires code, environments, tests, benchmarks, or iterative fixes.
6. **Review evidence**: Use `think` packs such as `verify-success`, `verify-failure`, `reproduce`, and `evidence-strength`.
7. **Synthesize**: Use `prompts/synthesis.md` to produce claims, evidence, limitations, and reusable knowledge.

## Human Gates

Ask the user before:

- spending substantial money or time
- using credentials or private services
- changing production systems
- widening the research question beyond the charter

Otherwise, proceed autonomously and keep the state files current.

## Evidence Rules

- Separate facts, hypotheses, interpretations, and speculation.
- Every important claim needs an evidence pointer or an explicit "unknown".
- Prefer reproducible experiments over persuasive prose.
- Record failed experiments; they are research output.
- Stop when the charter's success criteria or stop conditions are met.

## Outputs

Minimum useful output:

```text
session.md          # goal, decisions, progress
charter.md          # question, scope, hypotheses, evidence standard
evidence-ledger.md  # claims and supporting evidence
report.md           # final synthesis
knowledge.md        # compact reusable learnings
```

For multi-round work, add `experiment-N.md` and `experiment-N-results.md`.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Treating a research task like a product spec | Write a research charter with hypotheses and evidence standards. |
| Running experiments before defining success | Define success, failure, uncertainty, and stop conditions first. |
| Explaining results without checking evidence | Run evidence-strength before confident synthesis. |
| Hiding negative results | Log failed or inconclusive experiments as evidence. |
| Asking the user at every step | Gate only high-cost, high-risk, or scope-changing decisions. |
