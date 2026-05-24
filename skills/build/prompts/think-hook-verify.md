# Think Hook: Post-Verification Analysis

You are the think-hook agent. Your job is to analyze the verification result using the thinking packs framework, then recommend what the build skill should do next.

## Input

- State directory: `{state_dir}`
- Verification result: read from `{state_dir}/verify-report.md`
- Verification methods used: {verification_methods}

## Context

Read these files for context:
- `{state_dir}/session.md` — build goal and history
- `{state_dir}/understanding.md` — original requirements
- `{state_dir}/plan.md` — what was planned

## Instructions

1. Read `verify-report.md` and determine: Did verification pass or fail?

2. **If PASS (all checks passed):**
   - Invoke the **verify-success** thinking pack.
   - Read the prompt from `skills/think/prompts/verify-success.md`.
   - Fill the input materials from the build state:
     - 目标 = the build goal from session.md
     - 假设 = the plan's assumptions
     - 行动/实验 = what was executed (from session.md iteration history)
     - 观察到的成功结果 = the verification pass details
     - 成功标准 = the verification criteria from verify-report.md
     - 可用证据 = the verification method outputs
   - Execute the analysis steps from the prompt.
   - Write the output to `{state_dir}/think-verify-success.md` and `{state_dir}/think-verify-success.json`.

3. **If FAIL (any checks failed):**
   - Invoke the **verify-failure** thinking pack.
   - Read the prompt from `skills/think/prompts/verify-failure.md`.
   - Fill the input materials from the build state:
     - 目标 = the build goal from session.md
     - 假设 = the plan's assumptions
     - 行动/实验 = what was executed
     - 观察到的失败表现 = the verification failure details from verify-report.md
     - 失败标准 = the verification criteria
     - 时间窗口 = time spent on this iteration
     - 可用证据 = the verification method outputs
   - Execute the analysis steps from the prompt.
   - Write the output to `{state_dir}/think-verify-failure.md` and `{state_dir}/think-verify-failure.json`.

4. **Based on the thinking pack result, write a recommendation to `{state_dir}/think-recommendation.md`:**

```markdown
# Think Recommendation

## Entry Pack
[verify-success or verify-failure]

## Conclusion
[The pack's conclusion]

## Evidence Level
[强/中/弱]

## Recommendation for Build Skill

Choose one:
- **continue-fixing**: Issues are real, proceed to Phase 5 Fix with focused scope from root-cause analysis
- **narrow-scope**: Evidence is weak or uncertain, go back to Phase 3 with a smaller scope
- **re-verify**: Metrics may be wrong, go back to Phase 4 with adjusted verification
- **proceed**: Success is genuine, proceed to Phase 6 Knowledge Extraction
- **deep-analysis**: Root cause is complex, run root-cause and main-contradiction packs before fixing

## Reasoning
[Why this recommendation]
```

5. Append a log entry to `{state_dir}/session.md`:

```
## Think Analysis <timestamp>
**Entry**: [verify-success or verify-failure]
**Conclusion**: [真成功/假成功/不确定 or 真失败/假失败/不确定]
**Evidence**: [强/中/弱]
**Recommendation**: [continue-fixing | narrow-scope | re-verify | proceed | deep-analysis]
```

## Rules

- This is Phase 4.5 — it sits between Phase 4 (Verify) and Phase 5 (Fix).
- Do NOT modify any existing files except session.md (append only).
- The recommendation determines what the build skill does next. Be precise.
- If evidence level is "弱" for either pass or fail, default to recommending re-verify or narrow-scope rather than proceeding.
