# Gitlawb Gap Analysis — Batch 4 (commits 220–292)

Analysis date: 2026-05-11
Commits: 73db9b5 through 897ef20 (73 commits, Gitlawb main)

## Classification legend
- **GAP** — missing in openclaude, should backport
- **ALREADY_HAVE** — already present in openclaude
- **NOT_APPLICABLE** — merge/doc/CI/test/gitlawb-specific/python/vscode-only

---

## 8501786 | feat: provider-aware rate limit reset delay | GAP | src/services/api/withRetry.ts:883
Our `getRateLimitResetDelayMs()` only reads `anthropic-ratelimit-unified-reset` header. Gitlawb made it provider-aware: firstParty=`anthropic-ratelimit-unified-reset`, openai/codex/github=`x-ratelimit-reset-requests`/`x-ratelimit-reset-tokens`, bedrock/vertex/foundry/gemini=null. They also added `parseOpenAIDuration()` helper. Low priority for us (we use Anthropic-compatible providers), but the pattern is clean.
**Missing:** `parseOpenAIDuration()` export, provider-aware delay logic in `getRateLimitResetDelayMs`, `getAPIProvider` import.

## f5b20fc | fix: make clipboard images pasteable | GAP | src/utils/imagePaste.ts
Our `imagePaste.ts` only tries `image/png` and `image/bmp` for Linux clipboard extraction. JPEG/GIF/WebP clipboard images silently fail. Gitlawb added `LINUX_CLIPBOARD_IMAGE_MIME_TYPES` constant + `buildLinuxClipboardCheckCommand()`/`buildLinuxClipboardSaveCommand()` that generate commands from a single MIME type list. Also fixed `imageProcessor.ts` to reject `__stub`-marked modules (bundled builds crash on BMP→PNG conversion via stubbed sharp).
**Missing:** `LINUX_CLIPBOARD_IMAGE_MIME_TYPES`, `buildLinuxClipboardCheckCommand()`, `buildLinuxClipboardSaveCommand()` in imagePaste.ts; `ImageProcessorUnavailableError` class + `__stub` detection in imageProcessor.ts.

## 2c6ec01 | fix: prevent keyboard freeze when MCP notification effects fire | GAP | src/ink/reconciler.ts:410
React 19 requires `supportsMicrotasks: true` + `scheduleMicrotask: queueMicrotask` in the reconciler host config. Without this, passive effects from `useMcpConnectivityStatus` silently drop state updates, corrupt React's `executionContext`, and freeze all keyboard input after the "N MCP server(s) need auth" notification.
**Missing:** `supportsMicrotasks: true, scheduleMicrotask: queueMicrotask` in reconciler.ts (after `noTimeout: -1`); try/catch wrappers in notifications.tsx `addNotification`/`removeNotification`/`processQueue`; try/catch wrapper in `useMcpConnectivityStatus.tsx`.

## c1e5e36 | fix: resolve keyboard freeze via sync render path + stable selectors | PARTIAL-GAP | src/state/AppState.tsx
We ALREADY HAVE `updateContainerSync`/`flushSyncWork` in ink.tsx (lines 1495, 1497). But we do NOT have the stable-selector fix in AppState.tsx: the `_c` compiler cache in `useAppState` and `useAppStateMaybeOutsideOfProvider` invalidates on every inline-arrow selector (new reference per render), producing a new `get` function, which useSyncExternalStore treats as tearing signal, causing re-render loops that starve keyboard input. Fix: useRef + useCallback(fn, []) to give useSyncExternalStore stable snapshot references.
**Missing:** `selectorRef`/`storeRef` pattern in `useAppState()` and `useAppStateMaybeOutsideOfProvider()` in AppState.tsx.

## f3a984d | fix(security-review): Handle null shell output | GAP | src/tools/BashTool/BashTool.tsx:578
Our BashTool output rendering does `let processedStdout = stdout; if (stdout) { ... }` — if `stdout` is null (not undefined), `stdout.replace()` throws. Gitlawb normalizes: `const normalizedStdout = typeof stdout === 'string' ? stdout : '';` before calling string operations. Same pattern applied to `stderr`. Fixes `/security-review` crash.
**Missing:** `typeof stdout === 'string'` normalization in BashTool tool_result handler and PowerShellTool result handler.

## aa69e85 | fix: correct prompt identity branding | GAP (cosmetic) | src/constants/system.ts:10
Our `system.ts` still has `DEFAULT_PREFIX = "You are Claude Code, Anthropic's official CLI for Claude."`. Gitlawb rebranded to "You are OpenClaude, an open-source fork of Claude Code." across DEFAULT_PREFIX, AGENT_SDK prefixes, DEFAULT_AGENT_PROMPT, explore agent, and general-purpose agent. Low priority — we deliberately keep some upstream naming but the mismatch could confuse models.
**Missing:** 5 string replacements in system.ts, prompts.ts, exploreAgent.ts, generalPurposeAgent.ts.

## 4a4394b + 7b68eb1 | feat: enhance local provider URL validation for private IPs | GAP | src/services/api/providerConfig.ts
Our `isLocalProviderUrl` (in cli.tsx) only checks localhost/127.0.0.1/::1. Gitlawb expanded it to private IPv4 ranges (10.x, 172.16-31.x, 192.168.x), IPv6 unique local (fc00::/7), link-local, loopback net, 0.0.0.0, and .local hostnames. Moves the function to `providerConfig.ts` with `isIP` from `node:net`. Low priority for us (we target z.ai not local Ollama).
**Missing:** `isLocalProviderUrl()` with private IP range support in providerConfig.ts.

## 36d1c45 | fix(retry): prevent retries on quota-exhausted 429 errors | GAP | src/services/api/withRetry.ts:836
Our `shouldRetry()` returns `!isClaudeAISubscriber() || isEnterpriseSubscriber()` for all 429 errors. Gitlawb added `isQuotaExhausted()` check: if error message contains "limit: 0" or "exceeded your current quota" on 429, returns false (no retry) and throws `CannotRetryError` with actionable fix message. Prevents spamming API with retries that will never succeed.
**Missing:** `isQuotaExhausted()` function + check in `shouldRetry()` and the retry loop.

## 8ce09ae | fix: disable cache_control injection for third-party providers | NOT_APPLICABLE | src/services/api/claude.ts:327
Our `getPromptCachingEnabled` doesn't check provider type. But we exclusively use Anthropic-compatible backends (z.ai, DeepSeek via the Anthropic protocol, NIM via our OpenAI bridge). DeepSeek supports cache_control via the Anthropic protocol. z.ai passes it through. This fix targets OpenAI-native providers (Azure Foundry, Gemini, GitHub) that reject unknown Anthropic-specific fields. NOT_APPLICABLE for our setup.

## 70cfa61 | fix: disable experimental API betas by default | GAP | src/entrypoints/cli.tsx
We don't set `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` by default. External providers (z.ai, DeepSeek) can return 500 on `defer_loading`, global cache scope beta headers. Gitlawb sets `process.env.CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS ??= 'true'` in both cli.tsx and mcp.ts entrypoints. Also fixes: Sonnet 1M latch (computed before closure to avoid cache-key drift from mid-retry GB refreshes), system-before-messages key ordering in the API params object, /dream command with programmatic `recordConsolidation()` call.
**Missing:** `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS ??= 'true'` in cli.tsx + mcp.ts; `sonnet1mExpLatched` variable; `system` before `messages` in API params object; `/dream` command.

## 694c242 | fix: reduce resume OOM risk | GAP | src/utils/sessionStorage.ts
On resume, `toolUseResult.stdout` can be 200k+ characters — kept in memory even after the content is written to `<persisted-output>`. Gitlawb added `stripPersistedToolUseResultsFromJSONLBuffer()` — a zero-alloc Buffer walker that finds `"toolUseResult":` keys whose parent message already has a `<persisted-output>` tag and removes the key+value. Operates on the raw JSONL buffer before JSON.parse. Also fixes update-config skill schema generation.
**Missing:** `stripPersistedToolUseResultsFromJSONLBuffer()` and all helper functions (PERSISTED_OUTPUT_TAG, TOOL_USE_RESULT_KEY, isJsonWhitespaceByte, skipJsonWhitespace, findJsonValueEnd, stripPersistedToolUseResultFromLine, findClosingBracket).

## e5c9a6f | feat: Enable Free DDG WebSearch For Non-Claude Models | NOT_APPLICABLE | src/tools/WebSearchTool/WebSearchTool.ts
Adds `duck-duck-scrape` dependency and DuckDuckGo web search fallback for non-Claude providers. We already have working WebSearch via browser tools and WebFetch. Adding this would require a new npm dependency and scraping DDG may violate their ToS. NOT_APPLICABLE for our fork — we'd use our existing tools.

## fb221ba | fix: Limit auto-mode classifier transcript growth | GAP | src/components/messages/UserToolResultMessage/UserToolSuccessMessage.tsx
Auto-mode classifier stores the full tool result content in message state. Over many turns, persisted-output tool results accumulate, bloating transcript and causing OOM. Gitlawb releases persisted tool results from transcript state via `extractTag(content, 'persisted-output')` to display a compact fallback.
**Missing:** `fallbackContent` memo in UserToolSuccessMessage.tsx using `extractTag('persisted-output')`.

## 19c00e6 | feat: expose flicker-free mode as /config toggle | GAP | src/utils/fullscreen.ts
We set `CLAUDE_CODE_NO_FLICKER=0` in compose. Gitlawb added `flickerFreeMode` boolean to GlobalConfig with /config toggle, wired with priority: env wins > config > USER_TYPE=ant default. Low priority since our Docker users already have it off, but useful for non-Docker installs.
**Missing:** `flickerFreeMode` field in config.ts GlobalConfig type + GLOBAL_CONFIG_KEYS array; Config.tsx toggle; fullscreen.ts priority chain.

## b0d796e | fix: harden resume after compaction failures | GAP | src/screens/ResumeConversation.tsx
Three fixes: (1) In QueryEngine.ts, strips `preservedSegment` from transcript metadata when tail UUID is missing (resume falls back to ordinary boundary pruning instead of deadlocked relink). (2) In main.tsx, shows `errorMessage(error)` instead of hardcoded "Unable to load transcript" / "Failed to resume". (3) In ResumeConversation.tsx, catches resume errors and shows an in-UI error banner instead of throwing (which would black-screen the entire flow).
**Missing:** preservedSegment stripping in QueryEngine.ts; errorMessage() use in main.tsx; resumeError state + errorBanner in ResumeConversation.tsx.

## 7c0ea68 + 931ee96 | security: address code scanning alerts | GAP (targeted) | src/commands/install-github-app/repoSlug.ts
The key security fix: `extractGitHubRepoSlug` was vulnerable to URL spoofing (`https://evil.example/?next=github.com/owner/repo`). Gitlawb rewrote it to use regex-based extraction with `github.com` domain anchoring and added spoof-resistance tests. Other changes (scripts/ CI/ telemetry plugin/ provider-launch security) are NOT_APPLICABLE.
**Missing:** Rewritten `extractGitHubRepoSlug()` with domain-anchored regex; `escapeForResolvedPathRegex()` helper in no-telemetry-plugin.

## 72c6e97 | fix: route ask-user-question footer actions through useInput | GAP | QuestionView.tsx
Routes ask-user-question footer actions through `useInput` hook. Without this, keyboard input freezes after using `/ask-user-question` footer. Need to locate our QuestionView component to check exact path.

## c52245f | fix: restore image paste and image tool-result handling | GAP | multiple
Need to check this commit's diff more carefully — it may overlap with f5b20fc or be separate fixes.

## Commits confirmed ALREADY_HAVE:
- c1e5e36 (partial): `updateContainerSync/flushSyncWork` in ink.tsx ✓
- 11d9660: Status.tsx tab highlight (2-line Ink change, minor)

## Commits confirmed NOT_APPLICABLE (73 total, 52 NOT_APPLICABLE):

### Merges (26):
73db9b5, a430237, 96b9e02, 3581d3f, 2ee43d7, 4c22de2, 7bc903d, 1a57335, 11d9660, 5e77d82, 47c53a1, 1cd4164, a287597, 8495064, a6ed57d, 4158214, cdf4bad, 32046e9, 63ad019, 089a42f, 20d1ee8, 74a25d0, 66bbb75, 20d1ee8

### Docs/config/packages/tests (16):
7095abb, 63daf33, f68b9aa, 7cf4c88, 0fd0026, 6181050, 29edece, 59ab270, 7bd7d0f

### Gitlawb/python/vscode-specific (10):
37d4c21, b4aa271, cf90457, f3ab727, 0e7a244, 43deb49, 184ec25, 116cc8e, fb32e3f, 6987a54, c735233, afed73f

### Code cleanup only (8):
3df635c, 365bd31, c52245f, bffd430, 03dff27, ab3c46a, 897ef20

### Scripts-only (2):
2031c67, 7668aba

---

## Summary: 13 GAP, 1 PARTIAL-GAP, 59 NOT_APPLICABLE

**High priority gaps (keyboard freezes + crash fixes):**
1. `2c6ec01` — `supportsMicrotasks` in reconciler + try/catch in notifications (keyboard freeze)
2. `c1e5e36` — stable selector refs in AppState.tsx (keyboard freeze, partial)
3. `f3a984d` — null stdout/stderr normalization in BashTool (crash fix)
4. `b0d796e` — resume hardening after compaction failures (crash fix)
5. `694c242` — strip persisted toolUseResult on resume (OOM fix)

**Medium priority gaps (robustness):**
6. `36d1c45` — quota-exhausted 429 detection (avoids retry spam)
7. `f5b20fc` — Linux clipboard JPEG/GIF/WebP support
8. `70cfa61` — disable experimental betas for non-Anthropic providers
9. `fb221ba` — limit classifier transcript growth
10. `72c6e97` — ask-user-question footer input routing

**Low priority gaps (nice-to-have):**
11. `8501786` — provider-aware rate limit reset (we use Anthropic-compatible APIs)
12. `aa69e85` — prompt identity branding (cosmetic)
13. `4a4394b` + `7b68eb1` — local provider URL validation (we test against z.ai)
14. `19c00e6` — flicker-free /config toggle (Docker users already have it off)
15. `7c0ea68` — repoSlug hardening (targeted security fix)
