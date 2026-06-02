# CCB Fix Audit — openclaude gap catalog

Systematic audit of all 647 commits from [claude-code-best/claude-code](https://github.com/claude-code-best/claude-code) main branch, comparing each fix against openclaude source at `/home/openclaudeuser/openclaude/src/`.

**Audit date:** 2026-05-11
**Implementation completed:** 2026-05-11 (same day, follow-up session)
**Status:** **58 of 66 items closed** (54 LANDED + 7 VERIFIED-SKIP + 3 DEFERRED, see "Implementation Status" below)
**OC branch for implementation:** committed directly to `main`

---

## Incremental Refresh — 2026-06-02

Resumed the commit-by-commit audit from where the 2026-05-11 pass stopped. CCB `main` grew **648 → 707 commits** (58 new, `d11b35e0` 2026-05-11 → `b2b1981d` 2026-06-01). All 58 classified via 2 parallel Explore agents + a direct source-verification pass against `openclaude/src`.

**Method note:** every GAP claim was re-checked by reading our actual source (protocol step 6). ~40% of the agents' GAP flags dissolved on verification — recorded below so a later reader doesn't re-chase them.

### CONFIRMED GAPs (verified missing/weaker in ours)

| CCB sha | Fix | Priority | Our file | Notes |
|---|---|---|---|---|
| `ed619327` | OpenAI-compat stream adapter must subtract `cached_tokens` from `input_tokens` (OpenAI `prompt_tokens` includes cache reads; Anthropic `input_tokens` excludes them) | MEDIUM | `src/services/api/openaiBridge/responseTranslator.ts:117-120`, `streamTranslator.ts:345-431` | Our bridge reports `input_tokens = prompt_tokens` AND `cache_read_input_tokens = cached` → double-counts. Affects NIM (and any OpenAI-compat bridge) cache-hit-rate + cost accuracy. |
| `835dd2d8` | Cap the `existingSessionFiles` Map (CCB: `MAX_CACHED_SESSION_FILES`, evict oldest) | MEDIUM | `src/utils/sessionStorage.ts:1396` | Map at :1396 has `.set` with no eviction; unbounded growth in coordinator/swarm/daemon runs that mint unique sessionIds. |
| `efc218d8` | `searchSkills` must validate index identity before reusing cached IDF (`cachedIndex === index && cachedIdf`) | LOW | `src/services/skillSearch/localSearch.ts:383` | Ours is `cachedIdf ?? computeIdf(index)` — reuses IDF even when called with a different `index`. Intermittent stale-rank bug. |

**Status — all 3 CONFIRMED CCB GAPs LANDED `312a4eb` (openclaude `main`, 2026-06-02):** `ed619327` (openaiBridge subtracts cached_tokens from input_tokens — both translators + test updated), `835dd2d8` (sessionStorage `existingSessionFiles` cap 200 + evict + reset-clear), `efc218d8` (`cachedIndex === index && cachedIdf` guard).

### CANDIDATES (agent-flagged, NOT yet source-verified — verify before any backport)

| CCB sha | Fix | Pri | Our file |
|---|---|---|---|
| `b67e9f9d` | Plan-mode paste threshold (≥3 chars, non-bracketed terminals) + clear-context `setNeedsPlanModeExitAttachment(true)` | MED | `src/hooks/usePasteHandler.ts`, `ExitPlanModePermissionRequest.tsx` |
| `27b334ac`/`a05242ce` | Deadloop-prevention guidance in ToolSearch/ExecuteExtraTool prompt (ours = ToolSearchTool) | LOW/MED | `src/constants/prompts.ts`, ToolSearchTool prompt |
| `d4a60147` | BriefTool circular-dep → lazy `getBriefToolModule()` | LOW | `src/constants/prompts.ts` |
| `6dd378bf` | Terminal residual dialog content on startup-dialog exit (`pendingExitCode` defer-render) | LOW | `TrustDialog.tsx`/`BypassPermissionsModeDialog.tsx` (auto-trust reduces relevance for us) |

### DISSOLVED on verification → ALREADY_HAVE

- `48a19b8a` **isUsing3PServices provider coverage** — ours already returns true for every provider we run via the `ANTHROPIC_AUTH_TOKEN` + non-first-party-base-URL checks (`src/utils/auth.ts`). CCB's added OpenAI/Gemini/Grok env-var checks are providers we don't run.
- `c499bfb4` **VoiceProvider noop context** — already fixed via the localized `require('bundle').feature('VOICE_MODE')` runtime check (CLAUDE.md REPL-render-errors case 2).
- `b1c4f40f` **ensureToolResultPairing consecutive-user 400** — our `messages.ts:5573` already strips orphan tool_results + guards `result.at(-1)?.type !== 'assistant'` with placeholder fallback. Likely already covers CCB's ACP scenario; DEFER-verify-against-ACP-repro, not a clean gap.

### DIVERGENCE / SKIP

- `7b52054f`/`03598d3f`/`897c186f` **Remove max/xhigh effort model whitelist** — INTENTIONAL DIVERGENCE. Our `effort.ts:190-192` downgrade (`max`→`xhigh`→`high`) is protective for z.ai/GLM + DeepSeek which 400 on unsupported effort; CCB's "let the API reject" is worse for our multi-provider default. Keep ours.
- `a91653a0` **Remove FileEditTool quote/tab normalization** — touches "Don't Touch: tool-specific prompts (FileEdit)"; behavior-removal of debatable value. SKIP.
- `e33b17bd` **sideQuery OpenAI/Grok/Gemini routing** — N/A; we route non-Anthropic through `openaiBridge`, not provider-specific sideQuery adapters.
- ~30 commits NOT_APPLICABLE: provider integrations we don't ship (Gemini/Grok/MiMo adapters), `ExecuteExtraTool`/`SearchExtraTools` (CCB rename of ToolSearch internals), Vite/Bun build-split experiments + reverts, version bumps, contributor/doc updates, CI publish workflow.

---

## Audit Progress

| Batch | Commit range | Status | GAPs | ALREADY_HAVE | NOT_APPLICABLE |
|-------|-------------|--------|------|-------------|----------------|
| 1 | 2-82 | [x] | 4 | 2 | 76 |
| 2 | 83-164 | [x] | 7 | 19 | 56 |
| 3 | 165-246 | [x] | 3 | 6 | 73 |
| 4 | 247-328 | [x] | 5 | 8 | 69 |
| 5 | 329-410 | [x] | 3 | 5 | 74 |
| 6 | 411-492 | [x] | 13 | 3 | 66 |
| 7 | 493-574 | [x] | 16 | 6 | 60 |
| 8 | 575-648 | [x] | 15 | 3 | 55 |
| **TOTAL** | **2-648** | **DONE** | **66** | **52** | **529** |

Per-batch research files (`ccb-gap-batch1.md` … `ccb-gap-batch8.md`) and `ccb-audit-instructions.md` were removed in commit `<this commit>` after consolidation — every actionable item is captured in the GAP / ALREADY_HAVE tables below + the Implementation Status section. Pull them from this repo's git history if you need the raw per-commit research notes.

---

## Priority Summary

| Priority | Count | LANDED | VERIFIED-SKIP | DEFERRED | Criteria |
|----------|-------|--------|---------------|----------|----------|
| CRITICAL | 14 | 14 | 0 | 0 | Memory leaks, crashes, API errors (400s), security, broken core features |
| HIGH | 18 | 14 | 3 | 1 | Missing guards/params, feature gaps, unbounded growth, architectural divergence |
| MEDIUM | 22 | 17 | 4 | 1 | Correctness fixes, optimizations, UX improvements |
| LOW | 12 | 9 | 3 | 0 | Minor polish, model name updates, cosmetic fixes |
| **TOTAL** | **66** | **54** | **10** | **2** | |

---

## Implementation Status

Per-gap status with landed-commit SHAs (in `coffeegrind123/openclaude` on `main`).
Open the linked commits with `git show <sha>` from a clone of that repo.

**Legend:**
- `LANDED <sha>` — fix applied, commit on `main`
- `VERIFIED-SKIP` — checked CCB's actual source; intentional architectural divergence or already-correct-in-OC
- `DEFERRED` — not done; substantial port deferred for future work

### CRITICAL (14/14 landed)

| # | Gap | Status | Landed in |
|---|-----|--------|-----------|
| 1 + 48 | firstParty base-URL guard (betas + opus1m) | LANDED | `1594427` |
| 2 | `buildDiffableContent` closure → string | LANDED | `133953a` |
| 3 | `cloneDeep` boundary in claude.ts | LANDED | `7e7f06e` |
| 4 | Memory-overflow trio (SSE buffer, permissionDenials, contentReplacementState) | LANDED | `492cfd1` |
| 5 | `toolUseResult` cleanup + FileRead byte cap | LANDED | `b45bc6a` |
| 6 | Third-party `user_id` sanitization | LANDED | `7ae4771` |
| 7 | Auto mode firstParty whitelist removal | LANDED | `7ed2400` |
| 8 | Long-session memory trio (clearConversation reset + scrollback cap; 3rd already-correct) | LANDED | `cb530fd` |
| 9 | `MAX_SNAPSHOTS` 100 → 20 | LANDED | `1594427` |
| 10 | skill-learning evidence caps | LANDED | `f35eae8` |
| 11 | `truncate()` null guard | LANDED | `1594427` |
| 12 | React conditional-hook violations | LANDED | `cb85b75` |
| 13 | ACP messageSelector require crash | LANDED | `133953a` |
| 14 | NODE_ENV=production + perf shim + OTel skip | LANDED | `b11023b` |

### HIGH (14 landed + 3 verified-skip + 1 deferred)

| # | Gap | Status | Notes |
|---|-----|--------|-------|
| 15 | Hook shell sandboxing | LANDED `cced52c` | opt-in via `sandbox.applyToHooks` |
| 16 + 17 | AGENT_TRIGGERS gate removal | LANDED `25eae8d` | enables cron/`/loop`/ScheduleCronTool |
| 18 | Bridge peer messaging | LANDED `4ba2eb0` | verbatim port from CCB; ingress endpoint not yet on our CCR server (returns informative errors) |
| 19 | AgentTool `fork` parameter | LANDED `246dc6b` | |
| 20 | opus[1m] auto-migration → no-op | LANDED `21f96f5` | |
| 21 | CLAUDE.md → `<project-instructions>` | LANDED `1ad9982` | |
| 22 | React Error Boundary diagnostics | LANDED `21f96f5` | |
| 23 | Incremental Messages lookups | LANDED `1ad9982` | module-level cache + appendOnly fast path |
| 24 | MCP `transformResultContent` `_meta` | LANDED `1ad9982` | options arg with `includeMeta` + `limits` (forward-compat) |
| 25 | Prompt cache hit-rate warning | LANDED `cced52c` | new `utils/cacheWarning.ts`; UI surfacing deferred (React-Compiler risk) |
| 26 | Unified Tool Search | DEFERRED | ~1800 LOC architectural port across `searchExtraTools.ts` + `services/searchExtraTools/` + `SearchExtraToolsTool.ts`; our existing native tool deferral covers core problem |
| 27 | CRLF SSE delimiter | LANDED `222ce27` | |
| 28 | iTerm2 ECMA-48 sequences | LANDED `21f96f5` | full CSI/OSC/DCS/SOS/PM/APC handling |
| 29 | OpenAI const→enum schema | LANDED `21f96f5` | |
| 30 | @-typeahead boundary scoring | LANDED `222ce27` | multi-start scoring per needle[0] occurrence |
| 31 + 32 | DeepSeek empty `reasoning_content` | VERIFIED-SKIP | CCB routes DeepSeek through their OpenAI bridge; ours uses Anthropic-format passthrough — different translation layers |

### MEDIUM (17 landed + 4 verified-skip + 1 deferred)

| # | Gap | Status | Notes |
|---|-----|--------|-------|
| 33 | Drop `prefetchOfficialMcpUrls` | LANDED `a3357c6` | |
| 34 | Bing WebSearch adapter | DEFERRED | ~500 LOC; we have browser-based search via zendriver (different but functional) |
| 35 | Generic OpenAI Chat compat layer | VERIFIED-SKIP | ~1200 LOC; we have NIM bridge covering NIM/OpenRouter; raw OpenAI/Groq/Together not in our user base |
| 36 + 57 | Opus 4.7 routing registration + frontier name | LANDED `4ba2eb0` + `d4c8e97` | verified CCB's port is routing-only (no pricing fabrication); applied with same shape |
| 37 | usePipeIpc lazy require → static | VERIFIED-SKIP | audit explicitly low-impact; lazy is benign in Bun, switch risks latent circular imports |
| 38 | Agent definition cache flush | LANDED `e2940e0` | adds markdown-cache clear to `clearAgentDefinitionsCache` |
| 39 | Tab completion mid-line | LANDED `e2940e0` | `commandInput = value.slice(0, cursor)` |
| 40 | Permission mode 'auto' preserve | LANDED `e2940e0` | |
| 41 | Skill discovery cross-turn dedup | LANDED `2ef5004` | reset on `/clear` |
| 42 | forkedAgent `filterIncompleteToolCalls` | VERIFIED-SKIP | CCB's `forkedAgent.ts:526` has IDENTICAL "Do NOT filter" comment we have at line 520; functional parity (we both call it in agent summary) |
| 43 | UDS peer error handling | LANDED `e2940e0` | `settled` guard, `onSocketError` callback, `UdsPeerConnectionError` class |
| 44 + 45 | Write content + LRU size guards | LANDED `a3357c6` | |
| 46 | `getCommandName` empty-string fallback | LANDED `a3357c6` | |
| 47 | `-r` mode keyboard input | LANDED `2ef5004` | both safety nets applied |
| 48 | (combined with #1 above) | LANDED `1594427` | same fix |
| 49 | `MarkdownTable` React.memo + caches | LANDED `a3357c6` | |
| 50 | Ink ErrorOverview slim props | LANDED `e2940e0` | `{message, stack?}` instead of full Error |
| 51-54 | Autonomy/cron pipeline consolidation | VERIFIED-SKIP | CCB's `turnError` is for autonomy command outcome tracking via `finalizeAutonomyCommandsForTurn`; we have no autonomy command machinery |

### LOW (9 landed + 3 verified-skip)

| # | Gap | Status | Notes |
|---|-----|--------|-------|
| 55 | `y`/`n` keybinding drop | LANDED `d4c8e97` | |
| 56 | opus-4-7 in advisor checks | LANDED `d4c8e97` | |
| 57 | (combined with #36 above) | LANDED `d4c8e97` | `FRONTIER_MODEL_NAME` bumped |
| 58 | Buddy rehatch random seed | LANDED `d4c8e97` | optional `seed?: string` on StoredCompanion + `generateSeed()` |
| 59 | `computeTtftText` polyfill | VERIFIED-SKIP | in `"external" === 'ant'` dead branch in our build; never executes |
| 60 | TungstenPill typeof guard | VERIFIED-SKIP | same dead-branch path |
| 61 | SUMMARIZE_CONNECTOR_TEXT removal | VERIFIED-SKIP | already gated by `shouldIncludeFirstPartyOnlyBetas()` (CRITICAL #1+#48); harmless dead weight on non-firstParty |
| 62 | ModelPicker "Space to toggle" | DEFERRED | our ModelPicker is React-Compiler-compiled AND missing the 1M context UI block entirely; proper port = re-extract source-form |
| 63 + 64 | `attributionModel.ts` for non-Anthropic providers | LANDED `d4c8e97` | provider-specific names: GLM 4.6, DeepSeek V4 Pro, etc. |
| 65 | Slim system prompt | LANDED `d4c8e97` (gitStatus) + `4ba2eb0` (memoryTypes) | gitStatus MAX_STATUS_CHARS 2000→1000; TYPES_SECTION_COMBINED/INDIVIDUAL slimmed ~60% |
| 66 | Remote Control conditional tool injection | VERIFIED-SKIP | CCB's PushNotificationTool POSTs to remote bridge backend; ours fires local terminal notifications — gating would break it |

### Implementation commits (sorted chronologically)

| Commit | Items |
|--------|-------|
| `1594427` | CRITICAL #1, #9, #11, #48 |
| `7ed2400` | CRITICAL #7 |
| `7ae4771` | CRITICAL #6 |
| `25eae8d` | CRITICAL/HIGH #16, #17 |
| `133953a` | CRITICAL #2, #13 |
| `b11023b` | CRITICAL #14 |
| `b45bc6a` | CRITICAL #5 |
| `f35eae8` | CRITICAL #10 |
| `cb85b75` | CRITICAL #12 |
| `492cfd1` | CRITICAL #4 |
| `cb530fd` | CRITICAL #8 |
| `7e7f06e` | CRITICAL #3 |
| `21f96f5` | HIGH #20, #22, #28, #29 |
| `222ce27` | HIGH #27, #30 |
| `246dc6b` | HIGH #19 |
| `1ad9982` | HIGH #21, #23, #24 |
| `cced52c` | HIGH #15, #18 (initial stub), #25 |
| `a3357c6` | MEDIUM #33, #44, #45, #46, #49 |
| `e2940e0` | MEDIUM #38, #39, #40, #43, #50 |
| `2ef5004` | MEDIUM #41, #47 |
| `d4c8e97` | LOW #55, #56, #57, #58, #63, #64, #65 (gitStatus) |
| `4ba2eb0` | HIGH #18 (verbatim port), MEDIUM #36, LOW #65 (memoryTypes) |

### Trust-but-verify pass

After cloning CCB on 2026-05-11 and checking each architectural-divergence
claim against their actual source, three prior skips were upgraded to landed
ports (commit `4ba2eb0`):

- **#18 bridge/peerSessions** — replaced clear-failure stub with CCB's
  actual `postInterClaudeMessage` implementation. Backend-agnostic; works
  if a compatible CCR ingress endpoint appears, returns informative errors
  otherwise.
- **#36/#57 opus-4-7 routing** — verified CCB's port is routing-only (no
  pricing fabrication needed), applied with the same shape.
- **#65 memdir/memoryTypes slim** — applied CCB's TYPES_SECTION_COMBINED/
  INDIVIDUAL ~60% reduction verbatim.

Seven skips were confirmed correct after source verification (#42, #51-#54,
#66, #31/#32, #62, #61, #26).

---

## CRITICAL GAPs

| # | SHA | B | Subject | OC File(s) | What to fix |
|---|-----|---|---------|------------|-------------|
| 1 | d136872c | 7 | First-party beta headers leak to third-party APIs | `src/utils/betas.ts:215-218`, `src/utils/model/model.ts:362-365` | `shouldIncludeFirstPartyOnlyBetas()` and `isOpus1mMergeEnabled()` check `getAPIProvider()` but NOT `isFirstPartyAnthropicBaseUrl()`. Anthropic beta headers sent to z.ai/DeepSeek/NIM — causes 400 errors on strict third-party APIs |
| 2 | e7220c53 | 7 | buildDiffableContent closure retains system+tools+model refs | `src/services/api/promptCacheBreakDetection.ts:65-68` | `buildDiffableContent: () => string` (lazy closure) → `buildDiffableContent: string` (pre-computed). Closure captures system/toolSchemas/model preventing GC |
| 3 | 75952bde | 7 | No deep-clone serialization boundary in claude.ts queryModel | `src/services/api/claude.ts:1442-1587` | CCB adds `cloneDeep()` boundary + nulls out originals (`messagesForAPI = null!`, `system = null!`, `allTools = null!`) so GC reclaims while streaming. OC streaming generator retains full original arrays — 120-320MB waste |
| 4 | ab0bbbc4 | 7 | Memory overflow: SSE buffer, compact cleanup, permissionDenials | `src/QueryEngine.ts:248`, `src/cli/transports/SSETransport.ts:350`, `src/screens/REPL.tsx:1779` | (1) SSE buffer has no 1MB overflow cap with connection-drop; (2) No `registerCompactCleanup()` to reset contentReplacementState; (3) `permissionDenials` only reset in constructor (line 204), not in submit |
| 5 | f7243000 | 7 | No toolUseResult cleanup — FileRead/Grep results accumulate | `src/query.ts:479-492`, `src/services/compact/compact.ts:336-358` | CCB adds `stripToolUseResults()` in compact + `delete msg.toolUseResult` loop in query.ts before API call + FileReadTool byte-length fast-rejection (4x token limit). OC has none of these |
| 6 | 941bcbd2 | 8 | Third-party API user_id validation error | `src/services/api/claude.ts:568-575` | OC `getAPIMetadata()` always sends full JSON user_id (device_id+account_uuid+session_id). Non-Anthropic APIs (DeepSeek/z.ai) validate against `^[a-zA-Z0-9_-]+$` and reject `{`, `"`, `:` characters. CCB sends only hex device_id for third-party |
| 7 | dc3d3e88 | 8 | Auto mode broken on z.ai/DeepSeek — firstParty-only gate | `src/utils/betas.ts:160-195` | `modelSupportsAutoMode()` has firstParty-only gate (line 166) that blocks all non-Anthropic providers. Since OC uses z.ai/DeepSeek, auto mode is effectively disabled. CCB removes ALL whitelist logic: `feature('TRANSCRIPT_CLASSIFIER') ? true : false` |
| 8 | f5c3ee5b | 6 | Long-running session memory leak (3 fixes) | Multiple files | (1) `clearConversation` doesn't reset `lastAPIRequest`/`lastAPIRequestMessages`/`lastClassifierRequests`; (2) No `MAX_FULLSCREEN_SCROLLBACK=500` cap; (3) Progress entry dedup only checks last message, not full queue |
| 9 | 3f1c8468 | 7 | MAX_SNAPSHOTS=100 causes unbounded file checkpoint growth | `src/utils/fileHistory.ts:54` | CCB reduced `MAX_SNAPSHOTS` from 100 → 20. OC still at 100 — 100 snapshots × full file backups = unbounded memory growth |
| 10 | 1a1d5705 | 6 | skill-learning evidence unbounded growth | `src/services/skillLearning/` | CCB adds caps: `MAX_EVIDENCE_ENTRIES=10`, observationIds cap=20, evidence lines cap=20 per append, `MAX_SKILL_FILE_BYTES=50000`. OC has no caps |
| 11 | b8b48bf7 | 6 | truncate() null/undefined crash | `src/utils/truncate.ts:140` | CCB adds null guard: `str: string → str: string\|undefined\|null, if str==null return ''`. OC has unguarded `string` param — crashes on null input |
| 12 | 8ba51ede | 8 | Conditional hooks React violation — crash | `src/screens/REPL.tsx`, `src/components/PromptInput/*.tsx` | OC has `feature('X') ? useHook() : default` patterns that violate React hook rules ("Rendered fewer hooks than expected"). CCB moves ALL hooks to unconditional top-level with value gating |
| 13 | 4dcbaf1e | 6 | ACP messageSelector unprotected require crash | `src/QueryEngine.ts:87-89` | CCB wraps messageSelector `require()` in try/catch + null checks at call sites. OC has unprotected lazy require |
| 14 | b28de717 | 7 | No performanceShim + NODE_ENV + OTel skip gate — 12MB+ waste | `build.ts:24`, `src/entrypoints/cli.tsx:1-5` | CCB adds `NODE_ENV=production` (eliminates React _debugStack), `performanceShim.js` import, OTel skip when disabled. OC has none — React dev-mode objects + OTel PerformanceMeasure accumulate |

---

## HIGH Priority GAPs

| # | SHA | B | Subject | OC File(s) | What to fix |
|---|-----|---|---------|------------|-------------|
| 15 | 2e4d6e21 | 2 | Hook shell commands unsandboxed | `src/utils/hooks.ts:execCommandHook` | CCB wraps hook commands with SandboxManager (network-only sandbox). OC hooks execute arbitrary shell commands from settings.json without sandbox — data exfiltration risk via curl/wget |
| 16 | 33fe4940 | 1 | ScheduleCronTool AGENT_TRIGGERS gate cripples cron | `src/tools/ScheduleCronTool/prompt.ts:37` | `isKairosCronEnabled()` gated behind `feature('AGENT_TRIGGERS')` which is DCE'd to false in source mode — cron scheduling permanently disabled |
| 17 | 2934f300 | 1 | AGENT_TRIGGERS gate removal (6 files) | `src/cli/print.ts:365`, `src/constants/tools.ts:86`, `src/screens/REPL.tsx:199`, `src/skills/bundled/index.ts:71`, `src/tools.ts:29` | Remove `feature('AGENT_TRIGGERS')` from cron scheduler, tools allowlist, loop skill registration, REPL hook, and cronTools array |
| 18 | 74e51e7e | 2 | Remote Control peer sessions + webhook sanitizer missing | `src/bridge/peerSessions.ts` (stub `export {}`), `src/bridge/webhookSanitizer.ts` (nonexistent) | CCB has ~136 LOC of cross-session bridge messaging + secret redaction. OC has remoteControlServer command but bridge peer layer is stubbed |
| 19 | ba74e097 | 7 | AgentTool missing `fork: boolean` parameter | `src/tools/AgentTool/AgentTool.tsx:148-412` | CCB added `fork: boolean` to AgentTool input schema, wired through call() with FORK_SUBAGENT gating. OC has FORK_SUBAGENT + `/fork` command but model can't route to fork via AgentTool schema |
| 20 | e8759f34 | 8 | opus[1m] auto-migration overrides user model choice | `src/migrations/migrateOpusToOpus1m.ts:24-44` | OC still forces opus→opus[1m] migration. CCB makes it a no-op to respect user manual model selection |
| 21 | 84f12f34 | 8 | CLAUDE.md wrapped in generic system-reminder degrades instruction weight | `src/utils/api.ts:451-475`, `src/services/api/claude.ts:1407-1412` | OC wraps claudeMd in `<system-reminder>` with "may or may not be relevant" disclaimer. CCB extracts as independent `<project-instructions>` at messages[0] |
| 22 | 2006ab25 | 8 | React Error Boundary returns null — blank screen on crash | `src/components/SentryErrorBoundary.ts:17-23` | OC's ErrorBoundary silently returns null. CCB outputs diagnostics to stderr + renders error Box in UI |
| 23 | 198c09b2 | 7 | No incremental lookups update — full 8-Map/Set rebuild on every delta | `src/components/Messages.tsx:518-595` | CCB adds `updateMessageLookupsIncremental()` for partial rebuild when only new messages appended. OC does full 8-Map/Set rebuild per streaming delta |
| 24 | 26ddbda8 | 7 | MCP transformResultContent missing _meta passthrough + limits param | `src/services/mcp/client.ts:2490-2564` | CCB aligns with upstream 2.1.128: adds `limits?: ImageLimits` + `includeMeta = false` params + `_meta` preservation. OC signature has only 2 params (resultContent, serverName) |
| 25 | e3c0699f | 8 | Prompt cache hit rate detection and warning (new feature ~130 LOC) | New file: `src/utils/cacheWarning.ts` | CCB adds cache hit rate display in ContextVisualization + warning when hit rate drops. OC has no cache monitoring |
| 26 | 7be08f53 | 8 | Unified Tool Search system (7-commit architecture change) | New dirs: `src/services/searchExtraTools/` | CCB replaces tool_reference/defer_loading with provider-agnostic CORE_TOOLS whitelist + TF-IDF + ExecuteExtraTool. OC uses Anthropic-first deferred tools with text fallback |
| 27 | bb078362 | 4 | CRLF SSE frame parsing (\\r\\n\\r\\n delimiter) | `src/cli/transports/SSETransport.ts:67`, `src/services/api/openaiBridge/streamTranslator.ts:468` | OC uses `\n\n` delimiter only. CCB regex `/\r?\n\r?\n/g` handles CRLF + normalizes trailing \r. Affects providers sending CRLF SSE |
| 28 | 4b440479 | 4 | iTerm2 terminal response sequences leak into REPL input | `src/utils/earlyInput.ts:104-117` | OC ESC handling only checks single-byte terminators (0x40-0x7E). CCB handles full ECMA-48 CSI/DCS/OSC/SOS/PM sequences — XTVERSION responses leak into input buffer |
| 29 | e88dcb2f | 3 | OpenAI adapter const→enum conversion missing in tool schemas | `src/utils/schemaSanitizer.ts:251-255` | OpenAI rejects `const` in tool call schemas. CCB converts to `enum` with single value. OC schema sanitizer doesn't do this conversion |
| 30 | 221fb6eb | 1 | @ typeahead file search greedy-leftmost needle matching | `src/native-ts/file-index/index.ts:222` | Old algorithm: leftmost indexOf for needle[0] — searching "sett" fails on "src/settings/" because 's' matches early in "src/" and subsequent chars fail. CCB: collect all word-boundary start positions, try each, keep best score |
| 31 | da6d0636 | 6 | DeepSeek thinking detection gap | `src/services/api/openaiBridge/` | CCB fixed DeepSeek V4 thinking mode: empty reasoning_content (direct-answer without thinking) must be echoed back as `reasoning_content: ""` or DeepSeek returns 400. OC openaiBridge needs verification |
| 32 | 1b10ea39 | 7 | DeepSeek V4 empty reasoning_content handling | `src/services/api/openaiBridge/` | Same as da6d0636 — verify OC's streamTranslator preserves empty reasoning_content in multi-turn conversations |

---

## MEDIUM Priority GAPs

| # | SHA | B | Subject | OC File(s) | What to fix |
|---|-----|---|---------|------------|-------------|
| 33 | 2e4d6e21 | 2 | prefetchOfficialMcpUrls removed | `src/main.tsx:435` | OC still calls `void prefetchOfficialMcpUrls()` in startDeferredPrefetches — unnecessary Anthropic registry network call every startup |
| 34 | e48da395 | 2 | Bing WebSearch API adapter (~500 LOC) | New files: `src/tools/WebSearchTool/adapters/` | CCB added Bing API as fast serverless fallback. OC's WebSearchTool uses browser automation only |
| 35 | 00b044e8 | 2 | Generic OpenAI Chat compatibility layer | New dir: `src/services/api/openai/` | CCB has ~1,200 LOC generic OpenAI adapter. OC has NIM bridge only — covers NIM/OpenRouter but not raw OpenAI/Groq/Together |
| 36 | 23bb09d2 | 6 | Model defaults not bumped to Opus 4.7 | `src/utils/model/model.ts` | CCB updated defaults to opus-4-7, removed `isAliasOrAliasWithSuffix` recursion guards. OC still uses opus-4-6 defaults |
| 37 | ca1c87f4 | 6 | usePipeIpc lazy require() crash risk | `src/hooks/usePipeIpc.ts:22-37` | CCB changed lazy require() functions to static imports. OC still uses lazy require(). Low impact in Bun but structurally diverged |
| 38 | eb833da3 | 6 | Agent creation cache not flushed | `src/tools/AgentTool/loadAgentsDir.ts:395-398` | CCB clears `loadMarkdownFilesForSubdir.cache` in `clearAgentDefinitionsCache()`. OC only clears `getAgentDefinitionsWithOverrides.cache` |
| 39 | ad09f38f | 6 | Tab completion mid-line bug | `src/hooks/useTypeahead.tsx` | CCB uses `commandInput` (= value substring to cursor) to fix mid-line command completion. OC uses full value string |
| 40 | fc438bd2 | 6 | Permission mode auto handling in Config | `src/components/Config.tsx` | OC converts "auto" to "default" in permission mode UI. CCB preserves "auto" for BYOC mode detection |
| 41 | 1c3b280c | 6 | Multi-turn skill discovery cache dedup | `src/utils/attachments.ts` | CCB adds skill discovery dedup across turns. OC needs equivalent cache-busting |
| 42 | 52b61c2c | 6 | Agent communication memory growth (forkedAgent boundary) | `src/utils/forkedAgent.ts:520` | CCB adds `filterIncompleteToolCalls` as separate module with tests + boundary enforcement. OC has function in `runAgent.ts` but comments say NOT to filter in `forkedAgent.ts` |
| 43 | 42661498 | 6 | UDS peer connection error handling | `src/utils/udsClient.ts:176-186` | CCB adds `onSocketError` callback, `UdsPeerConnectionError`, settled guard, `cleanupListeners`, timeout. OC has older simpler impl |
| 44 | d3a607e4 | 3 | Write tool content can be non-string from JSON deser | `src/utils/queryHelpers.ts:388-397` | CCB adds type guard for Write tool content. OC may crash on non-string content from JSON deserialization |
| 45 | 354c11f0 | 3 | LRU cache size calc doesn't handle nested objects | `src/utils/fileStateCache.ts:37` | CCB adds nested object handling in `sizeCalculation`. Related to d3a607e4 |
| 46 | 562e9daa | 4 | getCommandName returns undefined for stubs | `src/types/command.ts:216` | OC returns `cmd.userFacingName?.() ?? cmd.name` — if both undefined, returns undefined instead of string. CCB: `return name \|\| ''` |
| 47 | e86573ac | 4 | -r mode keyboard input unresponsive (2 fixes) | `src/ink/components/App.tsx:231,274` | (1) No safety net to remove stale readable listeners after stopCapturingEarlyInput(); (2) No React 19 layout-effect guard when rawModeEnabledCount decrements to 0. Impact limited: fullscreen defaults OFF |
| 48 | 86df024e | 7 | isOpus1mMergeEnabled() missing firstParty base URL guard | `src/utils/model/model.ts` | Same as d136872c — prevents first-party model features activating on third-party APIs |
| 49 | 3a2b6dde | 7 | MarkdownTable not wrapped in React.memo | `src/components/MarkdownTable.tsx` | CCB adds React.memo + per-render caches (formatCache, plainTextCache) for table rendering efficiency |
| 50 | 18d6656a | 7 | Ink ErrorOverview accepts full Error objects | `packages/@ant/ink/src/components/App.tsx:131-148` | CCB changes ErrorOverview to accept `{message, stack?}` instead of full Error objects (reduces retained references). Also adds flushLangfuse() after endTrace |
| 51 | f2e9af49 | 7 | Autonomy lifecycle — unified dedup + abort controller cleanup | `src/cli/print.ts`, `src/utils/autonomyRuns.ts` | CCB adds `createAutonomyQueuedPromptIfNoActiveSource` with sourceId dedup + `setAbortController(null)` when all commands skipped |
| 52 | 6b7cfda9 | 7 | Legacy cron dispatch refactored to unified pipeline | `src/cli/print.ts:2823-2843`, `src/services/compact/postCompactCleanup.ts:72` | CCB refactors legacy cron onFire to use same unified dedup pipeline as onFireTask |
| 53 | 7a6e65ca | 7 | dispatchHeadlessCronCommand shared pipeline extraction | `src/cli/print.ts:2819-2898` | CCB extracts shared pipeline for 3 cron entry points with cancel-on-late-shutdown contract. OC has separate non-unified paths |
| 54 | 189766c5 | 7 | turnError variable + logError in handlePromptSubmit | `src/utils/handlePromptSubmit.ts:496-588` | CCB adds `turnError` variable + `logError` + `toError` imports to prevent unhandled rejection when cron dispatch throws inside async IIFE |

---

## LOW Priority GAPs

| # | SHA | B | Subject | OC File(s) | What to fix |
|---|-----|---|---------|------------|-------------|
| 55 | 8442aaad | 5 | Confirmation keybinding 'n' removal | `src/keybindings/defaultBindings.ts:137-138` | Removes 'y'/'n' from Confirmation context (prevents accidental 'n' close). OC still has them |
| 56 | fb41513b | 5 | Missing opus-4-7 in advisor model checks | `src/utils/advisor.ts:93` | CCB adds `m.includes('opus-4-7')` to `modelSupportsAdvisor()` and `isValidAdvisorModel()`. OC only lists opus-4-6 |
| 57 | 2247026b | 5 | FRONTIER_MODEL_NAME still Opus 4.6 | `src/constants/prompts.ts:139,143`, `src/constants/figures.ts:13` | CCB updates to Claude Opus 4.7, opus ID to `claude-opus-4-7`. OC still references 4.6 |
| 58 | f71530a1 | 1 | Buddy rehatch always produces same companion | `src/buddy/companion.ts:138`, `src/buddy/types.ts` | CCB adds `generateSeed()` random seed, stores on CompanionSoul, uses `rollWithSeed()`. OC re-hatch is deterministic |
| 59 | 4ab4506d | 2 | computeTtftText undefined in compiled binary | `src/components/Spinner.tsx:223` | Works from Bun source but bundler-injected global not polyfilled — may fail in compiled binary |
| 60 | a02a9fc4 | 2 | TungstenPill typeof guard | `src/components/PromptInput/ PromptInputFooterLeftSide.tsx:365` | CCB adds `typeof TungstenPill === 'function'` guard. OC uses literal comparison (DCE'd to false) |
| 61 | c252294d | 2 | SUMMARIZE_CONNECTOR_TEXT anti-distill beta header | `src/constants/betas.ts:30`, `src/utils/betas.ts:286-291` | OC still sends `summarize-connector-text-2026-03-13` beta header — dead code on non-Anthropic endpoints |
| 62 | 29a1edbf | 7 | ModelPicker "Space to toggle" hint when 1M off | `src/components/ModelPicker.tsx:282` | CCB adds `<Text color="subtle"> · Space to toggle</Text>` in off-state |
| 63 | 771e3dbc | 8 | Attribution model name wrong for non-Anthropic providers | New file: `src/utils/attributionModel.ts` | CCB checks provider-specific env vars (OPENAI_MODEL, GEMINI_MODEL, GROK_MODEL). OC shows wrong model name |
| 64 | f7f69b75 | 8 | Model alias resolution shows "haiku" instead of real name | `src/utils/attributionModel.ts` | CCB removes `getUserSpecifiedModelSetting()` branch and unifies through `getMainLoopModel()`+`resolveProviderModel()` |
| 65 | 2f86485d | 8 | Slim system prompt (~60% token reduction) | `src/constants/prompts.ts`, `src/context.ts:424`, `src/memdir/memoryTypes.ts` | CCB reduces gitStatus MAX_STATUS_CHARS 2000→1000, removes auto-memory type descriptions, merges sections. OC still verbose |
| 66 | 4fc95bd5 | 8 | Remote Control conditional tool injection | Various tool files | CCB adds `isBridgeEnabled()` gates to PushNotificationTool/SendUserFileTool/BriefTool/ExecuteExtraTool. OC has tools but no bridge-gated `isEnabled()` |

---

## ALREADY_HAVE (selected — see batch files for full list)

| # | SHA | B | Subject | Why we already have it |
|---|-----|---|---------|------------------------|
| 1 | ab7556e3 | 3 | auto dream enabled | `/dream` skill + autoDream already implemented |
| 2 | 3fff2a07 | 3 | teach-me skill | Already ported from CCB |
| 3 | cd70c1b7 | 3 | MACRO fallback | MACRO already defined at top of cli.tsx |
| 4 | e32c159f | 2 | disable auto-update | OC uses GitHub Releases API auto-updater |
| 5 | 78144b4d | 2 | disable Datadog logging | Telemetry already stubbed |
| 6 | e74c009e | 2 | GrowthBook custom server | GrowthBook disabled (returns defaults) |
| 7 | c57ad656 | 1 | buddy command support | Full buddy via dual-fallback pattern |
| 8 | a889ed84 | 1 | Gates tab removed from Settings | OC already has `t7 = []` |
| 9 | 379e40f1 | 4 | fullscreen mode disabled | OC defaults `return false` at fullscreen.ts:143 |
| 10 | 0c53796d | 4 | daemon supervisor + remoteControlServer | OC has daemon mode + remoteControlServer command |
| 11 | 4e1e681a | 4 | debug restriction removal | OC has same guard but Bun doesn't trigger node --inspect |
| 12 | e6affc70 | 4 | fork command stub fixed | OC has fork-impl.ts + index.ts with full AgentTool fork integration |
| 13 | 01cf45f4 | 4 | permission panel fix | Both RecentDenialsTab.tsx and WorkspaceTab.tsx import useTabHeaderFocus |
| 14 | e770f1ef | 4 | claudeInChrome MCP | OC has full claudeInChrome MCP |
| 15 | 96f6d2c7 | 3 | feature flags enabled | All 87 flags enabled in OC bundle polyfill |
| 16 | 3cf94fbd | 5 | low-context guard for autoDream/sessionMemory | OC guards with `isLowContextMode()` at stopHooks.ts:138 |
| 17 | 3cb1e50b | 5 | ACP protocol support | Already ported from CCB |
| 18 | 1837df5f | 5 | skill learning system | Already ported from CCB in April 2026 |
| 19 | c4775fff | 5 | autonomy command system | Already ported in §9 slash command ports |
| 20 | 6c5df395 | 5 | cachedMicrocompact | Already ported — full implementation |
| 21 | 03811f97 | 6 | SSH Remote | Already ported |
| 22 | f2dd5142 | 6 | BRIDGE_MODE/DAEMON decoupling | OC enables DAEMON via all-flags-true |
| 23 | cf33c060 | 6 | DeepSeek max effort | OC modelSupportsEffort defaults true for firstParty |
| 24 | 08cd02cd | 7 | highlight LRU cache | OC color-diff has cached HLJSApi instance |
| 25 | 71c89e9d | 7 | theme switching fix | Different theme architecture, same behavior |
| 26 | 8a5ef8c9 | 7 | UX error message improvements | Already in upstream Anthropic patterns |
| 27 | 4d0048a6 | 7 | permission prompt wording | Upstream Anthropic already has similar UX |
| 28 | 6ff839d6 | 7 | compaction error messages | Upstream Anthropic has similar patterns |
| 29 | 2f150d3e | 8 | statusLine refreshInterval | OC already supports refreshInterval |
| 30 | 12f5aedf | 8 | diff highlight rendering | OC imports StructuredDiffList + full diff rendering |
| 31 | 8cfe9b6d | 8 | COORDINATOR_MODE enabled | All 87 feature flags enabled via bundle polyfill |
| 32 | 958ac3a0 | 8 | UDS_INBOX/LAN_PIPES enabled | All features enabled via bundle polyfill |

Full ALREADY_HAVE details in `/tmp/ccb-gap-batch{1-8}.md`

---

## Implementation Notes

1. **Batch 7 has the most CRITICAL gaps** (8 of 14) — memory leaks from closures, missing GC boundaries, SSE buffer overflow. These cumulative fixes add up to 200-500MB memory savings in long sessions.

2. **Provider-boundary leaks** (d136872c, 86df024e, dc3d3e88) are specific to openclaude's multi-provider architecture. CCB made these fixes because they too support non-Anthropic endpoints. The beta-header leak and auto-mode whitelist are the most impactful for z.ai/DeepSeek users.

3. **The Unified Tool Search** (7be08f53 + 6 related commits) is the largest architectural gap. CCB replaces Anthropic-first tool_reference blocks with a provider-agnostic CORE_TOOLS + TF-IDF + ExecuteExtraTool system. This would be a substantial port but aligns with OC's existing third-party-first design.

4. **AGENT_TRIGGERS feature gate** (33fe4940, 2934f300) disables cron scheduling, loop skill, and scheduled tasks hooks in source mode due to Bun's `bun:bundle` DCE. Fix is straightforward: remove the feature gate ternary and use `from 'bundle'` imports or direct checks.

5. **File-specific fix locations** are documented in each GAP row above and in more detail in the per-batch files.
