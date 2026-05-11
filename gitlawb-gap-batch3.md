# Gitlawb Commits 147–219 Gap Analysis — Batch 3

**Date:** 2026-05-11  
**Range:** `4f78bde` → `2b5cf9f` (73 commits)  
**OpenCLaude base:** `/home/openclaudeuser/openclaude/src/`

---

## Security Fixes (HIGH PRIORITY)

### 942d09c | security: fix 5 findings from issue #42 | GAP (5 findings)

**Finding 1 [CRITICAL] — sessionRunner env leak:** Child processes inherit full `process.env` including `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, DB credentials.  
- OC_FILE: `src/bridge/sessionRunner.ts` (no `buildChildEnv()` function)
- Gitlawb adds `CHILD_ENV_ALLOWLIST` + `buildChildEnv()` with explicit allowlist of safe OS/runtime vars. Only `CLAUDE_CODE_*`, `PATH`, `HOME`, and standard OS vars are passed to child.

**Finding 3 [HIGH] — memoryScan unbounded directory walk:** No depth limit on `readdir({recursive:true})`.
- OC_FILE: `src/memdir/memoryScan.ts` (no `MAX_DEPTH` guard)
- Fix: Add `MAX_DEPTH=3`, filter entries by `f.split(sep).length - 1 < MAX_DEPTH` before the `MAX_MEMORY_FILES` cap.

**Finding 5 [HIGH] — buildSdkUrl SSRF via URL path:** Uses `apiBaseUrl.includes('localhost')` — a remote URL like `https://evil.com/localhost` would get `ws://` instead of `wss://`.
- OC_FILE: `src/bridge/workSecret.ts:43` — `apiBaseUrl.includes('localhost')`
- Also vulnerable: `src/bridge/bridgeMain.ts:2196,2858`, `src/constants/product.ts:32`
- Fix: Replace with `new URL(apiBaseUrl).hostname === 'localhost'`

**Finding 6 [HIGH] — CA cert validation:** No PEM validation before writing to system CA bundle. A compromised proxy sending HTML/JSON/scripts would be appended to the system CA.
- OC_FILE: `src/upstreamproxy/upstreamproxy.ts` (no `isValidPemContent()`)
- Fix: Add `isValidPemContent()` with `-----BEGIN CERTIFICATE-----...-----END CERTIFICATE-----` regex validation before `writeFile`.

**Finding 2 [HIGH] — ant gate:** Adds `isAntEmployee() -> false` constant, replaces direct `USER_TYPE === 'ant'` checks.  
- OC_FILE: `src/setup.ts:381,483` still uses raw `process.env.USER_TYPE === 'ant'`
- Note: Our codebase intentionally sets `USER_TYPE=ant` at entrypoint per CLAUDE.md, so this fix is less critical for us but still good hardening.

---

### d430ddd | fix: prevent ANTHROPIC_API_KEY interfering with Gemini auth | GAP

**auth.ts guard:** `getAnthropicApiKeyWithSource()` returns `ANTHROPIC_API_KEY` without checking `isUsing3PServices()`.
- OC_FILE: `src/utils/auth.ts:288` — `if (apiKeyEnv)` returns the key without provider check
- Fix: Change to `if (apiKeyEnv && !isUsing3PServices())`

**errors.ts guard:** x-api-key error handler fires for any provider, showing misleading "Invalid API key" to 3P users.
- OC_FILE: `src/services/api/errors.ts:838` — `error.message.toLowerCase().includes('x-api-key')` (no provider guard)
- Also: `src/services/api/errors.ts:1188` — same pattern in `getErrorTypeFromMessage()`
- Fix: Add `getAPIProvider() === 'firstParty'` guard to both sites

---

## Provider Guard Fixes (MEDIUM PRIORITY)

### 7a7437b | fix: skip Anthropic model migration for 3P | GAP

`migrateSonnet1mToSonnet45()` rewrites model to Anthropic-specific alias even for 3P users.
- OC_FILE: `src/migrations/migrateSonnet1mToSonnet45.ts:25` — no provider guard
- Fix: Add `if (getAPIProvider() !== 'firstParty') return` at function top

### 6c4225f | fix: skip assertMinVersion for 3P | GAP

`assertMinVersion()` calls Anthropic GrowthBook even for 3P providers. Currently safe because `isAnalyticsDisabled()` returns true for 3P, but the safety is fragile.
- OC_FILE: `src/utils/autoUpdater.ts:93` — no provider guard
- Fix: Add `if (getAPIProvider() !== 'firstParty') return` after the test-mode check

### 1709f5c | fix: block update command for 3P | GAP

`claude update` downloads from Anthropic GCS bucket, which would replace the OpenClaude build with upstream.
- OC_FILE: `src/cli/update.ts` — no `getAPIProvider() !== 'firstParty'` guard
- Fix: Block update with actionable message pointing to git pull + rebuild

---

## Provider-Aware UI/Services

### 5b20fe7 | fix: CostThresholdDialog provider-aware | GAP

Title hardcodes "Anthropic API" — misleading for z.ai/DeepSeek/NIM users.
- OC_FILE: `src/components/CostThresholdDialog.tsx:41` — `"You've spent $5 on the Anthropic API this session."`
- Fix: Use `getAPIProvider()` to show correct provider label

### c66b859 | fix: provider-aware error messages + skip key approval | GAP

**getCustomOffSwitchMessage():** Returns "Opus is experiencing high load" even for non-Anthropic providers.
- OC_FILE: `src/services/api/errors.ts:173` — still uses `CUSTOM_OFF_SWITCH_MESSAGE` directly (no `getCustomOffSwitchMessage()`)
- Fix: Add `getCustomOffSwitchMessage()` that returns provider-neutral message for 3P

**Onboarding.tsx:** Shows Anthropic key approval UI even when 3P provider is active.
- OC_FILE: `src/components/Onboarding.tsx` — check for `!isAnthropicAuthEnabled()` needed

### 84ac06b | fix: show display version in status | GAP (minor)

Status screen shows raw MACRO.VERSION instead of user-friendly DISPLAY_VERSION.
- OC_FILE: `src/components/Settings/Status.tsx:25` — `value: MACRO.VERSION`
- Fix: Change to `MACRO.DISPLAY_VERSION ?? MACRO.VERSION`

---

## Memory / REPL Fixes

### 5c4469f | fix: trim persisted tool results and sanitize MCP schemas | GAP

**syncToolResultReplacements:** When tool results are trimmed for token budget, the live REPL transcript retains the full untrimmed content in heap. No mechanism to push replacements back to the UI.
- OC_FILE: `src/Tool.ts` — no `syncToolResultReplacements` on `ToolUseContext`
- OC_FILE: `src/query.ts:443` — `applyToolResultBudget()` returns messages directly, not a `{messages, newlyReplaced}` result
- OC_FILE: `src/screens/REPL.tsx` — no sync callback, no initial replacement hydration
- Also spins off `src/services/api/openaiSchemaSanitizer.ts` (216 LOC) for MCP schema sanitization — OC has this already via `src/utils/schemaSanitizer.ts`

### 7f96920 | fix: graceful shutdown improvements | GAP

**cleanupTerminalModes skipUnmount:** Prevents double-unmount causing cursor/terminal corruption on exit.
- OC_FILE: `src/utils/gracefulShutdown.ts:59` — function signature is `cleanupTerminalModes(): void` (no `skipUnmount` param)
- OC_FILE: `src/utils/gracefulShutdown.ts:458` — calls `cleanupTerminalModes()` instead of `cleanupTerminalModes(true)` in the async path

**20ms tick before failsafe:** Gives React one event-loop tick to flush pending UI updates (e.g., hide autocomplete on `/exit`).
- OC_FILE: `src/utils/gracefulShutdown.ts:436` — no `await new Promise(r => setTimeout(r, 20))` before failsafe

**!isShuttingDown() in REPL:** Hides prompt input footer during shutdown to prevent lingering UI artifacts.
- OC_FILE: `src/screens/REPL.tsx` — no `!isShuttingDown()` guard in the prompt-input render condition

### 6f4aa02 | fix: refresh tab highlight on horizontal nav | GAP (minor)

Tab header box doesn't have a `key` prop that changes on selection, so React may not re-render the highlight.
- OC_FILE: `src/components/design-system/Tabs.tsx` — header `<Box>` wrapper missing `key={selectedTabIndex-${headerFocused}}`

---

## ALREADY_HAVE / NOT_APPLICABLE

| SHA | Subject | Verdict | Notes |
|-----|---------|---------|-------|
| 6aec841 | recursive schema normalization | ALREADY_HAVE | `sanitizeSchemaForOpenAICompat()` in `src/utils/schemaSanitizer.ts:189` already handles recursion into properties, items, anyOf/oneOf/allOf, and required filtering with keyword stripping |
| 0c88dea | strip JSON schema keywords | ALREADY_HAVE | Our `OPENAI_INCOMPATIBLE_SCHEMA_KEYWORDS` set covers 19 keywords (including format, $schema) — more comprehensive than Gitlawb's 3 |
| e494015 | streaming reader try/finally | ALREADY_HAVE | `src/services/api/openaiBridge/streamTranslator.ts:586` already wraps reader in try/finally with `reader.releaseLock()` |
| f385740 | isEnvTruthy for context window | NOT_APPLICABLE | Our `context.ts` uses `isNvidiaNimProviderForModel()` / `getAPIProvider()` for provider detection, not raw `=== '1'`/`=== 'true'` env checks |
| b65921e | Llama context windows + prefix sort | NOT_APPLICABLE | No `src/utils/model/openaiContextWindows.ts` in our codebase — we use NIM catalog + model capabilities instead |
| f4818dc | shim reliability overhaul | NOT_APPLICABLE | Fixes are in `openaiShim.ts` + `codexShim.ts` which we don't use — our `openaiBridge/` has different architecture |
| 4f78bde | delete hello/world | NOT_APPLICABLE | Cleanup |
| 3ca6c29 | pin GitHub Actions SHA | NOT_APPLICABLE | CI config only |
| 3ef09f9 | ANDROID_INSTALL.md | NOT_APPLICABLE | Documentation |
| aac326f | setup documentation | NOT_APPLICABLE | Documentation |
| All merge commits (24x) | merges | NOT_APPLICABLE | Merge commits only |
| 08f0b60 | /provider setup wizard | NOT_APPLICABLE | Gitlawb-specific provider profiles feature |
| 64ba7fd | Atomic Chat URL handling | NOT_APPLICABLE | Gitlawb-specific scripts |
| 0a42839 | GitHub onboarding PR feedback | NOT_APPLICABLE | Gitlawb-specific GitHub OAuth |
| cec3629 | Codex web tools | NOT_APPLICABLE | Gitlawb-specific Codex integration |
| 23216ca / 8f50f17 | EffortPicker + model refactor | NOT_APPLICABLE | Gitlawb-specific OpenAI/Codex provider UI |
| 5c25ac4 | Codex usage to /status | NOT_APPLICABLE | Gitlawb-specific Codex feature |
| 43ba2cb/8e8671f/ff124dc/2b5cf9f | VS Code extension | NOT_APPLICABLE | IDE extension, not core runtime |
| 5baee3b/4c1ba35 | MCP servers guide (reverted) | NOT_APPLICABLE | Docs, reverted |
| ac4efae | Firecrawl WebSearch/WebFetch backend | NOT_APPLICABLE | Gitlawb-specific — we use MCP browser tools |
| 5ccda35/118b079/4d0886a | slash suggestion highlight | NOT_APPLICABLE | Minor UX — our code already handles isSelected with color/dimColor; Gitlawb adds `figures.pointer` visual marker |

---

## Summary

| Verdict | Count |
|---------|-------|
| **GAP** | 12 unique source changes across 10 commits |
| **ALREADY_HAVE** | 3 |
| **NOT_APPLICABLE** | 58 (merges, docs, CI, Gitlawb-specific) |

### Critical Gaps:
1. **SessionRunner env leak** — child processes inherit full process.env with API keys
2. **buildSdkUrl localhost detection** — SSRF bypass via path manipulation
3. **CA cert PEM validation** — non-PEM data accepted into system CA bundle
4. **memoryScan unbounded depth** — DoS via deep/symlinked directories

### Important Gaps:
5. ANTHROPIC_API_KEY leaks to Gemini/3P provider auth path
6. Misleading x-api-key error for 3P providers
7. Anthropic model migration runs for 3P providers
8. assertMinVersion calls Anthropic GrowthBook for 3P
9. `claude update` downloads Anthropic binary even for 3P builds
10. Tool result replacements not synced to live REPL transcript
11. Cost threshold dialog hardcodes "Anthropic API"
12. Provider-aware error messages missing
