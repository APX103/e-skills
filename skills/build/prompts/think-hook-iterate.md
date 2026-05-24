# Think Hook: Post-Fix Analysis

You are the think-hook agent. Your job is to evaluate the fix cycle results and recommend whether the build should iterate again or proceed.

## Input

- State directory: `{state_dir}`
- Current iteration: {iteration_number}

## Context

Read these files:
- `{state_dir}/session.md` — full build history
- `{state_dir}/think-verify-success.md` or `{state_dir}/think-verify-failure.md` — the Phase 4.5 analysis (if it exists)
- `{state_dir}/think-recommendation.md` — the previous recommendation (if it exists)

## Instructions

1. Assess the fix cycle:
   - How many fix rounds were needed?
   - Did issues decrease across rounds?
   - Is the current state stable or fragile?

2. If the previous think-recommendation was "deep-analysis" and root-cause was NOT yet run:
   - Invoke the **root-cause** thinking pack using `skills/think/prompts/root-cause.md`.
   - Write output to `{state_dir}/think-root-cause.md` and `{state_dir}/think-root-cause.json`.
   - If root-cause finds multiple system conditions, also invoke **main-contradiction** using `skills/think/prompts/main-contradiction.md`.
   - Write output to `{state_dir}/think-main-contradiction.md` and `{state_dir}/think-main-contradiction.json`.
   - Update the recommendation based on the deeper analysis.

3. Write a recommendation to `{state_dir}/think-iterate-recommendation.md`:

```markdown
# Iterate Recommendation

## Fix Cycle Assessment
[How the fix cycle went]

## Think Analysis Results
[If root-cause or main-contradiction were run, summarize]

## Recommendation for Build Skill

Choose one:
- **next-iteration**: Issues resolved but need a fresh build pass — proceed to next outer iteration
- **stop-iterate**: Issues resolved, proceed to Phase 6 Knowledge Extraction
- **pivot**: Fundamental issues found — go back to Phase 1 (re-understand) or Phase 2 (re-plan)
- **continue-fixing**: More fix rounds needed, specific issues remain

## Reasoning
[Why this recommendation]
```

4. Append to `{state_dir}/session.md`:

```
## Iterate Think Analysis <timestamp>
**Assessment**: [fix cycle summary]
**Recommendation**: [next-iteration | stop-iterate | pivot | continue-fixing]
```

## Rules

- Do NOT modify understanding.md or plan.md.
- If this is the last iteration (--iterations N reached), recommend "stop-iterate" unless critical issues remain.
- A "pivot" recommendation is serious — only use it when root-cause reveals that the original plan was fundamentally wrong.
