# CCB Fix Audit — openclaude backport catalog

Systematic review of all 647 commits from [claude-code-best/claude-code](https://github.com/claude-code-best/claude-code) main branch (oldest→newest, skipping initial build commit `f90eee85`). Pure documentation — a separate session will apply selected fixes using this file as context.

**Started:** 2026-05-11 | **Completed:** 2026-05-11  
**Total commits reviewed:** 647 (8 parallel agents, ~82 commits each)  
**Total APPLY candidates found:** ~35 fixes worth backporting  
**Status key:** `[ ]` TODO | `[x]` APPLIED | `[-]` SKIP | `[~]` PARTIAL

---

## Audit changelog

- **2026-05-11 (all 8 batches complete)** — Full 647-commit audit. ~35 DOCUMENTED gaps identified, organized by priority below.

---

## Scope & Methodology

Each CCB commit examined for:
- **What changed** and why (the actual diff)
- **Whether openclaude already has this fix** (code comparison, not just file existence)
- **Fix vs feature**: genuine bug fix vs new feature vs refactor/docs/CI

**Relevance:**
- **GAP** — CCB has this fix; openclaude DOES NOT. Worth backporting.
- **ALREADY_HAVE** — Fix already present in openclaude (independent impl, prior backport, or different architecture)
- **NOT_APPLICABLE** — CCB-only (CI/docs/lockfile/langfuse/CCB-specific features not in openclaude, build-system-only)

**Note:** Windows/macOS fixes ARE in scope per user instruction.

---

## GAP Catalog (fixes CCB has that openclaude DOES NOT)

### CRITICAL — API Compatibility & Crashes

#### 1. `941bcbd2` — Third-party API user_id validation error (DeepSeek, z.ai, NIM)
- **Date:** 2026-05-06 | **Files:** `src/services/api/claude.ts`
- **Problem:** `getAPIMetadata()` sends `user_id` as JSON string `{"device_id":...,"account_uuid":...,"session_id":...}` which fails `^[a-zA-Z0-9_-]+$` validation on non-Anthropic providers.
- **Fix:** Send only hex `device_id` when base URL != `api.anthropic.com`.

#### 2. `047c85fc` / `1b10ea39` — DeepSeek V4 reasoning_content echoed back → 400 error
- **Date:** 2026-04-24 / 2026-05-02 | **Files:** `src/services/api/openaiBridge/requestTranslator.ts`, `streamTranslator.ts`
- **Problem:** DeepSeek sometimes returns `reasoning_content: ""` which must be preserved and echoed back. Our bridge doesn't handle empty-string thinking blocks.
- **Fix:** Preserve empty reasoning_content in both request and stream translation. Adapt from CCB's `@ant/model-provider` package into our `openaiBridge/`.

#### 3. `d136872c` — Third-party API rejects Anthropic-only beta headers
- **Date:** 2026-05-01 | **Files:** `src/utils/betas.ts`
- **Problem:** `shouldIncludeFirstPartyOnlyBetas()` sends headers like `tool-search` to z.ai/DeepSeek which reject unknown beta headers.
- **Fix:** Add `isFirstPartyAnthropicBaseUrl()` guard.

#### 4. `4dcbaf1e` — ACP mode messageSelector require crash → submitMessage fails
- **Date:** 2026-04-24 | **Files:** `src/QueryEngine.ts`
- **Problem:** `messageSelector()` lazy-require returns undefined; called without null check at lines 471, 659.
- **Fix:** try/catch + null guard.

#### 5. `ca1c87f4` — usePipeIpc require returns undefined → startup crash
- **Date:** 2026-04-23 | **Files:** `src/hooks/usePipeIpc.ts`
- **Problem:** Lazy `require()` pattern returns undefined when feature-gated modules not loaded.
- **Fix:** Convert to static imports.

#### 6. `b8b48bf7` — truncate() crash on undefined/null input
- **Date:** 2026-04-28 | **Files:** `src/utils/truncate.ts`
- **Problem:** `truncate()` called with undefined/null from BackgroundTask component causes crash.
- **Fix:** Null guard at function entry.

### HIGH — Memory & Performance

#### 7. `f5c3ee5b` — Long-running session memory leak (3 fixes in 1)
- **Date:** 2026-04-26 | **Files:** `src/commands/clear/conversation.ts`, `src/screens/REPL.tsx`
- **Problems & fixes:**
  - **a)** `/clear` doesn't clear `lastAPIRequest`, `lastAPIRequestMessages`, `lastClassifierRequests` → unbounded growth
  - **b)** REPL messages uncapped → unbounded scrollback memory. Add cap at 500.
  - **c)** Progress replacement only checks last message → duplicate entries. Scan backwards for last progress.

#### 8. `198c09b2` — Memory optimization (P0): toolUseResult release + predictive compact
- **Date:** 2026-05-02 | **Files:** `src/query.ts`, `src/screens/REPL.tsx`, `src/services/compact/autoCompact.ts`, `src/services/compact/compact.ts`, `src/services/compact/reactiveCompact.ts`, `src/components/Messages.tsx`, `src/utils/messages.ts`, `src/utils/readFileInRange.ts`
- **Fixes:**
  - Delete `toolUseResult` from user messages after UI render
  - `stripToolUseResults()` after compact
  - Predictive compact threshold uses `effectiveContextWindow - growth` (fixes double-reservation)
  - TOOL_RESULT_GROWTH_ESTIMATE 20K→15K
  - Incremental lookups orphaned tool detection
  - REPL deferred messages slice useMemo

#### 9. `ab0bbbc4` — Memory overflow: SSE buffer cap + compact cleanup
- **Date:** 2026-05-01 | **Files:** `src/QueryEngine.ts`, `src/cli/transports/SSETransport.ts`, `src/screens/REPL.tsx`, `src/services/compact/postCompactCleanup.ts`, `src/utils/errors.ts`, `src/utils/log.ts`
- **Fixes:**
  - Reset `permissionDenials` on new session
  - 1MB SSE buffer cap prevents runaway growth
  - `registerCompactCleanup()` hook for contentReplacementState
  - `shortErrorStack()` trims logged stacks

#### 10. `e7220c53` — Memory leak: promptCacheBreakDetection closure
- **Date:** 2026-05-05 | **Files:** `src/services/api/promptCacheBreakDetection.ts`
- **Problem:** `buildDiffableContent` as `() => string` closure captures references preventing GC.
- **Fix:** Pre-compute to `string` property, eliminate closure.

#### 11. `75952bde` — Request params deep-clone to break closure refs during streaming
- **Date:** 2026-05-05 | **Files:** `src/services/api/claude.ts`
- **Problem:** Messages/system/tools captured in generator closure during streaming → can't GC.
- **Fix:** `cloneDeep` at serialization boundary, null out originals, pre-compute scalars.

#### 12. `08cd02cd` — Highlight cache unbounded Map → LRUCache
- **Date:** 2026-05-01 | **Files:** `src/components/HighlightedCode/Fallback.tsx`, `src/components/Markdown.tsx`
- **Problem:** Unbounded Map caches grow without limit.
- **Fix:** Replace with LRUCache (requires `lru-cache` dep).

#### 13. `3f1c8468` — MAX_SNAPSHOTS 100 → 20 (unbounded memory)
- **Date:** 2026-05-05 | **Files:** `src/utils/fileHistory.ts`
- **Problem:** 100 full-file backups cause unbounded heap growth.
- **Fix:** Reduce to 20.

#### 14. `f8a289b8` — StartupProfiler clearMarks accumulation in daemon processes
- **Date:** 2026-05-04 | **Files:** `src/utils/startupProfiler.ts`
- **Problem:** `perf.clearMarks()` never called → PerformanceMark accumulation in long-lived processes.
- **Fix:** Call clearMarks in `profileReport()`.

### MEDIUM — Correctness & UX

#### 15. `4b440479` — iTerm2 terminal response sequences leak into REPL input
- **Date:** 2026-04-07 | **Files:** `src/utils/earlyInput.ts`
- **Problem:** Naive "skip until 0x40-0x7E" escape handling leaks CSI/string/device-attrib responses.
- **Fix:** Proper CSI parser + DCS/OSC/SOS/PM handling with BEL/ST terminators.

#### 16. `bb078362` — CRLF SSE frame parsing
- **Date:** 2026-04-09 | **Files:** `src/cli/transports/SSETransport.ts`
- **Problem:** Only handles `\n\n` frame delimiters. CRLF streams produce malformed frames.
- **Fix:** Regex `/\r?\n\r?\n/g` delimiter + strip trailing `\r` from lines.

#### 17. `562e9daa` — getCommandName() returns undefined → crash
- **Date:** 2026-04-09 | **Files:** `src/types/command.ts`
- **Problem:** `getCommandName()` returns undefined when `cmd.name` is undefined.
- **Fix:** `return cmd.userFacingName?.() ?? cmd.name || ''`

#### 18. `ad09f38f` — Slash command autocomplete broken mid-input; Tab overwrites
- **Date:** 2026-04-25 | **Files:** `src/hooks/useTypeahead.tsx`
- **Problem:** `isCommandInput(value)` uses full input instead of cursor-truncated input.
- **Fix:** `commandInput = value.substring(0, effectiveCursorOffset)` at 3 call sites.

#### 19. `1c3b280c` — Multi-turn skill discovery cache invalidation on resume
- **Date:** 2026-04-25 | **Files:** `src/utils/attachments.ts`, `src/utils/conversationRecovery.ts`
- **Problem:** Resume re-injects duplicate skill_discovery content → busts prompt cache.
- **Fix:** `suppressNextSkillDiscovery()` flag + unconditional suppression on resume.

#### 20. `354c11f0` — LRU cache size miscalculation for nested object content
- **Date:** 2026-04-05 | **Files:** `src/utils/fileStateCache.ts`, `src/utils/queryHelpers.ts`
- **Problem:** `Buffer.byteLength(nestedObject)` returns garbage when Write tool content deserialized as object.
- **Fix:** `coerceToolContentToString()` helper + safe string coercion.

#### 21. `221fb6eb` — @ typeahead file search false negatives + execa signal rename
- **Date:** 2026-04-01 | **Files:** `src/native-ts/file-index/index.ts`, `src/utils/execFileNoThrow.ts`
- **Problem:** Greedy-leftmost indexOf for first needle char causes false negatives. Also `signal` → `cancelSignal` (execa 9.x API).
- **Fix:** Multi-start-position scan + word-boundary awareness. Fix execa cancel signal param.

#### 22. `cee62bc6` — Model alias infinite recursion stack overflow
- **Date:** 2026-04-21 | **Files:** `src/utils/model/model.ts`
- **Problem:** `parseUserSpecifiedModel()` calls back to `getDefault*Model()` for aliases → possible recursion.
- **Fix:** `isAliasOrAliasWithSuffix()` guard in fallback paths.

#### 23. `84f12f34` — CLAUDE.md buried in system-reminder loses instructional weight
- **Date:** 2026-05-09 | **Files:** `src/services/api/claude.ts`, `src/utils/api.ts`
- **Problem:** `prependUserContext()` puts claudeMd in `<system-reminder>` with "may or may not be relevant." Deferred tools steal first-message position.
- **Fix:** Extract to `<project-instructions>` block. Move deferred tools from PREPEND to APPEND.

### LOW — Defensive & Nice-to-Have

#### 24. `82be5ff0` — O(n^2) text delta string concatenation in streaming
- **Date:** 2026-05-10 | **Files:** `src/services/api/claude.ts`
- **Problem:** `contentBlock.text += delta.text` in loop → O(n^2).
- **Fix:** Map-based accumulation + `join()` at `content_block_stop`.

#### 25. `2006ab25` — React Error Boundary returns null (invisible failure)
- **Date:** 2026-05-09 | **Files:** `src/components/SentryErrorBoundary.ts` → `.tsx`, `src/components/Messages.tsx`, `src/replLauncher.tsx`
- **Problem:** Current `.ts` ErrorBoundary returns null on crash. User sees nothing.
- **Fix:** Convert to `.tsx` with Ink error display. Wrap Messages + root REPL.

#### 26. `26ddbda8` — MCP transform pipeline missing upstream limits/includeMeta
- **Date:** 2026-05-05 | **Files:** `src/services/mcp/client.ts`, `src/utils/imageResizer.ts`
- **Problem:** `transformResultContent` / `processMCPResult` / `fetchMcpResource` signatures stale vs upstream 2.1.128.
- **Fix:** Plumb `limits?: ImageLimits` and `includeMeta = false`.

#### 27. `dc3d3e88` + `6e1d3d8f` — modelSupportsAutoMode() provider whitelist blocks z.ai/DeepSeek
- **Date:** 2026-05-10 | **Files:** `src/utils/betas.ts`
- **Problem:** 42-line restrictive logic: blocks non-firstParty providers, GrowthBook overrides, ant-internal denylist, external allowlist.
- **Fix:** Reduce to `feature('TRANSCRIPT_CLASSIFIER') ? true : false`.

#### 28. `e4ce08fe` (extracted) — Context counter flash to 0% on third-party APIs
- **Date:** 2026-04-20 | **Files:** `src/utils/tokens.ts`, `src/utils/context.ts`
- **Problem:** All-zero usage objects from 3rd-party APIs cause "ctx:0%" flash.
- **Fix:** Skip in `getCurrentUsage()`. Null-guard `calculateContextPercentages()`.

#### 29. `86df024e` — isOpus1mMergeEnabled needs firstParty guard
- **Date:** 2026-05-02 | **Files:** `src/utils/model/model.ts`
- **Problem:** `isOpus1mMergeEnabled()` missing `isFirstPartyAnthropicBaseUrl()` check.
- **Fix:** Add guard alongside existing `getAPIProvider() !== 'firstParty'`.

#### 30. `71c89e9d` — Theme switching always defaults to dark
- **Date:** 2026-04-30 | **Files:** `src/components/App.tsx`, `src/entrypoints/init.ts`
- **Problem:** Theme not persisted through globalConfig.
- **Fix:** Wire ThemeProvider with onThemeSave callback.

#### 31. `be97a0b0` (extracted) — Empty beta header filtering
- **Date:** 2026-04-22 | **Files:** `src/services/api/claude.ts`
- **Problem:** Empty-string beta headers like `CACHE_EDITING_BETA_HEADER=''` → 400.
- **Fix:** `betasParams.filter(Boolean)`.

#### 32. `8442aaad` — n keybinding causes accidental dialog close
- **Date:** 2026-04-14 | **Files:** `src/keybindings/defaultBindings.ts`
- **Problem:** `n: 'confirm:no'` in Confirmation context → typing `n` dismisses dialog.
- **Fix:** Remove y/n from Confirmation, keep Enter/Escape only.

#### 33. `c80e5932` (extracted) — FileEditTool tab/space normalization
- **Date:** 2026-04-27 | **Files:** `src/tools/FileEditTool/utils.ts`
- **Problem:** `findActualString()` only normalizes quotes, not tabs/spaces.
- **Fix:** Add `normalizeWhitespace()` → `mapNormalizedMatchBackToFile()` cascade.

#### 34. `da6d0636` (extracted) — Remove thinkingClearLatched sticky latch
- **Date:** 2026-04-24 | **Files:** `src/services/api/claude.ts`
- **Problem:** Sticky latch permanently clears thinking after 1h idle.
- **Fix:** Remove latch (hard-code `thinkingClearLatched: false`).

#### 35. `29a1edbf` — ModelPicker "Space to toggle" hint for 1M context
- **Date:** 2026-04-29 | **Files:** `src/components/ModelPicker.tsx`
- **Problem:** No hint when 1M context toggle is available but off.
- **Fix:** Add "Space to toggle" text.

---

## Files Most Frequently Changed (hotspots)

| File | APPLY Commits |
|------|-------------|
| `src/services/api/claude.ts` | #1, #11, #23, #24, #31, #34 (6 fixes) |
| `src/screens/REPL.tsx` | #7, #8, #9 (3 fixes) |
| `src/utils/betas.ts` | #3, #27 (2 fixes) |
| `src/utils/model/model.ts` | #22, #29 (2 fixes) |
| `src/QueryEngine.ts` | #4, #9 (2 fixes) |
| `src/services/api/openaiBridge/` | #2 (2 files) |
| `src/cli/transports/SSETransport.ts` | #9, #16 (2 fixes) |

---

## Agent Batch Details

| Batch | Commits | APPLY found | Key themes |
|-------|---------|-------------|------------|
| A (1-82) | 81 | 1 | File-index fuzzy scorer, execa signal |
| B (83-164) | 82 | 0 | CCB bootstrap: tests, docs, Buddy, voice, Chrome MCP, OpenAI bridge |
| C (165-244) | 81 | 1 | LRU cache fix; rest is ink-v2 migration, GrowthBook, Grok, Langfuse |
| D (247-328) | 82 | 0 | CCB ink-v2 (645 files), swarm RC, self-hosted RCS — architecture divergence |
| E (329-410) | 82 | 4 | Context counter, keybindings, model alias recursion, beta headers |
| F (411-492) | 82 | 8 | UDS/ACP crashes, memory leaks, typeahead, cache invalidation |
| G (493-574) | 82 | 11 | Memory optimization wave, DeepSeek fixes, theme fix, API compat |
| H (575-648) | 74 | 9 | API compat, auto mode, CLAUDE.md weight, Error Boundary, MCP alignment |
| **Total** | **647** | **~35** | |

---

## Next Steps (for the separate implementation session)

1. **Start with CRITICAL tier** (#1-#6): API crashes affecting z.ai/DeepSeek users + startup crashes
2. **Then HIGH tier** (#7-#14): Memory/performance — measurable impact on long-running sessions
3. **Then MEDIUM tier** (#15-#23): Correctness and UX — terminal glitches, SSE, autocomplete
4. **Low tier optional** (#24-#35): Defensive hardening and polish
5. For each fix: read the CCB diff, read openclaude's current code, apply the fix, build, hot-patch container, smoke test, commit with `CCB: <sha>` reference
