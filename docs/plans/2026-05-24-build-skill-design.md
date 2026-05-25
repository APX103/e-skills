# Build Skill Design

## Overview

`/e-build` — a self-driving, fully-automated, observable execution skill for Claude Code.
Single entry point. Agent autonomously executes the full cycle: understand → plan → execute → verify → iterate.
Process fully logged to `.agent-log/` for human review.

## Success Criteria

1. **Minimal human intervention** — human only interacts at Phase 0 (choose verification methods), then zero intervention.
2. **Full automation** — entire loop runs without human presence.
3. **Observable process** — `.agent-log/` contains everything the agent did, readable by humans.
4. **Universal** — works for both greenfield implementation and existing project improvement.

## Invocation

```
/e-build "<task description>" [--iterations N] [--verification "method1,method2"]
```

Parameters:
- `<task description>`: Required. What to build/improve.
- `--iterations N`: Optional, default 1. Run the full closed-loop N times. Each iteration starts a fresh subagent chain to avoid context degradation.
- `--verification`: Optional, comma-separated list of verification methods. If omitted, agent auto-detects and asks human to choose.

## Architecture

### State Persistence via File System

All state lives in files, NOT in conversation context. This is critical because:
- Long tasks will trigger context compaction (messages get summarized, detail lost).
- Subagents start with fresh context (no parent history).
- Compaction-resistant: files survive compaction, conversation doesn't.

State files:
```
.agent-log/
  <timestamp>-e-build/
    session.md          # Master log: head=goal, tail=progress, middle=steps
    understanding.md    # Phase 1 output: what the agent understood
    plan.md             # Phase 2 output: task breakdown
    verify-report.md    # Phase 4 output: verification results
    iteration-N/
      changes.md        # What was changed in iteration N
      verify-report.md  # Verification results for iteration N
```

### Master Log Format (session.md)

```markdown
# Build: <task summary>

## Goal
<Human's original task description>

## Verification Plan
<Chosen verification methods and why>

## Progress Summary
<AI-compressed summary of all iterations so far. Updated at start of each iteration.>

## Iteration 1
### Phase 1: Understand
<timestamp> — <what was understood, key findings>

### Phase 2: Plan
<timestamp> — <task breakdown>

### Phase 3: Execute
<timestamp> — <what was built/changed>

### Phase 4: Verify
<timestamp> — <verification results, pass/fail per method>

### Phase 5: Fix
<timestamp> — <what was fixed based on verification>

## Iteration 2
...
```

Key properties:
- `head` command shows goal + verification plan
- `tail` command shows latest progress
- File stays manageable: when >200 lines, agent auto-compresses older iterations into Progress Summary

## Execution Phases

### Phase 0: Contract Confirmation (Human Gate)

**This is the ONLY phase that requires human interaction.**

Agent reads the task description and any provided references (design docs, source files, test specs).

Then:
1. Analyze the task and project context.
2. Propose verification methods based on what's available:
   - Design document comparison (if design doc exists)
   - Automated testing (if test framework exists or can be set up)
   - Visual screenshot comparison (if frontend / browser-based)
   - Code self-review (always available)
   - Other task-specific methods the agent identifies
3. Ask human to select which verification methods to use.
4. Lock the contract: write goal + chosen verification methods to session.md.

If `--verification` flag was provided, skip asking and use the specified methods.

**Output**: session.md with Goal and Verification Plan sections filled.

### Phase 1: Deep Understanding

Spawn a **dedicated subagent** to deeply analyze the task.

For implementation tasks (e.g., "replicate this HTML"):
- Read and analyze all source materials (design docs, reference code, screenshots)
- Identify ALL functional requirements, not just obvious ones
- Map out interaction flows, especially non-obvious ones (JS-driven state changes, long interaction chains)
- Document edge cases and hidden behaviors
- Output: `understanding.md`

For improvement tasks (e.g., "refactor this module"):
- Analyze current codebase structure
- Identify what exists, what needs to change, what constraints exist
- Understand dependencies and impact radius
- Output: `understanding.md`

**Key principle**: The understanding agent should be thorough to the point of paranoia. Missing a requirement here costs many iterations later.

**Output**: understanding.md, log entry in session.md.

### Phase 2: Planning

Spawn a **dedicated subagent** to create an execution plan.

- Read understanding.md (NOT conversation context — files only)
- Break the work into atomic, ordered steps
- Each step should be independently verifiable
- Identify dependencies between steps
- Estimate complexity/risk per step

**Output**: plan.md, log entry in session.md.

### Phase 3: Execution

Execute the plan step by step. For each step:
- Spawn a **dedicated subagent** that reads plan.md and executes one step
- Subagent writes code, modifies files
- After each step, append a log entry to session.md with: what was done, files changed, any deviations from plan
- If a step fails or the agent encounters ambiguity, it logs the issue and continues with the next step (don't block the entire execution)

**Output**: Actual code changes, log entries in session.md.

### Phase 4: Verification

Spawn a **dedicated subagent** for each chosen verification method.

Available verification methods:

1. **Design Document Comparison**:
   - Read design doc and understanding.md
   - Compare implemented features against specified requirements
   - List: implemented correctly, implemented incorrectly, missing entirely

2. **Automated Testing**:
   - Run existing tests (if any)
   - If tests fail, analyze failures
   - Report: pass/fail per test, failure analysis

3. **Visual Screenshot Comparison** (frontend tasks):
   - Start the application
   - Use playwright/browser to capture screenshots
   - Compare against reference screenshots (if available)
   - Report: visual differences with descriptions

4. **Code Self-Review**:
   - Analyze code quality, redundancy, consistency with design
   - Check for dead code, unused imports, architectural violations
   - Report: issues found, severity, suggestions

**Output**: verify-report.md with structured results per method, log entry in session.md.

### Phase 5: Iteration Fix

If verification found issues:
1. Spawn a **dedicated subagent** that reads verify-report.md + understanding.md
2. Prioritize fixes (critical → major → minor)
3. Fix issues one by one
4. Update session.md with what was fixed

After fixes complete → go back to Phase 4 (re-verify).

**Convergence**: Each iteration should show improvement in verify-report.md.
- If verify-report shows no new issues found → declare success
- If max iteration count reached → report remaining issues and stop

### Iteration Loop

When `--iterations N > 1`:
- After iteration completes (Phase 0-5 cycle done once), compress current session.md:
  - Keep Goal and Verification Plan unchanged (head)
  - Summarize all iterations into Progress Summary
  - Start fresh Phase 1 with updated context (read session.md for what was already done)
- This prevents context accumulation across iterations

When called without `--iterations` or `--iterations 1`:
- Single execution of Phases 0-5, stops after convergence or first cycle

## Context Management Strategy (Presets)

These are the default strategies, NOT asked of the human each time:

### Subagent Sizing
- **Understanding agent**: Can be large (needs to read lots of files). Use `general-purpose` type.
- **Planning agent**: Medium. Use `Plan` type.
- **Execution agents**: One per step. Use `general-purpose` type. Keep each step small enough to fit in one subagent context.
- **Verification agents**: One per verification method. Use `general-purpose` type.

### File-Based State Protocol
- Every subagent receives a `state_dir` parameter pointing to the `.agent-log/<timestamp>-e-build/` directory
- Subagents READ state from files, WRITE results to files
- Subagents do NOT pass state back through conversation — only through files
- This makes subagents fully isolated and restartable

### Log Compaction Trigger
- When session.md exceeds 200 lines, the master agent compresses it:
  - Goal + Verification Plan: unchanged
  - Iterations older than the current one: compressed to summary
  - Current iteration: kept in detail
- Human can always read the compressed log to understand full history

### Failure Recovery
- If a subagent fails (timeout, error), log the failure and retry once with a fresh subagent
- If retry fails, log the failure and skip to the next step (with a prominent warning in the log)
- The human can review the log and manually fix + resume if needed

## Non-Goals

- NOT a replacement for human judgment on architectural decisions
- NOT a general-purpose orchestration framework
- NOT trying to solve "understanding intent perfectly" — that's an AI capability problem, not a workflow problem
- NOT trying to be clever about when to stop iterating — use simple convergence detection + max iterations

## Risks

1. **Subagent quality varies by model** — weaker models may not produce good results even with multiple iterations. Mitigation: skill works best with stronger models, but multiple iterations help weaker models converge.
2. **Verification may miss subtle issues** — especially visual/interaction nuances (as in the 30K HTML case). Mitigation: the verification plan is chosen by the human, who can add custom verification steps.
3. **Long tasks may time out** — Claude Code sessions have practical time limits. Mitigation: file-based state means work can be resumed across sessions.
4. **Context compaction may lose nuance** — even with file-based state, subagent prompts may lose detail after compaction. Mitigation: keep subagent prompts focused and reference files rather than embedding content.

## Future Evolution (Not in v1)

- `/verify` as a standalone skill (extract Phase 4)
- `/understand` as a standalone skill (extract Phase 1)
- Integration with CI/CD (e.g., trigger `/e-build` on PR)
- Historical learning: reuse understanding from previous similar tasks
- Custom verification plugins
