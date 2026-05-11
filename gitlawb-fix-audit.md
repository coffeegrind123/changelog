# Gitlawb Fix Audit — openclaude gap catalog

Systematic audit of all 587 commits from [Gitlawb/openclaude](https://github.com/Gitlawb/openclaude) main branch, comparing each fix against openclaude source at `/home/openclaudeuser/openclaude/src/`.

**Audit date:** 2026-05-11  
**Session type:** Research & documentation only — no openclaude source edits  
**OC branch for implementation:** `gitlawb-fix-port`

---

## Protocol (per commit)

1. `cd /tmp/gitlawb-openclaude && git show <sha> 2>&1 | head -100` — read Gitlawb diff
2. Identify: is this a fix to source code (not doc/CI/merge/version-bump/test/build-system-only)?
3. For each changed source file, verify if it exists in `/home/openclaudeuser/openclaude/src/`
4. Read the openclaude file at the relevant lines
5. Compare: is the same bug present in openclaude? Is the fix already applied?
6. Verdict:
   - **GAP** — Fix NOT in openclaude; document here for future backport session
   - **ALREADY_HAVE** — Fix already present (via independent impl, prior backport, or different architecture solving same problem)
   - **NOT_APPLICABLE** — Gitlawb-specific code, feature (not fix), file doesn't exist in OC, build/CI/docs/merge only

**Scope note:** Windows and macOS fixes ARE in scope if the source logic applies cross-platform.

---

## Gitlawb-Specific Context

- Gitlawb is a fork of the same upstream Claude Code source as openclaude and CCB
- Gitlawb uses an "OpenAI-compatible provider shim" (`packages/openai-shim/`) — their equivalent of our `src/services/api/openaiBridge/`
- Their provider shim is architecturally different from ours — shim-specific fixes are NOT_APPLICABLE unless the same bug exists in our bridge
- Gitlawb has its own MCP server set, auto-update mechanism, and CLI entrypoints
- Pay special attention to: Bash security fixes, hook fixes, permission fixes, memory leak fixes, provider-agnostic fixes — these are the most likely GAP sources

---

## Infrastructure

- **Gitlawb repo:** `/tmp/gitlawb-openclaude` (cloned from `github.com/Gitlawb/openclaude`, main branch, 587 commits after skipping initial)
- **Openclaude src:** `/home/openclaudeuser/openclaude/src/`
- **Changelog repo:** `/tmp/changelog-repo`
- **Push credentials:** `/tmp/git-cred-helper.sh`

---

## Audit Progress

| Batch | Commit range | Status | GAPs | ALREADY_HAVE | NOT_APPLICABLE |
|-------|-------------|--------|------|-------------|----------------|
| 1 | 2-73 | [ ] | — | — | — |
| 2 | 74-146 | [ ] | — | — | — |
| 3 | 147-219 | [ ] | — | — | — |
| 4 | 220-292 | [ ] | — | — | — |
| 5 | 293-365 | [ ] | — | — | — |
| 6 | 366-438 | [ ] | — | — | — |
| 7 | 439-511 | [ ] | — | — | — |
| 8 | 512-587 | [ ] | — | — | — |

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
