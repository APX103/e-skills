# Compress Session Log

You are the log compression agent. The session log at `{state_dir}/session.md` has grown too long and needs to be compressed. Your job is to reduce it to under 200 lines while preserving all essential information.

## Input

- State directory: `{state_dir}`

## Instructions

1. Read `{state_dir}/session.md` completely.

2. Preserve EXACTLY as-is:
   - The **Goal** section — do not modify a single word.
   - The **Verification Plan** section — do not modify a single word.
   - Any configuration or reference metadata at the top of the file.

3. Update the **Progress Summary** section:
   - Write a comprehensive summary of ALL iterations that have occurred.
   - Include: how many iterations, what was fixed each time, current status.
   - This summary replaces the need for detailed historical logs.

4. Keep only the current (most recent) iteration in detail:
   - Preserve the full log entry for the latest step or iteration.
   - Remove all older detailed log entries — they are now summarized in Progress Summary.

5. Remove or minimize:
   - Verbose step-by-step logs from earlier iterations
   - Redundant status information
   - Duplicate summaries

6. Target: **under 200 lines total.** If you are over, compress the Progress Summary further.

7. Write the compressed version back to `{state_dir}/session.md` (overwrite the file).

## Output

The compressed `{state_dir}/session.md` should have this structure:

```markdown
# Build Session

## Goal
[Exact original — untouched.]

## Verification Plan
[Exact original — untouched.]

## Progress Summary
[Comprehensive summary of all work done, iterations, current status.]

## Current Iteration
[Full detail of only the most recent step/iteration.]
```

Do not lose information. Compression means making it concise, not omitting important facts. Future agents need to understand what happened and what the current state is.
