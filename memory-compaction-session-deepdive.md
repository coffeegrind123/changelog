---
name: §10 Memory / Compaction / Session deep-dive (CCB / Gitlawb / openclaude)
description: Row-by-row source-level analysis of the memory, compaction, and session area — which forks really ship what, which claims in fork-parity-audit.md are wrong, and concrete adapt-recommendations.
type: audit-supplement
---

# §10 Memory / Compaction / Session — Source-Level Deep-Dive

> Date: 2026-04-24
> Supplements: `fork-parity-audit.md` §10
> Sources: `/tmp/ccb-docs/src`, `/tmp/gitlawb-oc/src`, `/home/claudeuser/openclaude/src`

Every row in §10 was re-verified by reading the actual source files across all three forks. The headline: **the summary table had 4 wrong cells** (one outright false positive for Gitlawb, one false negative for ours, and two over-optimistic ✅'s where the file is actually a stub). Those corrections are flagged per-row below. At the bottom, a concrete adapt-list with 6 recommended backports, ranked by value × effort.

---

## Row-by-row verdicts

Status marker in parentheses is the **verified** state. `audit-was-wrong:` flags where §10 disagrees with source.

### 1. File-based project memory (MEMORY.md + sidecars)
**(all three ✅ — substantially identical core, we extend)**

- **CCB** — `src/memdir/` = 1749 lines across 9 files (`memdir.ts` 507, `paths.ts` 278, `teamMemPaths.ts` 292, `memoryTypes.ts` 271, `findRelevantMemories.ts` 147, `teamMemPrompts.ts` 100, `memoryScan.ts` 94, `memoryAge.ts` 53, `memoryShapeTelemetry.ts` 7).
- **Gitlawb** — `src/memdir/` = 1801 lines across 9 files (same layout + `memoryScan.test.ts` 59). Core files byte-identical to CCB.
- **Ours** — `src/memdir/` = 2594 lines across **12** files. Adds `memdirGit.ts` (224), `memdirWrite.ts` (244), `memoryExportImport.ts` (388) — the provenance-frontmatter + cross-process-lock + git-versioning + export/import subsystem shipped in commit `09f6df0`. `memoryShapeTelemetry.ts` is stubbed (1 line vs CCB's 7).

Our extensions are clean additive — no changes to the CCB/Gitlawb baseline modules.

### 2. Sonnet-driven memory recall injection
**(all three ✅)** Part of `memdir/findRelevantMemories.ts` — 140–147 lines across forks, essentially identical.

### 3. Extract memories service
**(all three ✅ — byte-identical)**

`src/services/extractMemories/extractMemories.ts` is **identical 615 lines** across all three forks. Same for `prompts.ts` (154 lines). No meaningful drift.

### 4. Session memory
**(all three ✅ — trivial drift)**

- CCB: 1033 lines (`sessionMemory.ts` 502, `prompts.ts` 324, `sessionMemoryUtils.ts` 207)
- Gitlawb: 1026 lines (same split, `sessionMemory.ts` 495)
- Ours: 1037 lines (`sessionMemory.ts` 506)

Our +11 lines vs Gitlawb is a **more detailed permission-denied reason for the memory-extraction subagent** (tells the subagent "the FileEdit schema is already available — do not call ToolSearch — only call FileEdit with file_path=X"). Helps the agent recover gracefully from a misdirected edit. Gitlawb's and CCB's version is a terse `"only FileEdit on <path> is allowed"`.

### 5. Team memory (Anthropic backend)
**(all three ✅ — identical except for our backend switch)**

CCB + Gitlawb ship identical 2167-line `src/services/teamMemorySync/` (index 1256, watcher 387, types 156, secretScanner 324, teamMemSecretGuard 44). **Ours is 2769 lines** — same 5 files plus `githubBackend.ts` (545 lines) plus small `index.ts` (+50) + `watcher.ts` (+7) hooks that route through the GitHub backend when `TEAMMEM_GITHUB_REPO=owner/repo` is set.

### 6. Team memory GitHub backend
**(our unique)** Already tracked as ours-only in §19 of the main audit.

### 7. Team memory secret scanner
**(all three ✅ — byte-identical)** `secretScanner.ts` + `teamMemSecretGuard.ts` = same 324 + 44 lines across all three.

### 8. MicroCompact (single tool)
**(all three ✅ — Gitlawb materially improves; we should adopt)**

`microCompact.ts`:
- CCB: 530 lines
- Gitlawb: 536 lines
- Ours: 530 lines (matches CCB exactly on the core logic)

The +6 lines in Gitlawb are **`isCompactableTool(name)` — a helper that treats any MCP tool (`mcp__*` prefix) as compactable in addition to the built-in tool list**:

```typescript
const MCP_TOOL_PREFIX = 'mcp__'
export function isCompactableTool(name: string): boolean {
  return COMPACTABLE_TOOLS.has(name) || name.startsWith(MCP_TOOL_PREFIX)
}
```

The call site at line 240 uses `isCompactableTool(block.name)` instead of `COMPACTABLE_TOOLS.has(block.name)`. Net effect: MCP tool outputs get microcompacted alongside Read/Edit/Grep/Glob/Bash/WebFetch/WebSearch outputs.

**Impact on us:** we ship 200+ MCP tools by default when Ghidra + Zendriver + Computer Use MCP servers are installed. Ghidra decompile outputs routinely exceed 100KB; zendriver screenshots are base64 blobs of several MB. Right now none of that gets microcompacted — only the 8 built-ins. This is a material leak.

**Adapt recommendation: YES. Tier 1, ~15 minutes.** Three-line addition + one call-site swap. Gitlawb also uses the same `isCompactableTool` in their `compressToolHistory.ts` (row #16 below), so we'd also unlock that if/when we port it.

### 9. Cached MicroCompact
**(audit-was-wrong: only CCB has a real impl)**

- **CCB — 112 lines, REAL.** Tracks tool IDs, when >10 tool_results accumulate it produces a `{type: 'cache_edits', edits: [{type: 'delete_tool_result', tool_use_id: id}, ...]}` block that instructs the Anthropic API to drop old tool results from the prompt cache while keeping the last 5. Gated on `CLAUDE_CACHED_MICROCOMPACT=1` and `isModelSupportedForCacheEditing()` regex that matches `/claude-[a-z]+-4[-\d]/` (Claude 4.x families).
- **Gitlawb — 12 lines, STUB.** All functions return `false`/`null`.
- **Ours — 29 lines, STUB.** Type surface present (`CachedMCState`, `CacheEditsBlock`, `PinnedCacheEdits`), all functions no-op / return `false`/`{supportedModels: []}`.

§10 audit row says `— ✅ ✅` for CCB/Gitlawb/ours. Wrong: should be **CCB ✅, Gitlawb ❌, ours ⚠️** (types wired at call sites per CLAUDE.md stubs table, logic no-ops).

**Adapt recommendation: YES for first-party Anthropic users, Tier 2, ~2–3 hours.** 112-line port + verification that our existing wiring in `microCompact.ts` invokes it correctly. Main value: reduces prompt cache token waste on long Claude 4.x sessions (a user with Claude.ai Pro/Team subscription sees meaningful cost reduction). Skipped for non-Claude providers via the model regex.

### 10. Session Memory Compact
**(all three ✅ — byte-identical)**

`sessionMemoryCompact.ts` is **identical 630 lines** across all three forks (one trailing `ant-only` vs `internal-only` comment diff). No drift.

### 11. Full message compaction
**(all three ✅ — we extend)**

`compact.ts`:
- CCB: 1711 lines
- Gitlawb: 1712 lines (essentially identical)
- Ours: 1768 lines (+57 over Gitlawb)

Our additions over Gitlawb (verified by diff):
- **`recoveryReason?: string` parameter on `compactConversation()`** — observe-side annotation that surfaces on the PreCompact hook's `custom_instructions` field but never reaches the summarizer. Clean split: `customInstructions` steers the LLM, `recoveryReason` tells observability what triggered the compact. Used by the forced-PTL recovery path.
- **`isPromptTooLongMessage()` check in the post-compact error path** — catches the 429 "Extra usage required" variant that starts with "API Error:" instead of the classic PROMPT_TOO_LONG prefix.
- **`pruneThinkingFromOlderTurns`** — import + call for thinking-block cleanup during compact.
- **`logPermissionContextForAnts(appState.toolPermissionContext, 'summary')`** — ant-only usage telemetry hook.
- **PreCompact hook blocked path returns empty result early** with `userDisplayMessage` so hooks can veto.

All are additive. No regression against upstream shape.

### 12. Context Collapse (3-tier overflow recovery)
**(audit-was-wrong: Gitlawb's "full impl" is actually 7 lines)**

- **CCB — 82 lines, STUB.** Full type surface (`ContextCollapseStats`, `CollapseResult`, `DrainResult`), all functions return `{messages, committed: 0}` or `false`. `_contextCollapseEnabled = false` default.
- **Gitlawb — 7 lines, STUB.** Two functions: `isContextCollapseEnabled() → false`, `getContextCollapseState() → null`. That's it. **Way less than CCB.**
- **Ours — 26 lines, STUB.** Same essential exports as CCB's stub but tighter: `applyCollapsesIfNeeded`, `recoverFromOverflow`, `isWithheldPromptTooLong`, `initContextCollapse`, `isContextCollapseEnabled` — all no-op.

§10 audit row says `⚠️ ✅ ✅` (CCB/Gitlawb/ours). **All three should be ⚠️ stub.** Our overflow recovery doesn't live in `contextCollapse/` — it lives in **`reactiveCompact.ts` + the forced-autoCompact fallback path**. The audit description for this row was already right in spirit ("Ours: real + Reactive Compact + PTL recovery") but the per-fork column flags were wrong for Gitlawb.

**Correction to apply to the main audit.**

### 13. Reactive Compact (pivot-based partial compact on PTL)
**(our unique — confirmed)**

- CCB: 22-line stub (`tryReactiveCompact → null`, `isReactiveCompactEnabled → false`, all stubs). Audit row already classifies this ❌ for CCB.
- Gitlawb: no file.
- Ours: **316 lines real**. Picks pivot index based on `getPromptTooLongTokenGap()` + `PEEL_TOKEN_SAFETY_MARGIN` (15K extra beyond reported gap), groups messages by API round via `groupMessagesByApiRound`, falls back to `DEFAULT_PEEL_FRACTION = 0.3` if no gap reported. Media-size errors short-circuit via `stripImagesFromMessages` before the LLM call. Single-attempt per turn semantics; hands off to forced auto-compact if still PTL.

No change — row is correct.

### 14. Forced auto-compact fallback
**(our unique — confirmed)**

Embedded in our `autoCompact.ts` as the `force?: boolean` parameter to `shouldAutoCompact()` / `autoCompactIfNeeded()`. Bypasses the client-side estimated-token threshold check; trusts the API's overflow report. Used by `query.ts` PTL path when reactive is disabled or returns null.

CCB + Gitlawb have no equivalent `force` path. Gitlawb has a **different valuable fix**: a floor on `getEffectiveContextWindowSize()` that prevents the threshold from going negative when `reservedTokensForSummary > contextWindow` (fix for #635 on unknown 3P models with small context windows). We currently achieve similar safety via `isLowContextMode()` + `getAutoCompactBufferTokens(model)` — but that only fires for DeepSeek. Other unknown 3P providers with small context windows could still hit the #635 trap.

**Gap:** Gitlawb's universal floor is strictly safer than our DeepSeek-specific scaling. **Adapt recommendation: YES, Tier 1, ~15 minutes.** Add the 5-line floor inside `getEffectiveContextWindowSize()` as a universal safety net on top of our lowContextMode scaling:

```typescript
// Floor: effective context must be at least summary reservation + usable buffer.
const autocompactBuffer = getAutoCompactBufferTokens(model)
const effectiveContext = contextWindow - reservedTokensForSummary
return Math.max(effectiveContext, reservedTokensForSummary + autocompactBuffer)
```

### 15. Snip output compaction
**(our unique — confirmed)**

- CCB: 17-line stub (explicitly labelled `// Auto-generated stub`).
- Gitlawb: 4-line stub (`snipCompact() → null`).
- Ours: 104 lines real (`services/compact/snipCompact.ts`) + 22 lines `snipProjection.ts` (boundary marker + backward scan for last `snip_boundary`).

Gated on `snipEnabled` setting (default false). Threshold/target percent: `SNIP_THRESHOLD_PCT = 0.80`, `SNIP_TARGET_PCT = 0.50`. Emits `system/snip_boundary` markers into the transcript.

No change — row is correct.

### 16. Session transcript (JSONL)
**(audit-was-wrong: `services/sessionTranscript/` is a stub on all three)**

- CCB: 6-line stub (`writeSessionTranscriptSegment` + `flushOnDateChange`, both no-op).
- Gitlawb: no file.
- Ours: 1-line stub.

§10 audit row says ✅ all three. **In spirit the row is correct — JSONL persistence works** — but not because of this file. The actual persistent transcript writes happen in `utils/sessionStorage.ts` (5106 lines per inventory), not `services/sessionTranscript/`. Clarify the row's "Location / Notes" column: `utils/sessionStorage.ts` is the real path; `services/sessionTranscript/` is a stub on all three forks. (Upstream may have moved this into a dedicated service that none of the three forks ported.)

### 17. Session restore / resume
**(all three ✅ — byte-identical)**

`utils/sessionRestore.ts` = 551 (CCB) / 551 (Gitlawb) / 553 (ours). Two-line drift, trivial.

### 18. Session title / URL
**(all three ✅)** Shipped upstream, no fork drift detected.

### 19. Session ingress auth
**(audit-was-wrong: ours is identical to CCB + Gitlawb)**

`utils/sessionIngressAuth.ts` = **140 lines, identical across all three forks.** §10 row says `— ✅ ⚠️` (CCB/Gitlawb/ours). **All three should be ✅.**

### 20. Conversation recovery (mid-stream failure)
**(audit-was-wrong: ours has it — and Gitlawb has two additions we should adopt)**

- **CCB:** 600 lines.
- **Gitlawb:** 663 lines (+63 over CCB).
- **Ours:** 617 lines (+17 over CCB, but distinctly different +17 than Gitlawb's +63).

§10 audit row says `— ✅ ❌` (CCB/Gitlawb/ours). **Ours should be ✅.** We have the feature. False negative.

Comparing diffs:

**Gitlawb's additions over baseline (both missing from ours):**

1. **`ResumeTranscriptTooLargeError` + 8 MiB hard cap.** Resume fails fast with a specific error type if the reconstructed transcript exceeds 8 MiB. Prevents the multi-GB resume-bomb failure mode. ~30 lines.
2. **`stripThinkingBlocks` during 3P-provider resume.** When resuming against a non-first-party provider (not `firstParty`/`bedrock`/`vertex`/`foundry`), strip `thinking` and `redacted_thinking` blocks from assistant messages. Fixes issue #248 — Anthropic-specific thinking blocks cause 400s or context corruption when replayed against OpenAI-compat providers. ~20 lines.

**Our additions over baseline (both missing from Gitlawb):**

- **Malformed text block sanitization** — defensive `typeof block.text !== 'string'` check during resume, replaces corrupt content with empty string instead of crashing downstream. Useful when JSONL files are corrupted by disk issues or concurrent writes.

Not symmetric additions. Two wins from Gitlawb for us; one win from us for Gitlawb.

**Adapt recommendation:** both. Tier 1 / Tier 2.
- 8 MiB cap: ~30 min, Tier 1.
- `stripThinkingBlocks` 3P guard: ~1 hour (+ testing), Tier 2 — matters specifically when someone resumes against NIM bridge / OpenRouter / Ollama.

### 21. Cross-project resume
**(all three ✅ — byte-identical)**

`utils/crossProjectResume.ts` = **75 lines, identical across all three.** No drift.

---

## Audit row corrections to apply to `fork-parity-audit.md` §10

After the source-level re-verification, these rows need status flips:

| Row | Old classification | Corrected classification |
|---|---|---|
| **Cached MicroCompact** | `— ✅ ✅` | `✅ ❌ ⚠️` — only CCB ships real impl; Gitlawb + ours are stubs (types wired, logic no-op). |
| **Context Collapse** | `⚠️ ✅ ✅` | `⚠️ ⚠️ ⚠️` — all three ship stubs; overflow recovery in ours is via reactiveCompact + forced auto-compact, not contextCollapse/. |
| **Session transcript (JSONL)** | `✅ ✅ ✅` via "—" notes | `✅ ✅ ✅` but update Location to `utils/sessionStorage.ts`. The `services/sessionTranscript/` file specifically is a stub on all three forks. |
| **Session ingress auth** | `— ✅ ⚠️` | `✅ ✅ ✅` — identical 140-line file on all three. |
| **Conversation recovery** | `— ✅ ❌` | `✅ ✅ ✅` with note: Gitlawb adds 8 MiB cap + 3P-provider thinking-block stripping; ours adds malformed-block sanitization. |

---

## Adapt backlog — concrete porting targets

Ranked by value × effort. Tier 1 = high-value, low-effort, do next. Tier 2 = high-value, moderate-effort. Tier 3 = covered by main-audit backlog.

### Tier 1 — do next

1. **MCP tool compaction** — add `isCompactableTool()` helper to `microCompact.ts` that treats `mcp__*` prefix as compactable. **~15 minutes.** Unlocks microcompaction for the 200+ MCP tools users get from Ghidra + Zendriver + Computer Use. Big win given Ghidra decompile outputs + zendriver base64 screenshots.

2. **autoCompact universal floor** — add Gitlawb's floor clamp inside `getEffectiveContextWindowSize()` as a universal safety net for small-context providers (on top of our existing `lowContextMode` DeepSeek path). **~15 minutes.** Prevents #635-style negative-threshold loops on any unknown 3P provider, not just DeepSeek.

3. **8 MiB resume transcript cap** — add `ResumeTranscriptTooLargeError` + `assertResumeMessageSize()` to `conversationRecovery.ts`. **~30 minutes.** Fails fast before REPL boot if a corrupted session would load multiple GB of messages.

### Tier 2 — plan for later

4. **`stripThinkingBlocks` 3P-provider resume guard** — strip `thinking`/`redacted_thinking` blocks from assistant messages during resume when `getAPIProvider()` isn't first-party/bedrock/vertex/foundry. **~1 hour.** Guards against 400s when resuming on NIM bridge / OpenRouter / Ollama / future OpenAI-compat providers. Not blocking for our DeepSeek-via-Anthropic-endpoint users today, but becomes relevant any time we expand NIM bridge coverage.

5. **Real cachedMicrocompact** — port CCB's 112-line implementation. `CLAUDE_CACHED_MICROCOMPACT=1` env gate, Claude 4.x regex, `delete_tool_result` edit builder, wire into our existing pending-cache-edits slot in `microCompact.ts`. **~2–3 hours.** Valuable for first-party Anthropic / Claude.ai subscription users with long sessions and lots of tool use — direct prompt-cache token savings.

### Tier 3 — already tracked in main audit backlog

6. **`compressToolHistory.ts`** — size-based tier compression for small-context OpenAI-compat providers. 255 lines. Complements microCompact (time/cache-based) with a size-based pass at the API shim layer. Already `#21 small-context tool_result compression` in main audit backlog §22.

### Don't adopt

- **CCB cachedMCConfig.ts (3 lines)** — trivial stub, no real code.
- **CCB `snipCompact.ts` stub structure** — our 104-line impl supersedes.
- **Gitlawb's raw-context-window percentage display tweak** — cosmetic, our threshold-relative display is arguably more informative (shows distance to the compact trigger, which is what users actually care about).

---

## Key takeaways

- **We're materially ahead on overflow recovery** (reactiveCompact 316 lines + forced auto-compact) — but the main audit row wrongly credited Gitlawb with a full Context Collapse impl. All three have 7–82-line stubs in `contextCollapse/`; ours compensates via reactiveCompact.
- **We're materially ahead on memory infrastructure** — memdirGit / memdirWrite / memoryExportImport / teamMemorySync GitHub backend are real and unique.
- **Gitlawb is ahead in two narrow, fixable places**: MCP tool compaction in microCompact (15 min) and resume safety additions in conversationRecovery (8 MiB cap + thinking-block stripping).
- **CCB is ahead in exactly one place that matters**: real cachedMicrocompact for Claude 4.x prompt-cache cleanup.
- **Three audit-row corrections to apply** — §10 had two outright wrong cells (Gitlawb Context Collapse, ours Conversation recovery) and two partial errors (Cached MicroCompact classification, Session ingress auth).

Total adapt-surface: ~4 hours of Tier 1 work, ~4 hours of Tier 2. Closes every real gap in §10 except compressToolHistory (already in main audit backlog).
