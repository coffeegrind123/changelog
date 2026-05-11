# CCB Fix Audit — openclaude gap catalog

Systematic audit of every commit from [claude-code-best/claude-code](https://github.com/claude-code-best/claude-code) main branch, comparing each fix against openclaude to determine whether openclaude already has it (`ALREADY_HAVE`) or is missing it (`GAP`).

**Session type:** Research & documentation only — no edits to openclaude source.  
**Output:** This file, in `coffeegrind123/changelog`.

---

## Protocol (MUST follow for every commit)

For each CCB commit in chronological order (oldest first, skip `f90eee85`):

1. **Read CCB diff:** `cd /tmp/claude-code-ccb && git show <sha> 2>&1 | head -100`
2. **Identify:** Is this a fix to source code (not doc/CI/merge/version-bump/test/build-system-only)?
3. **Check openclaude:** For each changed source file, verify if it exists in `/home/openclaudeuser/openclaude/src/`
4. **Read the openclaude file** at the relevant lines
5. **Compare:** Is the same bug present in openclaude? Is the fix already applied?
6. **Verdict:**
   - **GAP** — Fix NOT in openclaude; document here for future backport session
   - **ALREADY_HAVE** — Fix already present (via independent impl, prior backport, or different architecture solving same problem)
   - **NOT_APPLICABLE** — CCB-specific code, feature (not fix), file doesn't exist in OC, build/CI/docs/merge only

**Scope note:** Windows and macOS fixes ARE in scope per user instruction.

---

## Infrastructure

- **CCB repo:** `/tmp/claude-code-ccb` (cloned from `github.com/claude-code-best/claude-code`, main branch, 647 commits after skipping initial)
- **Openclaude src:** `/home/openclaudeuser/openclaude/src/`
- **Changelog repo:** `/tmp/changelog-repo`
- **Push credentials:** `/tmp/git-cred-helper.sh` (uses `gh auth token`)
- **OC branch for implementation:** `ccb-fix-port` (exists in openclaude repo)

---

## Audit Progress

| Batch | Commit range | Status | GAPs found |
|-------|-------------|--------|------------|
| 1 | 2-82 | [ ] | — |
| 2 | 83-164 | [ ] | — |
| 3 | 165-246 | [ ] | — |
| 4 | 247-328 | [ ] | — |
| 5 | 329-410 | [ ] | — |
| 6 | 411-492 | [ ] | — |
| 7 | 493-574 | [ ] | — |
| 8 | 575-648 | [ ] | — |

Get any batch's commits with:
```bash
cd /tmp/claude-code-ccb && git log --oneline --reverse main | tail -n +2 | sed -n '<start>,<end>p'
```

---

## GAP Catalog

*(Populated as commits are processed)*

| # | SHA | Date | Subject | OC File(s) | What to fix | Priority |
|---|-----|------|---------|------------|-------------|----------|

---

## ALREADY_HAVE

*(Fixes found in CCB that openclaude already has)*

| # | SHA | Date | Subject | Why we already have it |
|---|-----|------|---------|------------------------|
