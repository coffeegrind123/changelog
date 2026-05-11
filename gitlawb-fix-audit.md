# Gitlawb Fix Audit — openclaude gap catalog

Systematic audit of all 587 commits from [Gitlawb/openclaude](https://github.com/Gitlawb/openclaude) main branch, comparing each fix against openclaude source at `/home/openclaudeuser/openclaude/src/`.

**Audit date:** 2026-05-11
**Session type:** Research & documentation only — no openclaude source edits
**OC branch for implementation:** `gitlawb-fix-port`
**Total GAPs found:** ~93 across 8 batches

---

## Audit Progress

| Batch | Commit range | Status | GAPs | ALREADY_HAVE | NOT_APPLICABLE |
|-------|-------------|--------|------|-------------|----------------|
| 1 | 2-73 | [x] | 7 | 2 | 64 |
| 2 | 74-146 | [x] | 8 | 5 | 60 |
| 3 | 147-219 | [x] | 12 | 3 | 58 |
| 4 | 220-292 | [x] | 13 | 2 | 58 |
| 5 | 293-365 | [x] | 8 | 11 | 52 |
| 6 | 366-438 | [x] | 10 | 7 | 56 |
| 7 | 439-511 | [x] | 14 | 2 | 57 |
| 8 | 512-587 | [x] | 21 | 3 | 50 |

---

## Priority Summary

| Priority | Count | Criteria |
|----------|-------|----------|
| CRITICAL | 13 | Memory leaks, crashes, API 400 errors, security, broken core features |
| HIGH | 20 | Missing guards/params, feature gaps, unbounded growth, architectural divergence |
| MEDIUM | 29 | Correctness fixes, optimizations, UX improvements |
| LOW | 31 | Minor polish, model name updates, cosmetic fixes |

---

## CRITICAL GAPs

| # | SHA | B | Subject | OC File(s) | What to fix |
|---|-----|---|---------|------------|-------------|
| 1 | 942d09c | 3 | SessionRunner env leak: child processes inherit full `process.env` | `src/bridge/sessionRunner.ts` | Add `CHILD_ENV_ALLOWLIST` + `buildChildEnv()` to filter env vars passed to spawned child processes |
| 2 | 942d09c | 3 | buildSdkUrl SSRF: `includes('localhost')` bypassable via URL path | `src/bridge/workSecret.ts:43`, `bridgeMain.ts:2196,2858`, `product.ts:32` | Replace `apiBaseUrl.includes('localhost')` with `new URL(apiBaseUrl).hostname === 'localhost'` |
| 3 | 942d09c | 3 | CA cert validation: no PEM validation before writing to system CA bundle | `src/upstreamproxy/upstreamproxy.ts` | Add `isValidPemContent()` with `-----BEGIN CERTIFICATE-----` regex guard before `writeFile` |
| 4 | 942d09c | 3 | memoryScan unbounded depth: no MAX_DEPTH on recursive readdir | `src/memdir/memoryScan.ts` | Add `MAX_DEPTH=3` guard before `readdir({recursive:true})` |
| 5 | aab4890 | 7 | `dangerouslyDisableSandbox` exposed to model in BashTool schema | `src/tools/BashTool/BashTool.tsx:310,322-327` | Remove from model-facing `inputSchema`; keep internal-only; remove from Bash prompt |
| 6 | 7002cb3 | 7 | Sandbox auto-allow bypasses Bash path constraints | `src/tools/BashTool/bashPermissions.ts:2022` | Change `!== 'passthrough'` to `=== 'deny' || === 'ask'` so sandbox 'allow' still runs Bash path validation |
| 7 | ae3b723 | 7 | Sandbox `enabled` setting read from projectSettings — malicious repo can disable sandbox | `src/utils/sandbox/sandbox-adapter.ts:476-483` | Limit sandbox config reads to trusted sources only (user/local/flag/policy), not `projectSettings` |
| 8 | 739b8d1 | 7 | MCP OAuth callback processes errors before state validation (CSRF) | `src/services/mcp/auth.ts:1129-1141` | Check `state` parameter first; only process `error` when state matches |
| 9 | ae3b723 | 7 | MCP tool results not Unicode-sanitized — injection via malicious MCP servers | `src/services/mcp/client.ts` | Add `recursivelySanitizeUnicode()` to MCP tool result processing |
| 10 | ae3b723 | 7 | WebFetch SSRF protection missing — DNS rebinding to internal/metadata endpoints | `src/tools/WebFetchTool/` | Add `ssrfGuardedLookup` or equivalent SSRF guards to WebFetch HTTP requests |
| 11 | ebc9c70 | 8 | Nested heredoc bypass in `stripSafeHeredocSubstitutions` | `src/tools/BashTool/bashSecurity.ts:573` | Add nested-heredoc rejection guard (same as `isSafeHeredoc` already has); nested inner range leaves outer.end stale, silently dropping trailing content from validators |
| 12 | 9fed6ae | 8 | Zero path-escape/symlink validation on plugin components | `src/utils/plugins/pluginLoader.ts`, `validatePlugin.ts` | Add `resolveExistingPluginComponentPath()` with symlink-escape + `..`-traversal protection |
| 13 | 0951c8b | 5 | Dangerous path check skipped in acceptEdits mode for rm/rmdir | `src/tools/BashTool/modeValidation.ts:39-50` | Call `checkDangerousRemovalPaths` before returning `{behavior:'allow'}` for rm/rmdir in acceptEdits |

---

## HIGH Priority GAPs

| # | SHA | B | Subject | OC File(s) | What to fix |
|---|-----|---|---------|------------|-------------|
| 14 | 2c6ec01 | 4 | Keyboard freeze when MCP notification effects fire — missing `supportsMicrotasks` in React 19 reconciler | `src/ink/reconciler.ts:410` | Add `supportsMicrotasks: true, scheduleMicrotask: queueMicrotask`; add try/catch in `notifications.tsx` |
| 15 | c1e5e36 | 4 | Keyboard freeze via stale selector refs in useSyncExternalStore | `src/state/AppState.tsx` | Add `selectorRef`/`storeRef` pattern via `useRef` + `useCallback(fn, [])` in `useAppState()` |
| 16 | f3a984d | 4 | Null shell output crashes BashTool | `src/tools/BashTool/BashTool.tsx:578`, PowerShellTool | Normalize `typeof stdout/stderr === 'string' ? stdout : ''` before calling string methods |
| 17 | b0d796e | 4 | Resume hardening after compaction failures | `src/screens/ResumeConversation.tsx`, `query.ts`, `main.tsx` | Strip `preservedSegment` on missing tail UUID; show `errorMessage(error)`; add error banner in ResumeConversation |
| 18 | 694c242 | 4 | Resume OOM from stale toolUseResult stdout in JSONL buffer | `src/utils/sessionStorage.ts` | Add `stripPersistedToolUseResultsFromJSONLBuffer()` buffer walker to remove persisted-output content before JSON.parse |
| 19 | d430ddd | 3 | ANTHROPIC_API_KEY leaks to 3P provider auth path | `src/utils/auth.ts:288` | Add `if (apiKeyEnv && !isUsing3PServices())` guard before returning key |
| 20 | d430ddd | 3 | Misleading x-api-key error message for 3P providers | `src/services/api/errors.ts:838,1188` | Add `getAPIProvider() === 'firstParty'` guard to x-api-key error handlers |
| 21 | 1278967 | 1 | Missing `!isUsing3PServices()` guard before CI credential throw | `src/utils/auth.ts:278-285,1746` | Add guard before throw; extend `isUsing3PServices()` to cover z.ai/DeepSeek/NIM |
| 22 | 36d1c45 | 4 | Quota-exhausted 429 errors not detected — spams retries | `src/services/api/withRetry.ts:836` | Add `isQuotaExhausted()` function checking for "limit: 0"/"exceeded your current quota"; skip retry |
| 23 | ffbc1f8 | 2 | CSI-u decodeModifier bug: modifier=0 produces m=-1 corrupting all modifier bits | `src/ink/parse-keypress.ts:494-506` | Use `Math.max(modifier, 1) - 1`; add `isPrivateUseCodepoint()` guard; extend `keycodeToName` for Unicode |
| 24 | 6c35f4e | 1,2 | `store.subscribe()` called without null guard in SandboxViolationExpandedView | `src/components/SandboxViolationExpandedView.tsx:34-41` | Add `if (!store || typeof store.subscribe !== 'function') return;` before subscribe call |
| 25 | 5c4fdca | 8 | Git 2.30+ refuses to start with control chars in env values — crashes all plugin git operations | `src/utils/plugins/` (no `gitEnv.ts`) | Add `sanitizeEnvForGit()` + `buildGitChildEnv()`; apply to all git invocations in marketplace/plugin loader |
| 26 | e438c89 | 8 | Hooks stdin.end async path blocks every plugin hook for 60s in interactive mode | `src/utils/hooks.ts:1479-1482` | Change to unconditionally `child.stdin.end()` after writing initial payload (already done in sync path at line 1275) |
| 27 | 208c896 | 8 | OAuth refresh attempts fire on third-party providers | `src/services/api/client.ts` | Add `authRouting.ts` with `shouldUseFirstPartyAnthropicAuth()` guard |
| 28 | 25ce2ca | 6 | Context overflow 500 error handler missing | `src/services/api/errors.ts` | Add keyword-based detection ('too many tokens', 'request too large', 'context length') and user-friendly recovery message |
| 29 | 25ce2ca | 6 | Auto-compact circuit breaker safety net missing | `src/query.ts` | Add pre-API-call check when auto-compact fails 3+ consecutive times; block with message instead of burning API call |
| 30 | 25ce2ca | 6 | SendMessage race condition: double-check task status before auto-resume | `src/tools/SendMessageTool/SendMessageTool.ts` | Add fresh status re-check after acquiring task reference |
| 31 | 25ce2ca | 6 | AgentTool cleanup: each call not individually try/catch'd | `src/tools/AgentTool/AgentTool.tsx` | Wrap `clearInvokedSkillsForAgent`, `clearDumpState` etc. each in its own try/catch |
| 32 | 6b2121d | 6 | Non-string saved model values crash `/models` and string methods | `src/utils/model/model.ts:67` | Add `typeof model !== 'string'` guard in `getUserSpecifiedModelSetting()` |
| 33 | a4c6757 | 7 | Shell CWD recovery uses `realpath()` which succeeds on files — ENOTDIR crashes all Bash | `src/utils/Shell.ts:252` | Replace `realpath()` with `stat().isDirectory()` for primary CWD check and fallbacks |

---

## MEDIUM Priority GAPs

| # | SHA | B | Subject | OC File(s) | What to fix |
|---|-----|---|---------|------------|-------------|
| 34 | eed77e6 | 6 | `truncate()` crashes when command description is undefined | `src/utils/truncate.ts:140` | Add early return for falsy values. ⚠️ **Also in CCB audit (#11, b8b48bf7)** — same file/line/fix |
| 35 | 3d1979f | 7 | `/help` tab crashes from undefined command descriptions (7 return paths) | `src/commands.ts:910-934` | Add `?? ''` on all 7 return paths in `formatDescriptionWithSource()` |
| 36 | 002a8f1 | 7 | MCP tool schema `required` array not synced after properties filtered → API 400 | `src/utils/api.ts:97-118` | Add `sanitizeSchemaRequired()` to sync `required` with filtered `properties` |
| 37 | 55c5f26 | 7 | Auto-compact % uses threshold as denominator — shows 16% when actual is 30% for DeepSeek | `src/services/compact/autoCompact.ts:127-129` | Use `getContextWindowForModel()` as denominator for display percentage |
| 38 | c6c5f06 | 7 | Error truncation limit 10KB too short for real-world errors | `src/utils/toolErrors.ts:15` | Bump from 10000 to 40000 chars |
| 39 | c6c5f06 | 7 | MCPTool null guards missing on abort paths | `src/tools/MCPTool/MCPTool.ts:70-76` | Null-guard `content` in `mapToolResultToToolResultBlockParam`; add AbortError re-throw |
| 40 | 310f1d3 | 2 | No session title fallback for non-Anthropic providers — tab stays blank | `src/utils/sessionTitle.ts:135-141` | Add `localFallbackTitle()` in catch block returning sentence-cased local fallback |
| 41 | d156aed | 2 | No bracket balancer for truncated tool JSON in streamTranslator | `src/services/api/openaiBridge/streamTranslator.ts:356-405` | Add bracket balancer trying 10 suffix combinations to close truncated tool-use JSON |
| 42 | 7a7437b | 3 | `migrateSonnet1mToSonnet45()` runs for 3P users | `src/migrations/migrateSonnet1mToSonnet45.ts:25` | Add `if (getAPIProvider() !== 'firstParty') return` at function top |
| 43 | 6c4225f | 3 | `assertMinVersion()` calls Anthropic GrowthBook for all providers | `src/utils/autoUpdater.ts:93` | Add `if (getAPIProvider() !== 'firstParty') return` after test-mode check |
| 44 | 1709f5c | 3 | `claude update` downloads Anthropic binary even for non-Anthropic builds | `src/cli/update.ts` | Block update with actionable message pointing to git pull + rebuild |
| 45 | 70cfa61 | 4 | `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` not set by default | `src/entrypoints/cli.tsx`, `mcp.ts` | Set `process.env.CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS ??= 'true'` |
| 46 | fb221ba | 4 | Classifier transcript growth: persisted-output tool results accumulate in state | `src/components/messages/UserToolResultMessage/UserToolSuccessMessage.tsx` | Add `fallbackContent` memo using `extractTag('persisted-output')` to compact large results |
| 47 | 01acc4c | 5 | No auto-allow for safe read-only commands in acceptEdits mode | `src/tools/BashTool/modeValidation.ts:38-51` | Add grep/cat/ls/find/head/tail/echo/pwd/wc/sort/uniq/diff with shell redirection detection |
| 48 | 284d9bd | 5 | Image dimension limit 2000→1568 prevents many-image API rejection | `src/constants/apiLimits.ts:42-43` | Change `IMAGE_MAX_WIDTH/HEIGHT` from 2000 to 1568 |
| 49 | daf2c90 | 5 | Duplicate marketplace plugins not deduplicated by name | `src/utils/plugins/pluginLoader.ts:3264` | Collapse duplicate marketplace plugins by name; warn on dropped duplicate |
| 50 | 8ece290 | 5 | Startup dialogs steal focus when input buffered (e.g. `-p` mode) | `src/screens/REPL.tsx` (replInputSuppression) | Add `isPromptTypingSuppressionActive()` that also returns true when `inputValue.trim().length > 0` |
| 51 | 2caf2fd | 5 | Startup checks fire before first message — CLI appears frozen | `src/screens/REPL.tsx:849` | Defer `performStartupChecks` until after first message submission (`submitCount > 0`) |
| 52 | 25ce2ca | 6 | Continuation nudge: model says "so now I have to do it" without tool calls → premature completion | `src/query.ts` | Add regex-based continuation signal detection with `MAX_CONTINUATION_NUDGES` cap (3) |
| 53 | 08cc6f3 | 6 | `addLineNumbers()` uses `\t` separator ambiguous for tab-indented files | `src/utils/file.ts:306` | Switch from `\t` to `→` arrow separator (parse side already handles both) |
| 54 | b280c74 | 6 | Forward PATH and CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST to teammates | `src/utils/swarm/spawnUtils.ts:96` | Add `PATH` and `CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST` to `TEAMMATE_ENV_VARS` |
| 55 | 5c4469f | 3 | Tool result replacements not synced to live REPL transcript | `src/Tool.ts`, `src/query.ts:443`, `src/screens/REPL.tsx` | Add `syncToolResultReplacements` to `ToolUseContext`; push replacements to REPL |
| 56 | 7f96920 | 3 | Graceful shutdown: cleanupTerminalModes skipUnmount + 20ms tick + REPL guard | `src/utils/gracefulShutdown.ts:59,436,458` + `REPL.tsx` | Add `skipUnmount` param; add 20ms await before failsafe; add `!isShuttingDown()` guard |
| 57 | c66b859 | 3 | `getCustomOffSwitchMessage()` missing — returns "Opus is experiencing high load" for all providers | `src/services/api/errors.ts:173` | Add `getCustomOffSwitchMessage()` returning provider-neutral message for 3P |
| 58 | 5b20fe7 | 3 | CostThresholdDialog hardcodes "Anthropic API" title | `src/components/CostThresholdDialog.tsx:41` | Use `getAPIProvider()` to show correct provider label |
| 59 | 5943c5c | 8 | PromptInput `!` leak — typing `!` into empty input leaves literal `!` in buffer | `src/components/PromptInput/PromptInput.tsx:886-899` | Consolidate single-char and multi-char paste paths through `detectModeEntry()` helper |
| 60 | fc89767 | 8 | Agent whenToUse coercion: `formatAgentAsMarkdown` calls `.replace()` on non-string values | `src/components/agents/agentFileUtils.ts:34` | Add `typeof whenToUse === 'string' ? : ''` guard |
| 61 | 6af709e | 8 | AgentTool subagent instructions insufficient — model continues generating after agent launch | `src/tools/AgentTool/AgentTool.tsx` | Strengthen instructions: "You may continue first ONLY if you have other tasks on clearly different files" |
| 62 | feb5791 | 8 | Effort xhigh not persisted; reasoning_effort not emitted in openaiBridge | `src/utils/effort.ts`, `src/services/api/openaiBridge/requestTranslator.ts` | Normalize `xhigh` → `max` for persistence; emit `reasoning_effort` in requestTranslator |

---

## LOW Priority GAPs

| # | SHA | B | Subject | OC File(s) | What to fix |
|---|-----|---|---------|------------|-------------|
| 63 | c957d49 | 1 | `collectRemovedRects()` crashes when `removed` is null/undefined in Ink DOM | `src/ink/dom.ts:230` | Add null-check on `removed` param; use `?.` for `elem.style?.position` |
| 64 | cb24750 | 1 | `modifiers-napi` supply-chain risk — live `require()` calls | `src/utils/modifiers.ts:17,34` | Replace `require('modifiers-napi')` with no-ops (prewarmModifiers no-op, isModifierPressed false) |
| 65 | 99543a2 | 1 | Double-slash import path `'src//types/message.js'` | `src/cli/structuredIO.ts:7` | Remove double-slash → `'src/types/message.js'` |
| 66 | 409e90c | 1,2 | wss:// default port should be 443 in NO_PROXY matching | `src/utils/proxy.ts:100` | Add `url.protocol === 'wss:'` to 443 branch of port resolution |
| 67 | c8a780a | 1 | 9 unsafe `as DOMElement` casts without type guards in Ink render-node-to-output | `src/ink/render-node-to-output.ts` (9 sites) | Add `isElementNode()` helper; guard all `as DOMElement` casts |
| 68 | 2bade92 | 2 | Missing RipgrepUnavailableError + platform install hints | `src/utils/ripgrep.ts` | Add error class with winget/brew/apt install guidance |
| 69 | 4918caa | 2 | Resume hint says `claude --resume` not `openclaude --resume` | `src/utils/gracefulShutdown.ts:187` | Replace string |
| 70 | 1d82022/e8dd3d6 | 2 | Missing getSkillListLabel + namespace sort in skills menu | `src/components/skills/SkillsMenu.tsx` | Add `getSkillListLabel()` for namespace:leaf-name display; sort by `a.name.localeCompare` |
| 71 | 84ac06b | 3 | Status screen shows raw MACRO.VERSION instead of DISPLAY_VERSION | `src/components/Settings/Status.tsx:25` | Use `MACRO.DISPLAY_VERSION ?? MACRO.VERSION` |
| 72 | 6f4aa02 | 3 | Tab header highlight not refreshed on horizontal nav | `src/components/design-system/Tabs.tsx` | Add `key={selectedTabIndex-${headerFocused}}` to header Box wrapper |
| 73 | 8501786 | 4 | Provider-aware rate limit reset delay | `src/services/api/withRetry.ts:883` | Add `parseOpenAIDuration()` + provider-aware delay in `getRateLimitResetDelayMs` |
| 74 | f5b20fc | 4 | Linux clipboard JPEG/GIF/WebP support + `__stub` detection in imageProcessor | `src/utils/imagePaste.ts`, `imageProcessor.ts` | Add `LINUX_CLIPBOARD_IMAGE_MIME_TYPES` constant + `buildLinuxClipboardCheckCommand()` |
| 75 | aa69e85 | 4 | Prompt identity still says "Claude Code, Anthropic's official CLI" | `src/constants/system.ts:10`, prompts.ts, agents | Replace 5 identity strings with fork-appropriate branding |
| 76 | 4a4394b/7b68eb1 | 4 | Local provider URL validation missing private IP ranges | `src/services/api/providerConfig.ts` | Add private IPv4/IPv6 ranges, .local hostnames, 0.0.0.0 to `isLocalProviderUrl()` |
| 77 | 19c00e6 | 4 | Flicker-free mode not toggleable via /config | `src/utils/fullscreen.ts`, config types | Add `flickerFreeMode` field to GlobalConfig + `/config` toggle |
| 78 | 7c0ea68 | 4 | `extractGitHubRepoSlug` vulnerable to URL spoofing | `src/commands/install-github-app/repoSlug.ts` | Rewrite with domain-anchored regex extraction |
| 79 | 72c6e97 | 4 | Ask-user-question footer actions not routed through useInput hook | QuestionView.tsx | Route footer actions through `useInput` hook to prevent keyboard freeze |
| 80 | c52245f | 4 | Image paste and image tool-result handling fixes | multiple files | Review diff and apply targeted image handling fixes |
| 81 | f9ce81b | 5 | Missing actionable SkillTool error message for missing `skill` parameter | `src/tools/SkillTool/` | Add `getSchemaValidationErrorOverride()` for "Missing skill name" message |
| 82 | 4ac7367 | 5 | Retry-after header not extracted from 429 error messages | `src/services/api/errors.ts` | Extract `retry-after` header; include timing guidance in error message |
| 83 | 25ce2ca | 6 | MCP URL elicitation retry doesn't check abort signal before each attempt | `src/services/mcp/client.ts` | Add `signal.aborted` guard at top of each retry loop iteration |
| 84 | 13e9f22 | 7 | API key masking in TextInput — no `mask` prop | `src/components/TextInput.tsx` | Add `mask='*'` prop + `maskTextWithVisibleEdges()` utility |
| 85 | 28de94d | 7 | `OPENCLAUDE_DISABLE_TOOL_REMINDERS` env var not supported | multiple files | Add env var to suppress hidden tool-output reminder messages |
| 86 | b0d9fe7 | 7 | Provider loading: env vars should take precedence over stored profiles | `src/utils/providerProfile.ts` | If persisting provider profiles, ensure env var precedence |
| 87 | e1e277a | 8 | Unicode glyphs U+23F5/U+23BF render as tofu boxes on Linux | 5 component files | Replace U+23F5→U+25B6, U+23BF→U+2514 in AgentProgressLine, MessageResponse, etc. |
| 88 | 6ea3eb6 | 8 | Request body not deterministically serialized — breaks OpenAI prefix caching | `src/services/api/openaiBridge/requestTranslator.ts` | Add `stableStringify` with sorted object keys at every depth |
| 89 | 4fab8b9 | 8 | 404 error message hardcodes Ollama hint regardless of actual host | `src/services/api/errors.ts` | Plumb request URL through `classifyOpenAIHttpFailure` for host-aware messages |
| 90 | 7711dda | 8 | Git stderr swallowed on worktree rev-parse failure | `src/utils/worktree.ts` | Add `buildRevParseFailureMessage()` that includes stderr + HEAD hint |
| 91 | e66d6e2 | 8 | Plugin hook registration duplicates not deduped at registration level | `src/bootstrap/state.ts:1524` | Add dedup before `push(...matchers)` in `registerHookCallbacks()` |
| 92 | d321c8f | 8 | Windows PasswordVault reads on by default; model cache key lacks env isolation | `src/utils/secureStorage/`, `modelSupportOverrides.ts` | Add `OPENCLAUDE_ENABLE_LEGACY_WINDOWS_PASSWORDVAULT` opt-in; include env values in cache key |
| 93 | 094f04c | 8 | Theme memo wrappers return stale closure captures | `src/components/design-system/ThemeProvider.tsx:123,148` | Remove `_c(3)`/`_c(4)` React Compiler memo wrappers from `useTheme()`/`usePreviewTheme()` |
| 94 | 35f86a9 | 8 | CLAUDE logo 'D' visually ambiguous with adjacent characters | `src/components/LogoV2/LogoV2.tsx` | Adjust letter spacing / glyph for visual distinction |

---

## ALREADY_HAVE

| # | SHA | B | Subject | Why we already have it |
|---|-----|---|---------|------------------------|
| 1 | 63adb95 | 2 | Nested skill directories | `buildNamespace()` + `getSkillCommandName()` + recursive `findSkillMarkdownFiles()` at `loadSkillsDir.ts:545-573` |
| 2 | 39d9616 | 2 | DeepSeek context window 64k→128k | `getContextWindowForModel()` at `context.ts:156,259,262` already has 128_000 |
| 3 | 598f59e | 2 | tool_choice 'none' mapping | `openaiBridge/requestTranslator.ts:345-346` already maps it |
| 4 | 217a864 | 2 | Commit co-author attribution disabling | `isUndercover()` + `settings.includeCoAuthoredBy` at `attribution.ts:52-98` |
| 5 | 0746802 | 2 | GrowthBook phone-home kill | All analytics stubbed; `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` at entrypoint |
| 6 | 6aec841 | 3 | Recursive schema normalization | `sanitizeSchemaForOpenAICompat()` at `schemaSanitizer.ts:189` handles recursion into properties/items/anyOf/oneOf/allOf |
| 7 | 0c88dea | 3 | Strip JSON schema keywords | `OPENAI_INCOMPATIBLE_SCHEMA_KEYWORDS` set covers 19 keywords (more than Gitlawb's 3) |
| 8 | e494015 | 3 | Streaming reader try/finally | `streamTranslator.ts:586` already wraps reader in try/finally with `releaseLock()` |
| 9 | c1e5e36 | 4 | `updateContainerSync/flushSyncWork` in ink.tsx | Already at `ink.tsx:1495,1497` |
| 10 | c385047 | 6 | Auto-fix service | Ported from Gitlawb on 2026-04-25 (263 LOC + skill + notice + settings schema) |
| 11 | aeaa658 | 6 | Auto-compact floor guard | `getEffectiveContextWindowSize()` at `autoCompact.ts:59-61` already floors with auto-compact buffer |
| 12 | b280c74 | 6 | Git worktree mutation serialization | `withGitWorktreeMutationLock` at `worktree.ts:207` has proper promise-chained serialization |
| 13 | 25ce2ca | 6 | MCP tool timeout | `getMcpToolTimeoutMs()` at `client.ts:227` returns 10 min default |
| 14 | 25ce2ca | 6 | MCP tools/list retry | `fetchToolsForClient` at line 1814 has 1-attempt retry on transient failure |
| 15 | 31be66d | 6 | allowBypassPermissionsMode setting | Superseded by our fork's default `bypassPermissions` in `permissionSetup.ts` |
| 16 | b4bd95b | 5 | Normalize malformed Bash tool args from OpenAI | `toolArgumentNormalization.ts` has full normalization |
| 17 | 52d33a8 | 5 | MCP tool results in microcompact | `isCompactableTool()` at `microCompact.ts:60-61` has `mcp__` prefix check |
| 18 | 1e05702 | 5 | GLM-5 reasoning model hang | `streamTranslator.ts:518-525` handles `reasoning_content` and `reasoning` |
| 19 | ccaa193 | 5 | Preserve only originally-required properties in strict schemas | `schemaSanitizer.ts:231-234` filters `required[]` against actual properties |
| 20 | e438c89 | 8 | logForDebugging import (Bug 1) | `App.tsx:3` already imports it |
| 21 | dc3c065 | 8 | MCP .mcp.json approval for 3P | `interactiveHelpers.tsx:160` calls `handleMcpjsonServerApprovals(root)` directly — no Anthropic gate |
| 22 | c873725 | 8 | createRequire→static import | `AppStateStore.ts` doesn't use `createRequire` |
| 23 | a3e728a | 7 | Agent model provider-aware fallback | `getAgentModel` in `model.ts` already handles provider-aware resolution |
| 24 | 44a2c30 | 7 | Hook Chains runtime integration | Already ported from Gitlawb (1518 LOC + docs) |
| 25 | 6e58b81 | 7 | Update shows real package version | Our updater uses GitHub Releases API — different mechanism |

---

## Implementation Notes

The 94 GAPs are organized by priority tier above. Recommended fix order:

**First pass (security + crashes):** Items 1-13 (CRITICAL) — all security vulnerabilities and crash bugs. Each is independently fixable.

**Second pass (stability):** Items 14-33 (HIGH) — keyboard freezes, resume failures, provider-guard bugs, OOM issues.

**Third pass (robustness):** Items 34-62 (MEDIUM) — error handling, UX correctness, startup behavior.

**Fourth pass (polish):** Items 63-94 (LOW) — cosmetic, minor UX, command branding.

**Batch files:** `/tmp/gitlawb-gap-batch1.md` through `batch8.md` contain full per-commit detail.

---

## Cross-Reference: CCB Audit Overlap

Cross-referenced against `coffeegrind123/changelog:ccb-fix-audit.md` (66 GAPs across 648 CCB commits). Full CCB batch files at `/tmp/changelog-repo/ccb-gap-batch{1-8}.md`.

### Exact duplicate (same file, same line, same fix)

| Gitlawb # | CCB # | File | Bug |
|-----------|-------|------|-----|
| #34 (eed77e6) | #11 (b8b48bf7) | `src/utils/truncate.ts:140` | truncate() null/undefined crash — add early return guard |

### Related but different fix sites (both audits apply)

| Gitlawb # | CCB # | Relationship |
|-----------|-------|-------------|
| #35 (3d1979f) | #46 (562e9daa) | Same symptom (undefined command names crash UI) — Gitlawb fixes `formatDescriptionWithSource()` consumer, CCB fixes `getCommandName()` getter. Fix both. |
| #45 (70cfa61) | #1 (d136872c) | Same goal (prevent Anthropic headers on 3P APIs) — Gitlawb adds global env var `DISABLE_EXPERIMENTAL_BETAS`, CCB fixes specific function guards. Complementary. |

### Unique to Gitlawb audit (no CCB equivalent)

The remaining 87 GAPs in this audit have no CCB overlap. They cover Gitlawb-specific fix domains: bash security (nested heredoc, sandbox auto-allow, acceptEdits path guard), MCP security (OAuth CSRF, Unicode sanitization, SSRF), provider-guard gaps (auth.ts, model migration, update.ts, CostThreshold), and Bash/Shell fixes (stdout null normalization, ENOTDIR recovery, error truncation).
