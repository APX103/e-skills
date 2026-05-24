---
name: build
description: Use when starting a greenfield implementation, replicating an existing project, refactoring a module, or improving an existing codebase. Triggers on "build", "implement", "create project", "replicate", "engineer", or any task requiring multi-step code execution with verification.
---

# /build

Self-driving loop: understand -> plan -> execute -> verify -> iterate. File-based state, subagent isolation, full logging. Human interacts only at Phase 0.

## Invocation

```
/build "<task>" [--iterations N] [--verification "method1,method2"] [--dry-run]
```

- `<task>`: What to build. May include file paths, URLs, or references.
- `--iterations N`: Closed-loop cycles (default 1).
- `--verification`: Comma-separated: `design-comparison`, `automated-testing`, `visual-comparison`, `code-review`. Omit to auto-detect and ask human.
- `--dry-run`: Run Phase 7 (Prompt Evolution) in read-only mode. Generates the evolution report but does not modify any prompt files. Useful for previewing what changes would be proposed before applying them.

## Architecture

All state in files under `.agent-log/<timestamp>-build/`:

```
session.md           # Master log: head=goal, tail=progress
understanding.md     # Phase 1 output
plan.md              # Phase 2 output
verify-report.md     # Phase 4 output
iteration-N/         # Per-iteration details
```

Persistent cross-session knowledge at `$HOME/.claude/build-knowledge/`:

```
$HOME/.claude/build-knowledge/
  knowledge/
    understanding.md   # Learnings for the understand phase
    planning.md        # Learnings for the plan phase
    execution.md       # Learnings for the execute phase
    verification.md    # Learnings for the verify phase
  metrics/
    sessions.jsonl     # Per-session structured metrics
    aggregate.json     # Rolling aggregate metrics
  prompt-versions/
    *.v{N}             # Versioned copies of prompt templates
    changelog.md       # Evolution history log
```

New prompt templates: `prompts/extract-knowledge.md`, `prompts/compact-knowledge.md`, `prompts/extract-metrics.md`, `prompts/evolve-prompts.md`.

Subagents isolated — state passes through `{state_dir}` files, never conversation.

## Execution Flow

```dot
digraph { rankdir=TB; node[shape=box];
  P0[shape=diamond label="P0 Contract" color=blue];
  P1[label="P1 Understand"]; P2[label="P2 Plan"];
  P3[label="P3 Execute"]; P4[shape=diamond label="P4 Verify"];
  P5[label="P5 Fix"]; CL[label="Compress Log"];
  P6[label="P6 Extract Knowledge" color=purple];
  P7[label="P7 Evolve Prompts" color=orange];
  Done[shape=oval label="Done" color=green];
  P0->P1->P2->P3->P4;
  P4->P5[label="issues"]; P5->P4[label="re-verify"];
  P4->CL[label="pass"];
  CL->P1[label="iter < N"];
  CL->P6[label="iter >= N"];
  P6->P7[label="3+ sessions"];
  P6->Done[label="<3 sessions"];
  P7->Done;
}
```

## Phase 0: Contract Confirmation (Human Gate)

1. Parse args. Create `.agent-log/<YYYY-MM-DD-HHMMSS>-build/`.
2. Init `session.md` with Goal.
3. If `--verification` omitted: analyze project, ask human to select methods.
4. Detect `$HOME/.claude/build-knowledge/` knowledge store. Classify project type as `language/framework-archetype` (e.g., `python-cli`, `react-spa`, `go-api`, `skill-modification`). Write the classification to `session.md` as `## Project Type: [type]`.
5. Write Verification Plan to `session.md`. Proceed to Phase 1.

## Phase 1: Deep Understanding

Dispatch subagent (`general-purpose`) with `./prompts/understand.md` filled: `{state_dir}`, `{references}`, `{relevant_knowledge}`.

Fill `{relevant_knowledge}` (mapped to `knowledge/understanding.md`): read `$HOME/.claude/build-knowledge/knowledge/understanding.md`, filter by project type tag, include top entries (~1500 tokens max). If file missing, empty, or malformed, set to empty string and proceed without knowledge injection. After dispatch, log to `session.md`: "Applied N entries from M sessions in understand phase." (If zero, log "No prior knowledge available for understand phase.")

Verify `understanding.md` exists. Resolve "Open Questions" if possible; otherwise log warning and proceed.

## Phase 2: Planning

Dispatch subagent (`Plan`) with `./prompts/plan.md` filled: `{state_dir}`, `{planning_knowledge}`.

Fill `{planning_knowledge}`: read `$HOME/.claude/build-knowledge/knowledge/planning.md`, filter by project type tag, include top entries (~1500 tokens max). If file missing, empty, or malformed, set to empty string and proceed without knowledge injection. After dispatch, log to `session.md`: "Applied N entries from M sessions in plan phase." (If zero, log "No prior knowledge available for plan phase.")

Verify `plan.md`: steps ordered, each has verification criterion, dependencies consistent.

## Phase 3: Execution

For each step in `plan.md`:
1. Dispatch subagent (`general-purpose`) with `./prompts/execute-step.md`: `{state_dir}`, `{step_number}`, `{execution_knowledge}`.
2. Fill `{execution_knowledge}`: read `$HOME/.claude/build-knowledge/knowledge/execution.md`, filter by project type tag, include top entries (~1500 tokens max). If file missing, empty, or malformed, set to empty string and proceed without knowledge injection. After dispatch, log to `session.md`: "Applied N entries from M sessions in execute phase." (If zero, log "No prior knowledge available for execute phase.")
3. Fail -> retry once -> if still fails, log `**FAILED**` and continue.
4. Plans >8 steps: parallelize independent steps in one message.

## Phase 4: Verification

**Before dispatching:** If `verify-report.md` already exists, move it to `verify-report-prev.md` (do not lose history).

Dispatch subagent (`general-purpose`) with `./prompts/verify.md`: `{state_dir}`, `{verification_methods}`, `{verification_knowledge}`.

Fill `{verification_knowledge}`: read `$HOME/.claude/build-knowledge/knowledge/verification.md`, filter by project type tag, include top entries (~1500 tokens max). If file missing, empty, or malformed, set to empty string and proceed without knowledge injection. After dispatch, log to `session.md`: "Applied N entries from M sessions in verify phase." (If zero, log "No prior knowledge available for verify phase.")

Read `verify-report.md`: all PASS → this iteration complete. Any FAIL/PARTIAL → Phase 5.

## Phase 5: Iteration Fix

1. Increment `fix_round` counter (starts at 1, increments each time Phase 5 runs within the same iteration).
2. Create `iteration-N/fix-round-{fix_round}/`, copy current `verify-report.md` into it as `verify-report-before.md`.
3. Dispatch subagent (`general-purpose`) with `./prompts/fix.md`: `{state_dir}`, `{iteration_number}`.
4. Return to Phase 4 (re-verify).
5. If Phase 4 finds no new issues → this iteration is complete. Go to **Iteration Loop** below.
6. If Phase 4 still finds issues but fewer than before → continue fixing (stay in Phase 5).
7. If Phase 4 finds the same or more issues for 2 consecutive fix rounds → log warning, stop fixing within this iteration. Go to **Iteration Loop**.

## Iteration Loop

**CRITICAL: Understand the two loop levels.**

```
OUTER LOOP (--iterations N):
  iteration=1,2,...N
    Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 (inner loop) → done

INNER LOOP (fix rounds within one iteration):
  Phase 4 → Phase 5 → Phase 4 → Phase 5 → ... until convergence
```

**`--iterations N` controls the OUTER loop only.** The inner loop (fix rounds) runs until convergence or the 2-round stall rule above.

### Outer loop execution:

1. Initialize `current_iteration = 1`.
2. Execute Phases 1-5 for `current_iteration`.
3. After iteration completes (Phase 5 convergence or stall):
   - If `current_iteration < N`:
     - Increment `current_iteration`.
     - If `session.md` >200 lines, dispatch compress-log subagent.
     - Start fresh Phase 1 (subagent reads compressed session.md for context).
   - If `current_iteration >= N`: stop. Proceed to Phase 6.

### Convergence detection (inner loop):

| Signal | Action |
|---|---|
| Zero new issues | Inner loop complete. Next outer iteration (if any). |
| Issues decreasing | Continue inner loop (another fix round). |
| Issues same 2 fix rounds | Warning, inner loop stall. Next outer iteration (if any). |

## Phase 6: Knowledge Extraction

Runs after the iteration loop completes (success or max iterations reached).

1. Dispatch subagent (`general-purpose`) with `./prompts/extract-knowledge.md` filled: `{state_dir}`, `{knowledge_dir}` = `$HOME/.claude/build-knowledge`. Then dispatch subagent with `./prompts/extract-metrics.md` filled: `{state_dir}`, `{knowledge_dir}`, `{skill_dir}` = `/Users/lijialun/work/engineer_skills/skills/build/`.
2. After extraction, check if any knowledge file exceeds ~200 lines; if so, dispatch compaction subagent with `./prompts/compact-knowledge.md`: `{knowledge_dir}`.

## Phase 7: Prompt Evolution (Self-Improvement)

Runs after Phase 6 if the knowledge store has 3+ sessions with metrics.

1. Check skip conditions: skip if project type is `skill-modification`, if fewer than 3 total sessions in aggregate metrics, or if knowledge files are empty/missing.
   - **Dry-run mode**: If `--dry-run` is set, Phase 7 runs in read-only mode. The evolution report is still generated (proposals, validations, and bloat warnings are computed), but no prompt files are modified, no version backups are created, and the changelog is not updated. The report will be marked as "DRY RUN".
2. Dispatch subagent (`general-purpose`) with `./prompts/evolve-prompts.md` filled: `{skill_dir}` = `/Users/lijialun/work/engineer_skills/skills/build/`, `{knowledge_dir}` = `$HOME/.claude/build-knowledge`, `{state_dir}`, `{project_type}` (from session.md), `{dry_run}` = `"true"` or `"false"` (from `--dry-run` flag).
3. The evolution agent will:
   - Analyze knowledge entries for each of the 5 core prompts
   - Generate proposals based on multi-session patterns
   - Auto-apply changes that pass the validation gate (3+ session reinforcement)
   - Propose changes for human review when evidence is weaker (2 sessions)
   - Create version backups of any modified prompts
   - Write an evolution report to `{state_dir}/evolution-report.md`
   - Acquire a lock file before modifying prompts (prevents concurrent evolution)
   - Detect manual edits to prompts and downgrade auto-apply to propose-for-review
   - Check for prompt bloat before applying (downgrade to propose-for-review if near threshold)
   - Weight knowledge entries by session outcome (failed-session entries need higher reinforcement)
   3a. **Safety mechanisms**:
      - **Lock file**: A file at `{skill_dir}/.evolution-lock` prevents two evolution agents from modifying prompts simultaneously. If the lock is older than 30 minutes, it is considered stale and removed.
      - **Manual edit detection**: Before applying changes, the agent compares the live prompt against its latest versioned backup. If the live prompt has been manually edited (differences not attributable to previous evolution), auto-apply is downgraded to propose-for-review for that prompt.
      - **Bloat prevention**: Two-tier system: pre-apply check blocks additions to prompts at 270+ lines or >40% growth from earliest version; post-apply check warns at >300 lines or >50% growth. Both downgrade to propose-for-review.
      - **Session outcome weighting**: Knowledge entries from failed sessions are given higher reinforcement weight, ensuring that lessons learned from failures are prioritized over those from successful sessions.
      - **Version metadata**: Each versioned backup includes a metadata comment recording the version number, timestamp, triggering session, and the knowledge entries that motivated the change.
4. Log the result to `session.md`: "Phase 7: [N changes applied, M proposed for review, K rejected]" or "Phase 7: Skipped [reason]".
5. If proposals-for-review exist, surface them to the human as part of the completion summary.

## Context Management

| Phase | Subagent | Notes |
|---|---|---|
| Understand | `general-purpose` | Full context + knowledge injection |
| Plan | `Plan` | Reads understanding.md + knowledge injection |
| Execute | `general-purpose`/step | One step per call + knowledge injection |
| Verify | `general-purpose` | Reads all outputs + knowledge injection |
| Fix | `general-purpose` | Reads verify-report |
| Extract Knowledge | `general-purpose` | Post-loop, reads all session files |
| Compact Knowledge | `general-purpose` | Triggered when knowledge files >~200 lines |
| Evolve Prompts | `general-purpose` | Post-extraction, reads knowledge + metrics, modifies prompts with versioning |

**Log compaction:** >200 lines -> compress. Goal/Verification Plan unchanged; older content -> Progress Summary.

## Completion

Print: iterations, remaining issues, log path. Include count of learnings extracted, count of past learnings applied, and evolution results (changes applied, proposals pending review).

## Common Mistakes

| Mistake | Fix |
|---|---|
| State via conversation | Use `{state_dir}` files |
| Skipping Phase 1 | Prevents cascading errors |
| Not logging failures | Log with `**FAILED**` marker |
| Verify only once | Always re-verify after fixes |
| Context too long | Subagents + compress at >200 lines |
| Forgetting knowledge extraction | Always run Phase 6, even on failed sessions |
| Over-injecting knowledge | Cap knowledge injection at ~1500 tokens; filter by project type |
| Modifying prompt files directly | Only modify prompts through Phase 7 evolution (versioned, validated). Manual edits are detected and may block auto-evolution for that prompt. |
| Bypassing evolution skip conditions | Phase 7 has safety gates (3+ sessions, non-skill-modification projects). Do not override these. |
| Ignoring proposals-for-review | Review proposed prompt changes surfaced in the completion summary. Dismissing them means losing potential improvements. |

## Rollback

To revert a prompt template to a previous version:
1. List versions: `ls $HOME/.claude/build-knowledge/prompt-versions/`
2. Read the version metadata comment at the top of the desired `.v{N}` file
3. Copy the version file over the live prompt: `cp {version-file} /Users/lijialun/work/engineer_skills/skills/build/prompts/{filename}`
4. The next evolution cycle will detect the manual change (the file will differ from the latest version backup) and skip auto-evolution for that prompt. To resume auto-evolution, apply the versioned backup over the live prompt, then the next evolution cycle will detect them as identical and proceed normally.
