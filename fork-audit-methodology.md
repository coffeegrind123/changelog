# Fork Audit Methodology — CCB + Gitlawb playbook

Reusable methodology for auditing any Claude Code fork (CCB-like or Gitlawb-like)
against openclaude. Captures everything learned across two completed audits
(CCB 647 commits / 66 GAPs / 58 closed; Gitlawb 587 commits / 94 GAPs /
75 closed) so the next fork audit can skip the trial-and-error and run the
proven pipeline end-to-end.

This document is a peer to `ccb-fix-audit.md` and `gitlawb-fix-audit.md` —
those are the *output* catalogs; this is the *process* that produces them.

---

## The three-phase pipeline

Every fork audit runs through these phases in order. Skipping or reordering
phases produces false negatives or duplicate work.

```
Phase 1: RESEARCH         → produces <name>-fix-audit.md (GAP catalog)
   ↓
Phase 2: IMPLEMENTATION   → produces N commits on openclaude:main
   ↓
Phase 3: TRUST-BUT-VERIFY → upgrades some SKIPs to LANDED ports
```

**Time budget per phase** (based on CCB + Gitlawb actuals):
- Phase 1: 8 parallel agents × ~12 min each = ~1.5 h wall-clock + 10 min compile
- Phase 2: 10–15 batched commits over ~3–4 h (smoke-test + hot-patch per batch)
- Phase 3: 1 verification agent + 5–8 follow-up edits over ~45 min

---

## Phase 1: Research (parallel batch agents)

Eight (or N) agents process disjoint ranges of the fork's commit history.
Each agent emits a per-commit verdict to a batch file. After all complete, a
single compilation pass merges batches into the master audit doc.

### 1a. Setup (orchestrating agent, before launching workers)

```bash
# Clone target fork
git clone https://github.com/<org>/<repo>.git /tmp/<name>-openclaude

# Verify changelog repo is current
cd /tmp/changelog-repo && git pull

# Count commits (excluding initial)
cd /tmp/<name>-openclaude && git log --oneline --reverse main | tail -n +2 | wc -l
```

Divide commit count by 8 for batch size. CCB had 647 → 81/batch; Gitlawb had
587 → 73/batch. Aim for ~80 commits per agent; if commits are unusually
source-change-dense (Batch 4 in CCB was the worst), drop to ~50.

Pre-create the skeleton `/tmp/changelog-repo/<name>-fix-audit.md` (template
in §5 below).

### 1b. Master orchestration prompt

This is what you send to the *orchestrating* agent — the one that launches
the 8 batch agents in parallel:

```
Audit all <N> commits from <REPO_URL> main branch, oldest-first, skip initial
commit. Pure research — document every fix gap into a single file. NO openclaude
code edits.

### Infrastructure (already set up)
- Target repo: /tmp/<name>-openclaude (already cloned)
- Openclaude src: /home/<user>/openclaude/src/
- Tracking file: /tmp/changelog-repo/<name>-fix-audit.md (skeleton ready)
- Push: cd /tmp/changelog-repo && git push
- OC branch: <branch-name>

### Protocol (per commit)
1. git show <sha> 2>&1 | head -100 — read diff
2. If doc/CI/merge/version-bump/test/build-only → NOT_APPLICABLE, next
3. If source change: Read the openclaude file at /home/<user>/openclaude/src/
4. Compare — is the same bug present? Is the fix already applied?
5. Verdict: GAP (missing) / ALREADY_HAVE / NOT_APPLICABLE
6. For each GAP: add row with SHA, date, subject, OC files, what to fix, priority

### Approach
Launch 8 agents, each processing ~73 commits. After all complete, compile into
the master tracking file, commit, push.

### Agent batch commands
Batch 1:  git log --oneline --reverse main | tail -n +2 | sed -n '1,73p'
Batch 2:  git log --oneline --reverse main | tail -n +2 | sed -n '74,146p'
[…continue for batches 3-8…]

### Fork-specific notes
- <One paragraph: what this fork is, what's their equivalent of our openaiBridge,
  what subsystems they add that we don't have, what to mark NOT_APPLICABLE>
- Pay special attention to: Bash security fixes, hook fixes, permission fixes,
  memory leak fixes, provider-agnostic fixes
```

### 1c. Per-agent (worker) prompt

This is what each of the 8 batch agents gets. Each batch differs only in the
`sed -n 'X,Yp'` range and the output filename. Otherwise identical.

```
CRITICAL PROTOCOL — find fixes openclaude is MISSING. Research only, NO edits
to openclaude.

Working dirs: target at /tmp/<name>-openclaude, openclaude at /home/<user>/openclaude/src/

Get your commits:
  cd /tmp/<name>-openclaude && git log --oneline --reverse main | tail -n +2 | sed -n 'X,Yp'

For EVERY commit in that list:
1. cd /tmp/<name>-openclaude && git show <sha> 2>&1 | head -100 — read the diff
2. EXTRACT CHANGED FILES from the diff header (lines like `diff --git a/path/to/file.ts ...`)
3. If ALL changed files are doc/CI/config/merge/version/test/build-only → NOT_APPLICABLE, skip
4. If ANY changed file is source code (src/ or packages/ with .ts/.tsx/.js):
   a. Find the corresponding file in /home/<user>/openclaude/src/
   b. Use Read tool to read the relevant lines — DO NOT skip this step
   c. Compare the fixed code vs openclaude's current code
   d. Verdict: GAP (bug exists in OC, fix not applied)
              / ALREADY_HAVE (fix already present)
              / NOT_APPLICABLE (repo-specific feature, file doesn't exist in OC, platform-specific)

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

### 1d. Compilation prompt (after all 8 agents complete)

```
All audit agents have completed. Compile results:

1. Read /tmp/<name>-gap-batch1.md through /tmp/<name>-gap-batch8.md
2. Extract every GAP entry (not ALREADY_HAVE, not NOT_APPLICABLE)
3. Read /tmp/changelog-repo/<name>-fix-audit.md for the current skeleton
4. Classify GAPs into priority tiers:
   - CRITICAL: memory leaks, crashes, API 400 errors, security, broken core features
   - HIGH: missing guards/params, feature gaps, unbounded growth, architectural divergence
   - MEDIUM: correctness fixes, optimizations, UX improvements
   - LOW: minor polish, model name updates, cosmetic fixes
5. Add all GAP entries to the GAP Catalog tables with SHA, batch#, subject,
   OC file(s), what to fix, priority
6. Add all ALREADY_HAVE entries to the ALREADY_HAVE table (with why we already have it)
7. Update the Audit Progress table (mark all batches done with counts)
8. Copy all 8 batch files to /tmp/changelog-repo/
9. Commit and push:
   cd /tmp/changelog-repo && git add -A && git commit -m "<name> fix audit: N GAPs" && git push
```

---

## Phase 2: Implementation pass

After the audit catalog is ready, work through it in priority order. The
**implementation prompt** for a fresh session looks like this:

```
Read coffeegrind123/changelog:<name>-fix-audit.md and start the <name>
implementation pass. The audit research is already done — the file lists
~N GAPs across CRITICAL/HIGH/MEDIUM/LOW. Use the same methodology that closed
the prior pass (see ccb-fix-audit.md "Implementation Status" section for the
model): commit-per-fix on main, hot-patch the openclaude-interactive
container after every edit, smoke-test against z.ai with `-p "say ok"`,
update CHANGELOG.md for every commit, and run a trust-but-verify pass before
declaring done. When finished, add an Implementation Status section to
<name>-fix-audit.md mirroring the CCB doc, then delete the per-batch
research files leaving only the consolidated audit doc.
```

### 2a. Workflow per fix

```
1. Read gap row → understand fix
2. Read OC source at the cited file:line to confirm gap
3. Edit
4. bun build src/entrypoints/cli.tsx --target=bun   (must exit 0)
5. docker cp <file> openclaude-interactive:/opt/openclaude-src/<file>
6. docker exec openclaude-interactive bash -c \
     'cd /opt/openclaude-src && IS_SANDBOX=1 timeout 30 bun run \
      src/entrypoints/cli.tsx -p "say ok" --dangerously-skip-permissions'
7. git add <file> && git commit -m "..."
8. Edit /tmp/changelog-repo/CHANGELOG.md (today's section, top of file)
9. cd /tmp/changelog-repo && git pull --rebase && git add CHANGELOG.md \
     && git commit && git push
10. git push (openclaude)
```

### 2b. Batching strategy

Batch related fixes into one commit when they touch the same file or share
a theme — keeps the changelog readable. Counter-examples that proved the
batching rule:

- `1594427` (CCB) — 3 *unrelated* safety fixes batched correctly because all
  three were trivial one-liner guards landing on the same release.
- `e2940e0` (CCB) — 5 MEDIUM ports across 5 different files; readable as a
  themed group ("medium-priority hardening").
- `69a21bb` (Gitlawb) — 4 CRITICAL bash-security fixes in one commit; all
  touched src/tools/BashTool/ files and shared the security theme.

When NOT to batch:
- A fix that needs careful smoke testing on its own (large refactor, new helper).
- Fixes that touch independent subsystems with no shared theme (auth + UI + retry).
- Fixes whose changelog descriptions don't fit on one bullet without losing detail.

### 2c. Status markers for unimplemented items

When a gap can't / shouldn't land as a verbatim port:

- `VERIFIED-SKIP` — checked the target fork's actual source; intentional
  architectural divergence or already-correct-in-OC. Required: brief reason.
- `DEFERRED` — substantial port deferred for future work. Required: scope
  estimate (LOC, file count) and rationale.
- `PARTIAL` — partial fix landed; full target shape deferred. Required:
  what's done and what's missing.

Every CRITICAL must land. HIGH should land unless there's a strong reason.
MEDIUM/LOW can SKIP/DEFER with documented rationale.

---

## Phase 3: Trust-but-verify

The audit's one-line "What to fix" descriptions are sometimes wrong (audit
agent misread the diff) or under-specified (fix has a non-obvious shape).
After the bulk implementation pass, run one verification agent that:

1. Clones the target fork (shallow, depth=50 is enough).
2. For each item marked SKIP or DEFERRED, opens the cited Gitlawb/CCB file
   and reads the actual fix.
3. Reports back with one of:
   - `CORRECT_SKIP — <reason confirmed in source>`
   - `LAND_AS_PORT — <one-line summary of actual fix shape we should port>`
   - `LANDED_OK — <our implementation matches their shape>`
   - `LANDED_DIVERGES — <what they do differently and whether it matters>`

CCB pass converted 3 of 7 skips to ports this way. Gitlawb pass converted
6 of 12 skips. The verification step is *not optional* — both audits had
material false negatives the audit agent introduced.

### Trust-but-verify prompt

```
Trust-but-verify pass for <name> fork port. I just landed ~M fixes from an
N-item audit against openclaude, and need you to verify the items I
VERIFIED-SKIPped or didn't land, against the actual source at /tmp/<name>/.

Context: The audit catalog is at /tmp/changelog-repo/<name>-fix-audit.md.
My openclaude tree is at /home/<user>/openclaude. For SKIPs I marked, your
job is to:
(a) find the actual <name> commit/file to confirm whether the divergence
    claim is correct
(b) flag any that are real bugs we should still port.

Items I skipped that warrant re-verification:
<list of skip-IDs with file paths to check>

Items I might have implemented incorrectly:
<list of port-IDs where the audit description was vague>

Report format: For each item, one of:
- CORRECT_SKIP — <reason confirmed in source>
- LAND_AS_PORT — <one-line summary of target's fix shape we should port>
- LANDED_OK — <confirms our implementation matches target's shape>
- LANDED_DIVERGES — <what target does differently and whether it matters>

Keep the whole report under 500 words. Actionable conclusions only.
```

---

## Phase 4: Close-out

After Phase 3 lands the verification-driven follow-ups:

1. Add an `Implementation Status` section to `<name>-fix-audit.md` mirroring
   CCB's format: per-gap rows with status + commit SHA, plus a chronological
   commits-to-items index, plus a Trust-but-verify summary.
2. Delete the per-batch research files (`<name>-gap-batch{1..8}.md`) and any
   session-prompt files. Everything actionable is in the consolidated audit doc.
3. Commit + push the changelog repo. Final state should be clean: only the
   canonical files remain (`BACKLOG.md`, `CHANGELOG.md`, prior audit docs,
   `fork-parity-audit.md`).

---

## Concrete session prompts that worked

The two completed audits used essentially identical structure with
fork-specific notes. Reproduced here verbatim for direct reuse.

### CCB-style session prompt

Used for the 2026-05-11 CCB audit of `github.com/claude-code-best/claude-code`:

```
Audit all <N> commits from CCB (github.com/claude-code-best/claude-code, main
branch, oldest-first, skip initial commit) against openclaude. Pure research —
document every fix gap into a single file. No openclaude code edits.

[infrastructure block as in §1b above]
[protocol block as in §1b above]
[approach block as in §1b above]

### CCB-specific notes
- CCB is a fork of the same upstream Claude Code source we forked.
- Their multi-provider routing lives in src/utils/auth.ts +
  src/utils/model/providers.ts — comparable to our z.ai/DeepSeek/NIM wiring.
- CCB has its own KAIROS-equivalent assistant mode (look for "assistant"
  references in commit messages) — many additions there map cleanly to our
  src/assistant/.
- CCB removes the upstream LangFuse/Statsig telemetry stack — same as us, mark
  ALREADY_HAVE.
- Pay special attention to: prompt-cache hit-rate detection, conditional hook
  violations, memory-overflow trio fixes, third-party API user_id sanitization.

[8 agent batch prompts, identical to §1c except for sed range and filename]
```

### Gitlawb-style session prompt

Used for the 2026-05-11 Gitlawb audit of `github.com/Gitlawb/openclaude`:

```
Audit all 587 Gitlawb commits (github.com/Gitlawb/openclaude, main branch,
oldest-first, skip initial d2542c9) against openclaude. Pure research —
document every fix gap into a single file. No openclaude code edits.

[infrastructure block as in §1b above]
[protocol block as in §1b above]
[approach block as in §1b above]

### Gitlawb-specific notes
- Gitlawb is ALSO a fork of the same upstream Claude Code source as openclaude
  and CCB.
- Gitlawb uses an "OpenAI-compatible provider shim" for multi-provider support —
  this is their equivalent of our openaiBridge.
- Their provider shim is in packages/openai-shim/ (separate from our
  src/services/api/openaiBridge/).
- Many Gitlawb commits will be their own feature additions or shim-specific
  fixes — mark these NOT_APPLICABLE.
- Gitlawb may have fixed bugs that exist in openclaude's equivalent code paths —
  those ARE gaps.
- Gitlawb has its own MCP server set (different from ours), its own auto-update
  mechanism, its own CLI entrypoints.
- Pay special attention to: Bash security fixes, hook fixes, permission fixes,
  memory leak fixes, provider-agnostic fixes.

[8 agent batch prompts, identical to §1c except for sed range and filename]
```

---

## Audit file skeleton

Pre-create this at `/tmp/changelog-repo/<name>-fix-audit.md` *before* launching
agents. The compilation step fills in the empty tables.

```markdown
# <Name> Fix Audit — openclaude gap catalog

Systematic audit of all <N> commits from [<repo-name>](<repo-url>) main branch,
comparing each fix against openclaude source at /home/<user>/openclaude/src/.

**Audit date:** YYYY-MM-DD
**Session type:** Research & documentation only — no openclaude source edits
**OC branch for implementation:** main
**Total GAPs found:** TBD across 8 batches

---

## Audit Progress

| Batch | Commit range | Status | GAPs | ALREADY_HAVE | NOT_APPLICABLE |
|-------|-------------|--------|------|-------------|----------------|
| 1 | 2-73   | [ ] | — | — | — |
| 2 | 74-146 | [ ] | — | — | — |
| 3 | 147-219| [ ] | — | — | — |
| 4 | 220-292| [ ] | — | — | — |
| 5 | 293-365| [ ] | — | — | — |
| 6 | 366-438| [ ] | — | — | — |
| 7 | 439-511| [ ] | — | — | — |
| 8 | 512-587| [ ] | — | — | — |

---

## Priority Summary

| Priority | Count | Criteria |
|----------|-------|----------|
| CRITICAL | — | Memory leaks, crashes, API 400 errors, security, broken core features |
| HIGH     | — | Missing guards/params, feature gaps, unbounded growth, architectural divergence |
| MEDIUM   | — | Correctness fixes, optimizations, UX improvements |
| LOW      | — | Minor polish, model name updates, cosmetic fixes |

---

## CRITICAL GAPs

| # | SHA | B | Subject | OC File(s) | What to fix |
|---|-----|---|---------|------------|-------------|

## HIGH Priority GAPs

| # | SHA | B | Subject | OC File(s) | What to fix |
|---|-----|---|---------|------------|-------------|

## MEDIUM Priority GAPs

| # | SHA | B | Subject | OC File(s) | What to fix |
|---|-----|---|---------|------------|-------------|

## LOW Priority GAPs

| # | SHA | B | Subject | OC File(s) | What to fix |
|---|-----|---|---------|------------|-------------|

## ALREADY_HAVE

| # | SHA | B | Subject | Why we already have it |
|---|-----|---|---------|------------------------|

---

## Implementation Notes

*(Populated after audit. Order: First pass CRITICAL → Second pass HIGH →
Third pass MEDIUM → Fourth pass LOW.)*
```

After Phase 2 + 3, add an `Implementation Status` section with per-gap rows +
SHAs (see `ccb-fix-audit.md` lines 42–175 or `gitlawb-fix-audit.md` lines 22–225
for the exact format).

---

## Lessons learned (cross-audit)

Carried forward from both CCB (2026-05-11) and Gitlawb (2026-05-11). Order is
"most likely to bite you on the next audit" first.

1. **Agents MUST `Read()` files, not just check existence.** In an early
   failed CCB attempt, agents checked `ls` output and inferred code differences
   from file paths alone — 80% false negatives. The `Read()` step is
   non-negotiable. If you see an agent doing existence checks without reading,
   kill it and restart with a stronger prompt.

2. **Per-commit line format must be consistent.** Each batch should use
   `SHA | SUBJECT | VERDICT | OC_FILE:LINE | NOTES`. Structured output makes
   compilation scriptable. CCB Batch 8 used a different format and required
   manual extraction.

3. **Smaller batches work better.** ~80 commits per agent takes 10–15 min. If
   commits are unusually source-change-dense (CCB Batch 4 was the worst), drop
   to ~50. Above 80 the agent's working memory degrades and the verdicts get
   sloppy.

4. **Windows/macOS fixes ARE in scope.** Several CCB GAPs came from
   platform-specific fixes that had generalizable logic (CRLF parsing,
   terminal ESC sequences, stdin listener cleanup). Don't auto-mark
   platform-tagged commits as NOT_APPLICABLE.

5. **Feature gates from `bun:bundle` cause silent DCE in source mode.** When
   comparing code, remember that openclaude's `feature('X') ? require : null`
   pattern evaluates to `null` when running from Bun source. CCB and Gitlawb
   use different gate patterns; the difference creates false GAPs if not
   accounted for. See `CLAUDE.md` "Bun `bun:bundle` DCE behavior" section.

6. **Provider-boundary checks are the most common CRITICAL gap type.** Any
   code that gates on `isFirstPartyAnthropicBaseUrl()` or sends
   Anthropic-specific headers/betas/params needs verification against
   non-Anthropic endpoints (z.ai, DeepSeek, NIM). Both audits found 3+ of these.

7. **Compile GAPs manually for priority classification.** Auto-classification
   by keyword matching is too crude. Read the batch reports and classify based
   on the agents' detailed analysis, not scripted heuristics. "API error" is
   not always CRITICAL — a niche 400 on a config-only path is MEDIUM at best.

8. **The implementation pass needs hot-patching to surface bugs.** Building
   and committing without `docker cp <file> openclaude-interactive:...` plus
   `-p "say ok"` smoke test missed several stub-export regressions during
   early CCB implementation. Treat the hot-patch + smoke step as
   non-optional, exactly like the build step.

9. **Trust-but-verify is not optional.** Both audits had material false
   negatives. CCB: 3 of 7 SKIPs were real bugs after source verification.
   Gitlawb: 6 of 12. Budget ~45 min for the verification pass + ~2 h for the
   follow-up edits.

10. **Document SKIPs with concrete rationale, not "complex".** "Substantial
    port, deferred" without LOC estimate and impact analysis just kicks the
    can. Either commit to a scope estimate or land the port. The
    Implementation Status section in both audits is the contract that
    prevents drift.

11. **Stub-export crashes look like REPL fallback or "Element type is
    invalid".** When implementation pass adds a feature that touches the
    tools or commands registry, smoke-test interactive mode (not just `-p`),
    or you'll miss the rendering failures. See `CLAUDE.md` "REPL enters
    fallback mode" debugging guide.

12. **Changelog updates must accompany every commit.** Not at the end. The
    public release-notes system fetches from the changelog repo and the
    "between deploys" gap is what users notice. CCB's 22-commit batch had a
    3-day changelog catch-up that produced a confusingly-ordered set of
    bullets.

---

## Cross-audit outcomes

| Metric | CCB (2026-05-11) | Gitlawb (2026-05-11) |
|--------|------------------|----------------------|
| Source commits audited | 647 | 587 |
| GAPs identified | 66 | 94 |
| CRITICAL | 14 (all landed) | 13 (all landed) |
| HIGH | 18 (14 landed, 3 verified-skip, 1 deferred) | 20 (all landed) |
| MEDIUM | 22 (17 landed, 4 verified-skip, 1 deferred) | 29 (16 landed, 4 verified-skip, 9 deferred) |
| LOW | 12 (9 landed, 3 verified-skip) | 31 (10 landed, 5 verified-skip, 16 deferred) |
| Trust-but-verify upgrades | 3 (of 7 candidates) | 6 (of 12 candidates) |
| Total closed (landed + verified-skip) | 58 / 66 | 75 / 94 |
| Total LANDED commits on openclaude:main | 21 | 10 |
| Implementation pass wall-clock | ~6 hours | ~5 hours |

The deferred items are the natural backlog for a future audit refresh — they
fall into one of three buckets:

- **Architectural ports** (`CCB #26 Unified Tool Search`, `Gitlawb #41
  bracket balancer`, `Gitlawb #52 continuation nudge`): substantial multi-file
  diffs that need their own design pass.
- **UX polish** (most LOW deferrals): cosmetic items where the cost / benefit
  doesn't justify the implementation cost during the main audit pass.
- **Niche subsystems** (`Gitlawb #92 PasswordVault`): Windows-specific or
  enterprise-specific features we don't exercise.

---

## Reusing this for the next fork audit

1. Find a fork worth auditing — typically one that's actively patching the
   same upstream Claude Code source and has been ahead of us on at least one
   subsystem.
2. Copy this file, fill in `<name>` and fork-specific notes (§1b "Fork-specific
   notes" block).
3. Pre-create `/tmp/changelog-repo/<name>-fix-audit.md` from the skeleton.
4. Launch Phase 1 with 8 parallel batch agents.
5. Compile. Implement. Trust-but-verify. Close out.
6. Update this document's "Cross-audit outcomes" table with the new fork's
   numbers — every audit refines the time estimates and lessons.

The methodology is stable across the two completed runs. The fork-specific
details are the variable; everything else is the constant.
