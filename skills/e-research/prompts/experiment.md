# Research Experiment Prompt

Design the next minimal experiment for a research task.

## Input

- Charter: read `{state_dir}/charter.md`
- Evidence ledger: read `{state_dir}/evidence-ledger.md` if it exists
- Prior results: `{prior_results}`
- Target hypothesis: `{hypothesis}`

## Instructions

1. Pick exactly one hypothesis or uncertainty to test.
2. Design the smallest action that can change belief about it.
3. Identify the changed variable and controlled variables.
4. Define success, failure, and inconclusive criteria before execution.
5. Define result metrics, process metrics, and side-effect metrics.
6. Define required tools or environment.
7. Define reproduction steps.
8. Define stop or pivot conditions.

## Output

Write `{state_dir}/experiment-N.md`:

```markdown
# Experiment N

## Hypothesis
[one sentence]

## Minimal Action
[smallest testable action]

## Variables
- Changed variable:
- Controlled variables:

## Criteria
- Success:
- Failure:
- Inconclusive:

## Metrics
- Result:
- Process:
- Side-effect:

## Execution Plan
[commands, files, data, or procedure]

## Reproduction
[how another agent can rerun it]

## Stop / Pivot Conditions
[when to stop, retry, or change direction]
```

After executing the experiment, write `{state_dir}/experiment-N-results.md` and update `{state_dir}/evidence-ledger.md`:

```markdown
# Experiment N Results

## Result
[success / failure / inconclusive]

## Evidence
[commands, observations, files, or data]

## Interpretation
[what changed in belief and why]

## Gaps
[what remains unknown]
```
