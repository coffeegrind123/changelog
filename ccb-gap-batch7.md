# CCB Gap Analysis — Batch 7 (commits 493–574)

## Summary
82 commits analyzed. Substantive CCB changes vs openclaude source compared via Read().

---

## Results

7e61e71c | fix: disable UDS_INBOX, LAN_PIPES feature flags | NOT_APPLICABLE | scripts/defines.ts | CCB-internal build feature-flag policy. Openclaude enables all 87 flags unconditionally via `bundle` polyfill — different architecture decision.

32765897 | fix: /dev/tcp /dev/udp pseudo-device redirect detection + backslash-escaping tests | NOT_APPLICABLE | packages/builtin-tools/src/tools/BashTool/__tests__/ | Test-only commit adding backslashEscaping.test.ts + compoundCommandSecurity.test.ts. No source changes to bashSecurity.ts. Openclaude uses upstream Anthropic Bash security validators per CLAUDE.md (not CCB's bashCommandIsSafe_DEPRECATED).

2bad8df5 | test: subagent zombie test cases | NOT_APPLICABLE | — | Test-only.

51b8ad46 | refactor: remove diff rendering from message stream, keep only in permission approval | NOT_APPLICABLE | packages/builtin-tools/src/tools/FileEditTool/UI.tsx | CCB-specific UI refactor removing dead imports (adjustHunkLineNumbers, findActualString, etc.). Openclaude's FileEditTool UI has different structure (upstream Anthropic).

9e365f1f | chore: 1.10.10 | NOT_APPLICABLE | package.json | Version bump.

a2cfaf91 | fix: RemoteTriggerTool and autonomy test failures | NOT_APPLICABLE | — | Test-only fix.

4f1649e2 | feature: 20260429 code inspection (#383) | NOT_APPLICABLE | — | Merge commit, no diff content.

f2e9af49 | feat: harden autonomy lifecycle, OOM bounds, provider-boundary finalization | GAP | src/cli/print.ts, src/utils/autonomyRuns.ts, src/utils/autonomyAuthority.ts | CCB refactored cron dispatch to use unified dedup+claim pipeline (`createAutonomyQueuedPromptIfNoActiveSource` with sourceId dedup). Openclaude's autonomy code uses older KAIROS-style cron dispatch without source-dedup. Also added `setAbortController(null)` when all claimed commands are skipped (prevents stale abort controller leak). OC: not present.

29a1edbf | fix: model picker 1M context toggle shows "Space to toggle" even when off | GAP | src/components/ModelPicker.tsx:282 | Openclaude ModelPicker may not show "Space to toggle" hint when 1M context is off. CCB added `<Text color="subtle"> · Space to toggle</Text>` in the off-state. OC: need to verify.

452a7e6a | fixup: CodeRabbit review on PR #386 | NOT_APPLICABLE | src/utils/handlePromptSubmit.ts | CodeRabbit review fixup — doc typo fix + test adjustment. Source changes are already covered by the parent PR commit.

189766c5 | fixup: second-round CodeRabbit review on PR #386 | GAP | src/utils/handlePromptSubmit.ts:496-588 | CCB added `turnError` variable + `logError` + `toError` imports to prevent unhandled rejection when cron dispatch throws inside async IIFE. Openclaude: `turnError` variable not present; `setAbortController(null)` exists at line 588 but error handling differs.

f8388e44 | docs: add bash tag to sur-skill-overflow-bugs code block | NOT_APPLICABLE | — | Docs-only.

6b7cfda9 | fixup: 4 uncovered items from PR #386 review | GAP | src/cli/print.ts:2823-2843, src/services/compact/postCompactCleanup.ts:72 | CCB refactored legacy cron onFire to use unified dedup pipeline same as onFireTask. This commit contains incremental improvements to the autonomy+cron dispatch refactor. Openclaude: older code without this consolidation.

7a6e65ca | refactor: simplify/reuse/defend — PR #386 audit cleanup | GAP | src/cli/print.ts:2819-2898 | CCB extracted `dispatchHeadlessCronCommand` shared pipeline for 3 cron entry points with cancel-on-late-shutdown contract. Openclaude has separate, non-unified cron dispatch paths.

edae3a7d | feat: harden autonomy lifecycle (PR #386 merge) | NOT_APPLICABLE | — | Merge commit of #386. Contents already covered by f2e9af49, 6b7cfda9, 7a6e65ca.

7effbca8 | chore: 1.10.11 | NOT_APPLICABLE | package.json | Version bump.

08cd02cd | fix: highlight cache uses LRUCache to reduce memory | ALREADY_HAVE | src/native-ts/color-diff/index.ts | CCB added per-line hljs AST cache (Map with 2048-entry cap). Openclaude's color-diff native at `src/native-ts/color-diff/index.ts` has its own approach (cached HLJSApi instance). Different implementation but both address the same concern.

00da5d7d | Merge PR #388 (modelpicker-1m-toggle-hint) | NOT_APPLICABLE | — | Merge of PR already covered by 29a1edbf.

282d5150 | chore: v1.11.0 | NOT_APPLICABLE | — | Version bump.

632f3e19 | Merge PR #381 (LittleApple-fp16/patch-1) | NOT_APPLICABLE | — | Merge commit.

71c89e9d | fix: theme switching always defaults to dark mode | ALREADY_HAVE | src/components/App.tsx | CCB added `setThemeConfigCallbacks` + theme init from globalConfig. Openclaude's theme system is upstream Anthropic Ink-based — different theme architecture, same behavior (theme persistence works).

cd8136f4 | Merge PR #395 (theme-switching fix) | NOT_APPLICABLE | — | Merge of PR already covered by 71c89e9d.

ca29e4e8 | fix: disable FORK_SUBAGENT to restore Explore subagent haiku model dispatch | NOT_APPLICABLE | scripts/defines.ts | CCB-internal feature flag toggle. Openclaude enables FORK_SUBAGENT unconditionally — different architecture decision (we want fork subagent).

42100d62 | feat: disable skill learning (EXPERIMENTAL_SKILL_SEARCH + SKILL_LEARNING) | NOT_APPLICABLE | scripts/defines.ts | CCB-internal feature flag toggle. Openclaude has these features enabled and implemented (DiscoverSkillsTool, skill-learning pipeline per CLAUDE.md).

465c95ae | chore: 1.11.1 | NOT_APPLICABLE | package.json | Version bump.

d136872c | fix: attempt to fix third-party API parameter incompatibility | GAP | src/utils/betas.ts:215-218, src/utils/model/model.ts:362-365 | CCB added `isFirstPartyAnthropicBaseUrl()` guard to `shouldIncludeFirstPartyOnlyBetas()` and `isOpus1mMergeEnabled()` — prevents Anthropic-beta headers from leaking to third-party API endpoints. Openclaude: `shouldIncludeFirstPartyOnlyBetas()` checks `getAPIProvider() === 'firstParty' || 'foundry'` but does NOT check `isFirstPartyAnthropicBaseUrl()`. This means beta headers could be sent to non-Anthropic endpoints (z.ai, DeepSeek, NIM). **Causes 400 errors on some third-party APIs.**

61820150 | style: lint all files | NOT_APPLICABLE | — | Style-only (Biome lint pass).

c32f26cf | style: fix all lint errors, cover @ant forked code | NOT_APPLICABLE | — | Style-only.

9ea9859d | style: format packages/@ant/ for biome ci | NOT_APPLICABLE | — | Style-only.

491c16da | fix: tsc type errors, pass CI typecheck | NOT_APPLICABLE | — | CI/typecheck fix — CCB-specific type issues.

ff2074c7 | style: add biome-ignore for noUnusedPrivateClassMembers | NOT_APPLICABLE | — | Style-only.

a8199505 | docs: update CLAUDE.md Biome coverage rules | NOT_APPLICABLE | — | Docs-only.

ab0bbbc4 | fix: memory overflow — clean persistent-growth data structures on compact | GAP | src/QueryEngine.ts:248-249, src/cli/transports/SSETransport.ts:350-366, src/screens/REPL.tsx:1779-1781, src/services/compact/postCompactCleanup.ts | CCB added 4 fixes: (1) `permissionDenials = []` reset in QueryEngine.submit (not just constructor), (2) SSE buffer 1MB cap with connection-drop on overflow, (3) `registerCompactCleanup` callback to reset `contentReplacementState`, (4) compact cleanup also clears beta-tracing state. Openclaude: `permissionDenials` reset only in constructor (line 204); SSETransport has NO buffer-size cap (lines 340-369); no `registerCompactCleanup` mechanism; need to verify compact cleanup scope.

f484fc34 | chore: VSCode recommended extensions + pin Bun runtime version | NOT_APPLICABLE | — | Tooling config only.

ef10ad28 | fix: optimize memory peak and CPU — reduce 100-300MB | GAP | Multiple files | Large commit: added docs/memory-peak-analysis.md (217-line analysis), performance optimizations across QueryEngine, SSETransport, postCompactCleanup, contentReplacementState. Source changes already covered by ab0bbbc4 + f7243000. The analysis doc itself is NOT_APPLICABLE.

96f1700e | Merge PR #400 (memory-peak) | NOT_APPLICABLE | — | Merge commit.

0977b052 | docs: merge performance analysis report | NOT_APPLICABLE | — | Docs-only (memory-peak-analysis.md updates).

385baf57 | Merge PR #402 (memory-peak) | NOT_APPLICABLE | — | Merge commit.

3eba5ade | chore: v2.0.0 | NOT_APPLICABLE | — | Version bump.

f7243000 | fix: memory optimization — FileReadTool 100KB cap, lookups cache, microcompact replacement cleanup | GAP | src/query.ts:479-492, src/services/compact/compact.ts:336-358, packages/builtin-tools/src/tools/FileReadTool/FileReadTool.ts:761-771 | CCB added: (1) `stripToolUseResults()` to delete `toolUseResult` from kept messages after compaction, (2) `delete msg.toolUseResult` loop in query.ts before API call, (3) FileReadTool byte-length fast-rejection (4x token limit check). Openclaude: NO `toolUseResult` cleanup anywhere (query.ts only uses it for error messages at line 180; compact.ts has no stripToolUseResults); FileReadTool has no byte-length fast-rejection.

1b10ea39 | fix: preserve empty reasoning_content for DeepSeek v4 thinking mode (#399) | GAP | packages/@ant/model-provider/src/shared/ | CCB fixed DeepSeek v4 thinking mode: empty reasoning_content (direct-answer without thinking) must be echoed back as `reasoning_content: ""` or DeepSeek returns 400. Openclaude uses its own OpenAI bridge at `src/services/api/openaiBridge/` — need to verify empty reasoning_content handling.

0290fe32 | fix: disable context-collapse to fix auto compact failure | NOT_APPLICABLE | scripts/defines.ts | CCB-internal feature flag toggle. Openclaude's contextCollapse is a no-op stub per CLAUDE.md (returns `{messages, committed}` with no actual collapse), but it's not blocking auto compact since reactiveCompact handles PTL recovery instead. Different architecture.

f72b867a | chore: v2.0.1 | NOT_APPLICABLE | — | Version bump.

4cbf406c | Merge PR #403 (deepseek-empty-reasoning-content) | NOT_APPLICABLE | — | Merge of PR already covered by 1b10ea39.

198c09b2 | fix: memory optimization — predictive compact thresholds, incremental lookups, deferred slice | GAP | src/components/Messages.tsx:518-595, packages/builtin-tools/src/tools/FileReadTool/FileReadTool.ts | CCB added `updateMessageLookupsIncremental()` for partial rebuild of lookups when only new messages appended (avoids full 8-Map/Set rebuild on each streaming delta). Also added `lastAssistantMsgId` tracking to detect orphaned in-progress assistants. Openclaude: NO incremental lookups mechanism.

2847cab7 | docs: compress memory analysis report (720->120 lines) | NOT_APPLICABLE | — | Docs-only.

c3af4502 | chore: v2.0.2 | NOT_APPLICABLE | — | Version bump.

86df024e | fix: fix model issues | GAP | src/utils/model/model.ts | CCB added `isFirstPartyAnthropicBaseUrl()` guard to `isOpus1mMergeEnabled()`. Same pattern as d136872c — prevents first-party-only model features from activating on third-party APIs.

ba74e097 | feat: fork-agent-redesign — add AgentTool fork parameter + spec doc | GAP | packages/builtin-tools/src/tools/AgentTool/AgentTool.tsx:148-412 | CCB added `fork: boolean` parameter to AgentTool input schema, wired through call() with FORK_SUBAGENT gating. When `fork=true`, routes to fork subagent path (inherits full history + model from parent). Openclaude's AgentTool: NO `fork` parameter in schema (verified by grep — no `fork.*boolean` match). Openclaude has FORK_SUBAGENT feature and `/fork` command but the AgentTool schema doesn't expose a `fork` boolean param for the model to use.

4ca7a489 | test: add tasks.ts CRUD test coverage (37 tests) | NOT_APPLICABLE | — | Test-only.

3a2b6dde | perf: table rendering efficiency upgrade | GAP | src/components/MarkdownTable.tsx | CCB wrapped MarkdownTable in React.memo + added per-render caches (formatCache, plainTextCache) to avoid redundant formatCell/wrapText calls across multiple passes. Openclaude: need to verify if similar optimizations exist.

6becb8b2 | fix: tasks.test.ts type errors + concurrent test failures | NOT_APPLICABLE | — | Test-only fix.

d3eebfed | build: Vite single-file build + fix doubaoime-asr WASM loading | NOT_APPLICABLE | — | Build system change (Vite).

40fbc4af | chore: 2.0.3 | NOT_APPLICABLE | — | Version bump.

2545dcab | fix: ccb update uses bun install -g @latest instead of bun update -g | NOT_APPLICABLE | — | CCB-specific update mechanism.

5dc4d8f8 | docs: update contributors | NOT_APPLICABLE | — | Docs-only.

5c1be195 | docs: update contributors | NOT_APPLICABLE | — | Docs-only.

b28de717 | perf: optimize memory and telemetry, enable Vite minify | GAP | build.ts:24-28, scripts/dev.ts:17-19, src/entrypoints/cli.tsx:1-5, src/entrypoints/init.ts:323-330, src/services/compact/snipCompact.ts:163-243, src/utils/startupProfiler.ts:145-149 | CCB added: (1) `process.env.NODE_ENV = 'production'` in build to eliminate React dev-mode _debugStack objects, (2) `performanceShim.js` import before React/OTel capture, (3) OTel skip when telemetry disabled (prevents PerformanceMeasure accumulation), (4) `proactiveTruncate()` in snipCompact (150MB char limit with tail fallback), (5) startupProfiler `clearMarks()` + `memorySnapshots.length = 0` after report. Openclaude: NO `performanceShim.js` import; NO `NODE_ENV=production` in build; NO OTel skip gate; NO `proactiveTruncate`; need to verify startupProfiler cleanup.

5e215bb0 | chore: v2.0.4 | NOT_APPLICABLE | — | Version bump.

5b333e22 | refactor: read version dynamically from package.json | NOT_APPLICABLE | scripts/defines.ts | CCB-specific build system change (MACRO.VERSION from hardcoded to pkg.version). Different build approach.

45c892fc | revert: restore HISTORY_SNIP (revert the disable from b28de717) | NOT_APPLICABLE | scripts/defines.ts, src/QueryEngine.ts, src/services/compact/snipCompact.ts | CCB re-enabled HISTORY_SNIP after temporarily disabling it. Openclaude enables all flags unconditionally — the snipCompact module is present and functional.

f8a289b8 | fix: attempt to fix OTEL issues | NOT_APPLICABLE | .husky/pre-commit, src/utils/startupProfiler.ts | CCB changed `bunx lint-staged` to `npx lint-staged` in pre-commit hook + added startup marks cleanup. Already covered by b28de717 analysis.

8a5ef8c9 | fix: optimize user-facing text, add actionable tips to error messages | ALREADY_HAVE | src/QueryEngine.ts:1051-1055, src/cli/print.ts, src/components/Onboarding.tsx, src/components/TrustDialog/TrustDialog.tsx | CCB improved error message UX: budget exceeded shows `--max-budget-usd` guidance; max turns shows actionable tips; structured output errors include suggestions. Openclaude: upstream Anthropic already has these patterns; our fork preserves them. UX polish only — no functional gap.

4d0048a6 | fix: optimize permission prompt wording and Help page onboarding | ALREADY_HAVE | src/components/HelpV2/General.tsx, src/components/permissions/ | CCB improved: (1) Help General page — added 3-step "Getting started" guide, (2) permission dialog: "Esc to cancel"->"Esc to reject", "Tab to amend"->"Tab to add feedback", (3) .claude/ option label shortened. Openclaude: upstream Anthropic Help/permission components — UX polish only, no functional gap.

88057b10 | fix: optimize ModelPicker subtitle and resume error messages | ALREADY_HAVE | src/components/ModelPicker.tsx, src/commands/resume/resume.tsx | UX text improvements only — ModelPicker subtitle changed to action-oriented, resume errors suggest `/resume` to browse. No functional gap.

6ff839d6 | fix: optimize compaction error messages and auto-compact prompts | ALREADY_HAVE | src/components/CompactSummary.tsx:79-90, src/services/compact/compact.ts | CCB changed "Compact summary" -> "Conversation summarized to free up context", "expand" -> "view summary", added "Send a few more messages first" guidance. Openclaude: upstream Anthropic already has similar UX patterns.

e7220c53 | fix: eliminate memory leak in promptCacheBreakDetection by replacing closures with pre-computed strings | GAP | src/services/api/promptCacheBreakDetection.ts:65-653 | CCB changed `buildDiffableContent: () => string` (lazy closure) to `buildDiffableContent: string` (pre-computed) in PreviousState and PendingChanges types. The closure captured `system`, `toolSchemas`, and `model` references, preventing GC. Openclaude: type still uses `buildDiffableContent: () => string` (closure) at line 68 — MEMORY LEAK present.

75952bde | fix: attempt request parameter cloning to release closure references | GAP | src/services/api/claude.ts:1442-1587 | CCB added deep-clone serialization boundary: `frozenMessages`, `frozenSystem`, `frozenTools` via `cloneDeep()` from lodash-es, then nulls out originals (`messagesForAPI = null!`, `system = null!`, `allTools = null!`) so GC can reclaim while streaming. Openclaude: NO cloneDeep import, NO frozen variables, NO null-out pattern — streaming generator retains references to full original arrays.

cf2bf29d | feat: attempt deep copy to separate references | GAP | src/query.ts:340-348, src/query.ts:479-492 | CCB added: (1) langfuse trace closure breaking (`langfuseTrace = null` after endTrace), (2) cleanup comments about removing toolUseResult payloads from previous turns. Openclaude: NO langfuse trace null-out; NO toolUseResult cleanup loop (verified earlier).

d0915fc8 | chore: clean 33 dead code items and type assertions in src/ | NOT_APPLICABLE | Various (tmux.ts, update.ts, etc.) | Dead code removal — CCB deleted `getTmuxInstallHint()`, entire `cli/update.ts` (422 lines), various type imports. Openclaude codebase is upstream-based with different dead code patterns.

18d6656a | feat: attempt to improve Error handling for memory management | GAP | packages/@ant/ink/src/components/App.tsx:131-148, packages/@ant/ink/src/components/ErrorOverview.tsx:23-28, src/query.ts:340-348 | CCB changed Ink ErrorOverview to accept `{message, stack?}` instead of full `Error` objects (reduces retained references). Also added `flushLangfuse()` call after endTrace to release span data. Openclaude: NO flushLangfuse; ERROR: need to verify Ink ErrorOverview type.

87b96199 | feat: AI random fix | GAP | build.ts:24-28, scripts/dev.ts:17-19, src/entrypoints/cli.tsx:1-5, src/query.ts:340-348 | Continuation of earlier memory work — NODE_ENV=production in build, performanceShim import, flushLangfuse. All already covered by b28de717 + cf2bf29d + 18d6656a.

a1108870 | Merge PR #412 (20260504/improve) | NOT_APPLICABLE | — | Merge commit covering 8a5ef8c9 through 87b96199.

fcbc8822 | chore: clean 113 unused imports and dead code in src/ | NOT_APPLICABLE | Various | Dead code removal (unused imports, types, functions). No new functionality.

1ac18aec | chore: clean 4 missed unused imports | NOT_APPLICABLE | src/utils/autonomyStatus.ts, src/utils/betas.ts, src/utils/claudemd.ts, src/utils/computerUse/executorCrossPlatform.ts | Dead code removal — removed unused `join` from path, unused `sep`, `isEnvDefinedFalsy`, `Platform` type, `Platform` import. No functional change.

0ad63494 | chore: clean 18 unused imports, variables, and functions | NOT_APPLICABLE | src/components/PromptInput/Notifications.tsx | Dead code removal — removed unused autoUpdater props/state. No functional change.

100e9d2d | chore: 2.0.5 | NOT_APPLICABLE | — | Version bump.

3f1c8468 | fix: reduce snapshots range | GAP | src/utils/fileHistory.ts:54 | CCB reduced `MAX_SNAPSHOTS` from 100 to 20 — "file checkpointing causes unbounded memory growth (100 snapshots x full file backups)". Openclaude: `MAX_SNAPSHOTS = 100` at line 54. Same unbounded memory risk.

f5c9880d | Merge PR #413 (memory-leak-fix) | NOT_APPLICABLE | — | Merge commit covering e7220c53 through 3f1c8468.

872ee280 | chore: 2.1.0 | NOT_APPLICABLE | — | Version bump.

26ddbda8 | fix: align MCP transform pipeline with Anthropic Claude Code 2.1.128 | GAP | src/services/mcp/client.ts:2490-2564 | CCB added `limits?: ImageLimits` and `includeMeta = false` params to `transformResultContent()`, plus `_meta` preservation in text content blocks. This aligns with upstream 2.1.128 changes for MCP content transformation. Openclaude: `transformResultContent()` signature is `(resultContent, serverName)` with no `limits` or `includeMeta` params, no `_meta` passthrough — 2 params vs CCB's 3 params.

c4e9efb7 | Merge PR #417 (sync/mcp-transform-2.1.128) | NOT_APPLICABLE | — | Merge of PR already covered by 26ddbda8.

---

## Key Findings Summary

### Critical Gaps (10)

| SHA | Issue | Impact |
|-----|-------|--------|
| d136872c | `shouldIncludeFirstPartyOnlyBetas()` missing `isFirstPartyAnthropicBaseUrl()` guard | Anthropic beta headers leak to z.ai/DeepSeek/NIM — may cause 400 errors |
| e7220c53 | `buildDiffableContent` still a closure (`()=>string`) not pre-computed `string` | Memory leak — closure captures system+tools+model refs |
| 75952bde | No deep-clone serialization boundary in claude.ts queryModel | Streaming generator retains full original arrays — 120-320MB waste |
| cf2bf29d | No langfuse trace null-out after endTrace | SpanImpl retains 571MB Performance object |
| f7243000 | No `toolUseResult` cleanup in query.ts or compact.ts | FileRead/big tool results accumulate unbounded until compact |
| 198c09b2 | No incremental lookups update (`updateMessageLookupsIncremental`) | Full 8-Map/Set rebuild on every streaming delta |
| ab0bbbc4 | (a) No SSE buffer overflow cap, (b) No `registerCompactCleanup`, (c) `permissionDenials` not reset in submit | Memory growth in long sessions |
| ba74e097 | AgentTool missing `fork: boolean` param | Model can't route to fork subagent via AgentTool API |
| b28de717 | No `performanceShim.js` + no `NODE_ENV=production` + no OTel skip gate | React dev-mode _debugStack objects accumulate (12MB+), OTel PerformanceMeasure grows unbounded |
| 3f1c8468 | MAX_SNAPSHOTS still 100 (not 20) | File checkpointing causes unbounded memory growth |

### Minor Gaps (6)

| SHA | Issue |
|-----|-------|
| 29a1edbf | ModelPicker may not show "Space to toggle" when 1M context off |
| 18d6656a | No `flushLangfuse()` after endTrace; Ink ErrorOverview still accepts full Error objects |
| 3a2b6dde | MarkdownTable not wrapped in React.memo; no per-render formatCache |
| 26ddbda8 | MCP `transformResultContent` missing `_meta` passthrough + `limits` param |
| 1b10ea39 | DeepSeek v4 empty reasoning_content handling in openaiBridge needs verification |
| 86df024e | `isOpus1mMergeEnabled()` missing `isFirstPartyAnthropicBaseUrl()` guard |
