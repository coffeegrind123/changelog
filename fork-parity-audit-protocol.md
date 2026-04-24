# Fork Parity Audit Protocol

> Generalized procedure for auditing N external forks of Claude Code against ours. Method used to produce `fork-parity-audit.md`. Supersedes the earlier `ccb-audit-protocol.md` which handled only one fork at a time.

## Goal

Given one or more external forks (documented OR source-only), classify every distinctive feature per fork and produce a single unified comparison table with one column per fork. Output: **one** `fork-parity-audit.md` covering all forks, plus a prioritized backport backlog.

## Why this protocol exists

Single-fork audits are easy to land in a wrong state:

1. **False negatives** — a delegated agent claims "X is MISSING" based on directory-name absence. Verify every MISSING/PARTIAL before trusting it.
2. **Sampling gaps** — walking the fork's top-level directories and reading 3–4 representative files misses half the distinctive features. The inventory must be exhaustive.
3. **Incomplete categorization** — when the categories are tuned for Fork-A, Fork-B's idiosyncratic features get crammed into the wrong section or dropped. Categories must be derived AFTER enumerating all forks.

This protocol bakes verification and exhaustive enumeration into the workflow so the final table is accurate the first time.

## Every fork is source-based — verify before assuming otherwise

**Lesson from the first audit of this protocol:** I initially treated CCB as doc-based after cloning its repo into a directory I named `/tmp/ccb-docs`. That misleading directory name led me to only inspect `/tmp/ccb-docs/docs/` and never notice the repo also had `/tmp/ccb-docs/src/` (2741 TS files) and `/tmp/ccb-docs/packages/` (including native NAPI modules). The audit was redone from source once a user pointed this out.

**Rule:** after `git clone`, always run `ls /tmp/<repo>/` *once* and eyeball the top-level entries. If you see `src/`, `packages/`, or `lib/` — the fork is source-based regardless of whether it also ships a Mintlify docs site. Never let a directory naming convention decide your audit approach.

Some forks ship both. A docs catalogue (when present) is useful for *orientation* — it tells you what the maintainers think their marquee features are — but the source is the authoritative record of what actually shipped. Doc admissions of "this is a stub" can be outdated.

| Fork shape | How to handle |
|---|---|
| Source only | Enumerate `src/` exhaustively. Read `README.md`, `CHANGELOG.md`, `package.json` scripts + deps, `CLAUDE.md` / `AGENTS.md` if present. |
| Source + docs | Use docs as orientation + feature names. Verify stub / shipped / parity claims against `src/`. |
| Docs only (source truly private) | Rare. Trust the docs but flag any "stub per doc admission" row as unverified. |

## Procedure

### 1. Acquire every source-of-truth repo

```bash
git clone --depth 1 https://github.com/<fork-a>/... /tmp/fork-a
git clone --depth 1 https://github.com/<fork-b>/... /tmp/fork-b
# etc.
```

Use `--depth 1` — we only need current state. Clones take ~30s each. Run them in parallel when you have more than one.

### 2. Map each fork's catalogue surface

For each fork, start with a top-level `ls` to classify the shape — do this before ANY deeper work. If `src/` or `packages/` exists, the fork is source-based (regardless of the clone directory name you picked):

```bash
ls /tmp/fork-a/
ls /tmp/fork-b/
```

Then map the real surface:

```bash
# Source
ls /tmp/fork-a/src
command find /tmp/fork-a/src -maxdepth 2 -type d | head -80
command find /tmp/fork-a/src -type f \( -name '*.ts' -o -name '*.tsx' \) | wc -l
ls /tmp/fork-a/packages 2>/dev/null  # native NAPI modules often live here

# Docs (if present — as orientation only)
command find /tmp/fork-a/docs -name '*.md' -o -name '*.mdx' 2>/dev/null | wc -l
```

**Bash shadowing caveat:** In this harness `find` and `grep` are functions routing through the `claude` CLI and will emit "claude native binary not installed" errors. Always prepend `command ` (e.g. `command find`, `command grep`) to get the real binary. `ls`, `head`, `wc` are unaffected.

### 3. Read each fork's top-level orientation files

Every fork (whether it ships docs or not):
- Root `README.md`
- `CHANGELOG.md` — gives feature names + issue numbers
- `CLAUDE.md` / `AGENTS.md` / `PLAYBOOK.md` / `CONTRIBUTING.md` — the agent-ramp-up index is usually the tightest feature list
- `package.json` `scripts` + `dependencies` — headless modes, daemons, diagnostic scripts, native NAPI modules signal native capabilities
- `.env.example` — configurable features surfaced via env

If the fork also ships a docs site (Mintlify or similar), skim:
- `docs/features/all-features-guide.md` (or equivalent master catalogue)
- Any `CLAUDE.md` in docs too — sometimes duplicates the source one

Docs are **orientation**, not ground truth. A feature doc admitting "this is a stub" was true when written and may be out of date. Only the source decides current status.

### 4. Read OUR `CLAUDE.md` end-to-end

Our project's `CLAUDE.md` is the authoritative index of what we've shipped. **Read it cover-to-cover** before judging any feature missing. Pay close attention to:
- "Key Architecture Decisions" — individual feature paragraphs
- "Feature Notices" table — every major feature ships with a startup notice
- "Backported Features" table
- "Don't Touch" / "NEVER Do" — constraints that rule out certain backports
- The stubs table at the end of "Debugging Guide" — features where we export `null` or stubs deliberately

### 5. Exhaustive inventory per fork — delegate in parallel

Spawn one `Explore` subagent per fork. Run them concurrently (multiple `Agent` calls in a single message, `run_in_background: true`).

**Brief each agent identically except for the target path.** Each brief must require:
- Enumerate **every** subdirectory of `src/` (source-based) or **every** `.md`/`.mdx` file of `docs/` (doc-based) — no sampling
- For each file/directory, a one-line purpose inference
- Coverage of easily-missed areas: `utils/` sub-directories (not just top-level files), `services/` full list, `commands/` full list (subdir AND bare `.ts` files), `tools/` full list, plus cryptic top-level dirs (e.g. `moreright`, `native-ts`, `upstreamproxy`, `memdir`, `grpc`, `proto`, `vim`, `voice`, `remote`, `bootstrap`, `bridge`, `buddy`, `coordinator`)
- Read `package.json` scripts for headless/daemon/diagnostic modes
- Read `CHANGELOG.md` for recent distinctive features
- Output format: flat markdown bullets, not prose. No classification — just the raw catalogue
- Explicit note about the `command find` / `command grep` shadowing caveat
- Token budget: 3000–4000 words per fork

**Don't do the inventory yourself.** The subagent output goes back into your context budget as a single tool-result — leave the deep file-walking to the subagent so your own context stays clean for the final synthesis.

### 6. Verify every "MISSING" and "PARTIAL" claim

**This is the step that prevents shipping a wrong report.** After the subagents return, for every claim that a fork lacks a feature we ship (or that we lack a feature they ship), run independent verification:

```bash
# Directory / file absence check
ls /home/claudeuser/openclaude/src/services/ | command grep -i <keyword>
ls /tmp/fork-b/src/services/ | command grep -i <keyword>

# Name-variant check (features often live under non-obvious names)
command find /home/claudeuser/openclaude/src -type d -iname '*<keyword>*'
command find /tmp/fork-b/src -type d -iname '*<keyword>*'

# Spot-check actual file contents
head -30 <suspected-implementation>
```

Rough rule: ~20% of a subagent's "MISSING" claims dissolve on direct verification. Budget for this. Examples from prior audits:
- "Channels MISSING" → `src/services/mcp/channelNotification.ts` existed
- "Coordinator MISSING" → `src/coordinator/coordinatorMode.ts` + `workerAgent.ts` existed
- "LSP MISSING" → `src/services/lsp/` (full client + manager) + `src/tools/LSPTool/`
- "Context Collapse MISSING" → `src/services/contextCollapse/` shipped, CCB's doc admits theirs is stub

### 7. Skim each fork's own admission of stubs

Source-based forks often ship stub files. Doc-based forks sometimes document stubs as if shipped. Before classifying HAVE on their side:

```bash
# Doc admissions
head -40 /tmp/ccb-docs/docs/features/<feature>.md | command grep -i 'stub\|not.*implemented\|design.only\|placeholder'

# Source stubs (bodies <5 lines, export null/empty)
wc -l /tmp/fork-b/src/services/<feature>/*.ts
head -10 /tmp/fork-b/src/services/<feature>/index.ts
```

Common findings: `experimental-skill-search`, `bash-classifier`, half of a Computer Use module, half of an SSH scaffold. Flag as **STUB (symmetric)** when both forks ship the stub, or **STUB (only X)** when only one fork has it.

### 8. Derive categories AFTER enumeration

Don't pre-commit to the category schema. Enumerate every feature first, then group by natural clusters. For the three-fork audit (CCB, Gitlawb, ours) the stable categories were:

- Provider / Auth / Model routing
- Integration / Headless / IDE
- Web / Search / Fetch
- Model / Context / Token management
- Diagnostics / Observability
- Self-Healing / Automation / Hooks
- Slash commands (huge table — alphabetical)
- MCP servers (bundled + auto-install)
- Bundled skills
- Feature notices / startup UX
- Infrastructure / distribution / platform
- Miscellaneous
- Symmetric (all forks have, roughly equivalent)
- Unique-to-each-fork

### 9. Build the unified N-column comparison table

One table per category, columns:

```
| Feature | CCB | Gitlawb | openclaude | Notes / Location |
|---|---|---|---|---|
| <feature name> | ✅/⚠️/❌/— | ✅/⚠️/❌/— | ✅/⚠️/❌/— | <our path or cross-reference> |
```

Status markers:
- `✅ HAVE` — shipped and working
- `⚠️ PARTIAL` — shipped but incomplete, stubbed internals, or differs materially
- `❌ MISSING` — not present
- `⭐ UNIQUE` — only this fork has it (ours-only column — avoid in main table, use separate Unique section)
- `— N/A` — intentionally out of scope for this fork (e.g. Anthropic telemetry we neutralized)

Avoid effort estimates in the table — they're guesses. Put them in the backlog only.

### 10. Prioritized backlog

After the table stabilizes, rank the real gaps in ours. Tier structure:

- **Tier 1** — high user-visible value, gap in ours, feasible backport
- **Tier 2** — polish / parity, moderate value
- **Tier 3** — skip-or-defer with rationale (out of scope, niche, low value, or symmetric stub)

Rank by **user-visible value**, not by effort. Cite the source fork's file path as the implementation hint. Note when a gap is already scheduled in a kickoff document (e.g. `ccb-port-kickoff.md`).

### 11. Tracking completeness — the "what we have they don't" mirror

For each external fork, write a short symmetry section listing **our** unique features. This protects against tunnel vision — a fork audit can make you feel behind on everything even when you're ahead on other axes.

### 12. Output structure

Save to `fork-parity-audit.md`. Single file, covering all forks. Structure:

1. Header (date, sources, methodology pointer to this file)
2. Philosophy contrast (one paragraph per fork — what each one optimizes for)
3. Methodology note (one paragraph — acknowledge source-based vs doc-based, acknowledge verification)
4. Per-category tables (with all N+1 columns)
5. Prioritized backport backlog (Tier 1/2/3)
6. "Things WE have that [Fork A / Fork B / …] does NOT" — one subsection per external fork
7. Key takeaway — one paragraph + recommended starting point
8. Audit changelog — dated bullets tracking what was verified / backported since audit started

## Time budget

For two external forks (one doc-based, one source-based) of comparable size to upstream:
- Acquire + map: 10 min
- Read OUR `CLAUDE.md`: 10 min
- Delegate two inventory agents (parallel): 10–15 min wait
- Verify subagent claims: 45–60 min
- Derive categories + build unified table: 45 min
- Write backlog + symmetry + takeaway: 20 min
- **Total: ~3 hours**

Add 30–60 min per additional fork beyond two.

Skipping verification (step 6) saves an hour but produces a wrong report. Don't skip.

## Anti-patterns

- ❌ Trusting subagent output verbatim — every MISSING claim must be verified
- ❌ Sampling the fork's `src/` instead of exhaustive enumeration
- ❌ Pre-committing to category schema before enumeration completes
- ❌ Writing one audit file per fork and calling it done — the value is in the N-column comparison
- ❌ Forgetting to read OUR `CLAUDE.md` end-to-end
- ❌ Declaring MISSING based on directory-name absence alone
- ❌ Including features unique to us in the main table rows (use the dedicated "Unique to openclaude" section)
- ❌ Omitting the symmetry section — it calibrates expectations for the reader
- ❌ Adding effort estimates inline in the feature tables — keep them in the backlog only
- ❌ Skipping stub-admission checks — doc-based forks especially sometimes document features that haven't shipped
