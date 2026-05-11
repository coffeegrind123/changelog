# CCB-Style Fix Audit — Reusable Instructions

Use these prompts to audit any CCB-like fork (based on the same upstream Claude Code source) against openclaude. Replace placeholders in `<>` brackets.

---

## Master Prompt (to the orchestrating agent)

```
Audit all commits from <REPO_NAME> (oldest-first, skip initial commit) against openclaude.
Pure research — document every fix gap into a single file. No openclaude code edits.

### Infrastructure
- Target repo: <REPO_PATH> (already cloned)
- Openclaude src: /home/openclaudeuser/openclaude/src/
- Tracking file: /tmp/changelog-repo/<name>-fix-audit.md
- Push: cd /tmp/changelog-repo && git -c credential.helper=/tmp/git-cred-helper.sh push

### Protocol (per commit)
1. git show <sha> 2>&1 | head -100 — read diff
2. If doc/CI/merge/version-bump/test/build-only → NOT_APPLICABLE, next
3. If source change: Read the openclaude file at the relevant lines
4. Compare — same bug present? Fix already applied?
5. Verdict: GAP / ALREADY_HAVE / NOT_APPLICABLE
6. For each GAP: add row to audit file with SHA, date, subject, OC files, what to fix, priority

### Approach
First run `cd <REPO_PATH> && git log --oneline --reverse main | tail -n +2 | wc -l` for commit count.
Divide into batches of ~80. Launch one agent per batch.

### After all batches complete
Read all batch output files. Extract every GAP. Classify into priority tiers:
- CRITICAL: memory leaks, crashes, API 400 errors, security, broken core features
- HIGH: missing guards/params, feature gaps, unbounded growth, architectural divergence
- MEDIUM: correctness fixes, optimizations, UX improvements
- LOW: minor polish, model name updates, cosmetic fixes
Compile into <name>-fix-audit.md. Commit ALL batch files + master file, push.
```

---

## Agent Prompts (one per batch of ~80 commits)

**Agent N (commits X–Y):**

```
CRITICAL PROTOCOL — find fixes openclaude is MISSING. Research only, NO edits to openclaude.

Working dirs: target at <REPO_PATH>, openclaude at /home/openclaudeuser/openclaude/src/

Get your commits:
  cd <REPO_PATH> && git log --oneline --reverse main | tail -n +2 | sed -n 'X,Yp'

For EVERY commit in that list:
1. cd <REPO_PATH> && git show <sha> 2>&1 | head -100 — read the diff
2. EXTRACT CHANGED FILES from the diff header (lines like `diff --git a/path/to/file.ts ...`
   or `--- a/path/to/file.ts`)
3. If ALL changed files are doc/CI/config/merge/version/test/build-only → NOT_APPLICABLE, skip
4. If ANY changed file is source code (src/ or packages/ with .ts/.tsx/.js extension):
   a. Find the corresponding file in /home/openclaudeuser/openclaude/src/
   b. Use Read tool to read the relevant lines — DO NOT skip this step
   c. Compare the fixed code vs openclaude's current code
   d. Verdict: GAP (bug exists in OC, fix not applied) /
      ALREADY_HAVE (fix already present) /
      NOT_APPLICABLE (repo-specific feature, file doesn't exist in OC, platform-specific)

IMPORTANT RULES:
- You MUST Read() the openclaude source file at the relevant lines.
  Checking file existence is not enough.
- Compare actual code, not just commit subject lines.
- Windows/macOS fixes ARE in scope if the source logic would apply on Linux.
- If the fix is in a file that doesn't exist in openclaude but the same concern
  exists, flag as GAP with a note.
- If the fix is to a repo-specific subsystem (Langfuse, specific provider adapter,
  unique package), mark NOT_APPLICABLE.
- If openclaude solves the same problem via different architecture,
  mark ALREADY_HAVE and explain why.
- Smaller batches (≤50) work better than larger ones. If your batch is >80 commits,
  flag the overload and request a split.

OUTPUT FORMAT — use this EXACT format for every commit (one line):

  SHA | SUBJECT | VERDICT | OC_FILE:LINE | WHAT_THE_FIX_DOES

At the end, add a summary section:

## Summary
Total: N commits. GAP: X, ALREADY_HAVE: Y, NOT_APPLICABLE: Z.

### GAPs found (priority order):
1. **SHA** — One-line description. OC file: path:line. Fix: what to change.
2. ...

Write complete output to /tmp/<name>-gap-batchN.md
DO NOT edit openclaude files. Research only.
```

---

## Compilation Prompt (after all agents complete)

```
All audit agents have completed. Compile results:

1. Read /tmp/<name>-gap-batch1.md through /tmp/<name>-gap-batchN.md
2. Extract every GAP entry (not ALREADY_HAVE, not NOT_APPLICABLE)
3. Read /tmp/changelog-repo/<name>-fix-audit.md for the current structure
4. Classify GAPs into priority tiers:
   - CRITICAL: memory leaks, crashes, API 400 errors, security issues, broken core features
   - HIGH: missing guards/params, feature gaps, unbounded growth, architectural divergence
   - MEDIUM: correctness fixes, optimizations, UX improvements
   - LOW: minor polish, model name updates, cosmetic fixes
5. Add all GAP entries to the GAP Catalog table with SHA, batch#, subject,
   OC file(s), what to fix, priority
6. Add all ALREADY_HAVE entries to that table (with why we already have it)
7. Update the Audit Progress table (mark all batches done)
8. Copy all batch files to the changelog repo
9. Commit and push:
   cd /tmp/changelog-repo && git add -A && git commit -m "<name> fix audit: N GAPs" && git -c credential.helper=/tmp/git-cred-helper.sh push
```

---

## Audit File Skeleton

Create `/tmp/changelog-repo/<name>-fix-audit.md` with this structure before launching agents:

```markdown
# <Name> Fix Audit — openclaude gap catalog

Systematic audit of all commits from <REPO_URL> main branch.

**Audit date:** YYYY-MM-DD
**Session type:** Research & documentation only
**OC branch for implementation:** <branch-name>

---

## [Copy protocol from ccb-fix-audit.md]

---

## Infrastructure

- **Target repo:** <REPO_PATH>
- **Openclaude src:** /home/openclaudeuser/openclaude/src/
- **Changelog repo:** /tmp/changelog-repo
- **Push credentials:** /tmp/git-cred-helper.sh

---

## Audit Progress

| Batch | Commit range | Status | GAPs |
|-------|-------------|--------|------|
| 1 | 2-82 | [ ] | — |
| 2 | 83-164 | [ ] | — |
| ... | ... | ... | ... |

---

## Priority Summary

| Priority | Count | Criteria |
|----------|-------|----------|
| CRITICAL | — | Memory leaks, crashes, API errors, security, broken core features |
| HIGH | — | Missing guards/params, feature gaps, unbounded growth, architectural divergence |
| MEDIUM | — | Correctness fixes, optimizations, UX improvements |
| LOW | — | Minor polish, model name updates, cosmetic fixes |

---

## CRITICAL GAPs

| # | SHA | B | Subject | OC File(s) | What to fix |
|---|-----|---|---------|------------|-------------|

---

## HIGH Priority GAPs

| # | SHA | B | Subject | OC File(s) | What to fix |
|---|-----|---|---------|------------|-------------|

---

## MEDIUM Priority GAPs

| # | SHA | B | Subject | OC File(s) | What to fix |
|---|-----|---|---------|------------|-------------|

---

## LOW Priority GAPs

| # | SHA | B | Subject | OC File(s) | What to fix |
|---|-----|---|---------|------------|-------------|

---

## ALREADY_HAVE

| # | SHA | B | Subject | Why we already have it |
|---|-----|---|---------|------------------------|

---

## Implementation Notes

*(Populated after audit)*
```

---

## Lessons from the CCB Audit (2026-05-11)

1. **Agents MUST Read() files, not just check existence.** In a prior failed attempt, agents checked `ls` output and assumed code differences from file paths alone — 80% false negatives. The Read step is non-negotiable.

2. **Per-commit line format must be consistent.** Each batch should use `SHA | SUBJECT | VERDICT | OC_FILE:LINE | NOTES`. Structured output makes compilation scriptable. Batch 8 used a different format which required manual extraction.

3. **Smaller batches work better.** ~80 commits per agent takes 10-15 minutes. If commits are dense (many source changes), split to ~50. Batch 4 took the longest (18 minutes) because commits 247-328 had the highest source-change density.

4. **Kill agents that check file existence without reading.** If you see an agent doing `ls`/file-exists checks without Read calls, kill it and restart with a stronger prompt.

5. **Windows/macOS fixes ARE in scope.** Several GAPs came from platform-specific fixes that had generalizable logic (CRLF parsing, terminal ESC sequences, stdin listener cleanup).

6. **Feature gates from `bun:bundle` cause silent DCE in source mode.** When comparing code, remember that openclaude's `feature('X') ? require : null` pattern evaluates to null when running from Bun source. CCB uses `process.env.USER_TYPE` or `from 'bundle'` for runtime evaluation. This difference creates false GAPs if not accounted for.

7. **Provider-boundary checks are the most common CRITICAL gap type.** Any code that gates on `isFirstPartyAnthropicBaseUrl()` or sends Anthropic-specific headers/betas/params needs verification against non-Anthropic endpoints (z.ai, DeepSeek, NIM).

8. **Compile GAPs manually for priority classification.** Auto-classification by keyword matching is too crude. Read the batch reports and classify based on the agents' detailed analysis, not scripted heuristics.
