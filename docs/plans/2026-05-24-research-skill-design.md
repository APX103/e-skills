# E-Research Skill Design

## Overview

Add an `e-research` skill for long-running knowledge production tasks: thought experiments, computer science research, autonomous experiments, unfamiliar-system investigation, and evidence-backed reports.

The skill complements the existing system instead of replacing it:

- `brainstorming` clarifies the initial contract when the goal is vague.
- `e-research` owns the research loop: charter -> investigation -> experiment -> evidence review -> synthesis.
- `think` supplies analysis packs for unknowns, assumptions, evidence quality, failures, and next experiments.
- `build` executes engineering-heavy experiments when code, environments, tests, or benchmarks are needed.

## Success Criteria

1. Agents can take a broad research request and turn it into a bounded research charter.
2. Agents can run multiple investigation or experiment loops without repeatedly asking the user for approval.
3. Research outputs distinguish facts, hypotheses, speculation, and evidence gaps.
4. Results are logged in `.agent-log/<timestamp>-research/` so long tasks survive context compaction.
5. The skill remains selective: it triggers for knowledge production, not ordinary implementation or one-off explanations.

## Workflow

### Phase 0: Charter

If the user has not already supplied a clear research question, success criteria, scope, and stop conditions, use `brainstorming` once to clarify them. The result is a research charter, not a product design.

The charter defines:

- research question
- background and known facts
- hypotheses
- acceptable methods
- evidence standards
- outputs
- autonomy boundaries
- stop conditions

### Phase 1: Investigation

Use high-information sources first: existing files, docs, logs, papers, APIs, benchmarks, or public sources when freshness matters. Invoke `think` packs such as `investigation`, `assumption-surfacing`, and `evidence-strength` when the task has unknowns or thin evidence.

### Phase 2: Experiment

Design the smallest experiment that can change belief about one hypothesis. For CS research, this may involve creating a benchmark, implementing a prototype, running simulations, testing algorithms, or reproducing a paper result. If the experiment is engineering-heavy, route execution through `build`.

### Phase 3: Evidence Review

After each experiment, verify whether the result is genuine. Use `think` packs to classify success or failure, assess evidence strength, surface assumptions, and decide the next experiment.

### Phase 4: Synthesis

Produce a report with claims tied to evidence. Include limitations and unresolved questions. Extract reusable knowledge into a concise final section.

## State Files

Research state lives under `.agent-log/<YYYY-MM-DD-HHMMSS>-research/`:

```text
session.md
charter.md
evidence-ledger.md
experiment-1.md
experiment-1-results.md
experiment-2.md
report.md
knowledge.md
```

## Skill Shape

The skill should include:

- `skills/e-research/SKILL.md`: concise routing and workflow guidance.
- `skills/e-research/prompts/charter.md`: turns a broad ask into a research charter.
- `skills/e-research/prompts/experiment.md`: designs minimal experiments.
- `skills/e-research/prompts/synthesis.md`: produces evidence-backed reports.

The `SKILL.md` should reference `think` and `build` instead of duplicating their detailed procedures.
