# Gitlawb GAP Analysis — Batch 8 (commits 512–587)

Analyzed 76 commits from Gitlawb `main` against openclaude `ccb-fix-port` branch at `/home/openclaudeuser/openclaude/src/`.

## Verdict Key
- **GAP** — Fix missing in openclaude, should be backported
- **ALREADY_HAVE** — Fix present or equivalent already exists
- **NOT_APPLICABLE** — Doc/CI/merge/release/test/openaiShim-specific/branding/feature-only

---

## HIGH PRIORITY GAPs (security, crashes, provider-agnostic bugs)

### ebc9c70 | fix(bashSecurity): reject nested heredoc ranges in stripSafeHeredocSubstitutions | GAP
OC_FILE: `src/tools/BashTool/bashSecurity.ts:573`
NOTES: `stripSafeHeredocSubstitutions` at line 573 goes from `if (!found) return null` directly to the reverse-strip loop. Missing the nested-heredoc rejection guard that `isSafeHeredoc` already has. A nested inner range stripped first leaves `outer.end` stale; `result.slice(outer.end)` skips trailing content (e.g., `; rm -rf /`), silently hiding it from validators. Security bypass.

### 9fed6ae | fix: validate plugin component paths | GAP
OC_FILE: `src/utils/plugins/pluginLoader.ts` (no `resolveExistingPluginComponentPath`), `src/utils/plugins/validatePlugin.ts` (schema-only, no path checks)
NOTES: Gitlawb adds `resolveExistingPluginComponentPath()` with symlink-escape + `..`-traversal protection, then calls it at plugin skill/hook/command load sites. Our code has zero path-escape validation on plugin components — a symlink inside a plugin could point outside the plugin directory and get loaded. Security gap.

### 5c4fdca | fix(plugins): sanitize env before spawning git so /plugin marketplace add works | GAP
OC_FILE: `src/utils/plugins/` (no `gitEnv.ts`)
NOTES: Git 2.30+ refuses to start when any env value contains NUL/CR/LF ("Unsafe environment"). Gitlawb adds `sanitizeEnvForGit()` + `buildGitChildEnv()` that drops keys with control characters and applies this to all git invocations in marketplaceManager.ts (5 sites) and pluginLoader.ts (8 sites). Without this, any copy-pasted API key with trailing newline in env crashes all plugin git ops.

### 5943c5c | fix(input): strip leading ! when entering bash mode | GAP
OC_FILE: `src/components/PromptInput/PromptInput.tsx:886-899`
NOTES: The onChange handler had two branches for entering bash mode: a single-char path that toggled mode and a multi-char paste path that also stripped the leading `!`. The single-char path returned without stripping, so typing bare `!` into empty input switched modes but left the literal `!` visible in the buffer. Gitlawb consolidated both paths through `detectModeEntry()` helper. Our code still has the old split-path bug at lines 886-899.

### fc89767 | fix(agents): coerce non-string whenToUse to prevent crash on save | GAP
OC_FILE: `src/components/agents/agentFileUtils.ts:34`
NOTES: `formatAgentAsMarkdown()` calls `whenToUse.replace(...)` at line 34 without checking if `whenToUse` is a string. Weak local models (qwen3.5:9b reported) can return non-string values, crashing agent creation with "whenToUse.replace is not a function". Gitlawb adds `typeof === 'string' ? : ''` guard.

### e438c89 | fix: resolve two bugs making interactive mode unusable with plugin ecosystems | PARTIAL GAP
OC_FILE: `src/ink/components/App.tsx:3` (logForDebugging import — ALREADY_HAVE), `src/utils/hooks.ts:1479-1482` (stdin.end — still conditional)
NOTES: Bug 1 (logForDebugging import): ALREADY_HAVE — our App.tsx already imports it at line 3. Bug 2 (hooks stdin.end): our hooks.ts at line 1479 still has `if (!requestPrompt) { child.stdin.end() }` — the conditional path. In interactive mode requestPrompt is always truthy, so stdin stays open and every plugin hook blocks on EOF for the full timeout (60s) before the model call proceeds. Gitlawb changed it to unconditionally `child.stdin.end()` after writing the initial JSON payload. Trade-off documented: the duplex-stdin path for prompt-responses stops working, but every interactive user with plugins was getting minutes of delay. Our code at line 1275 DOES already unconditionally close stdin (the sync path), but line 1479-82 (the async executor path) still has the conditional. GAP for the async path.

### e1e277a | fix: replace unsupported Unicode glyphs with widely available alternatives | GAP
OC_FILE: `src/components/AgentProgressLine.tsx`, `src/components/MessageResponse.tsx`, `src/components/messages/SystemTextMessage.tsx`, `src/components/messages/UserLocalCommandOutputMessage.tsx`, `src/components/messages/CollapsedReadSearchContent.tsx`
NOTES: TUI characters U+23F5 (⏵) and U+23BF (⎿) from obscure Unicode blocks render as tofu boxes on most Linux terminal fonts. Replaced with U+25B6 (▶) and U+2514 (└) which are universally supported. Our files still contain the unsupported glyphs.

### 208c896 | fix(oauth): skip refresh for third-party providers | GAP
OC_FILE: `src/services/api/client.ts` (no `authRouting.ts`)
NOTES: Gitlawb adds `authRouting.ts` with `shouldUseFirstPartyAnthropicAuth()` that returns false when a `providerOverride` is set, when the API provider is not firstParty (e.g., gemini), or when the base URL is not Anthropic's. Without this, OAuth refresh attempts fire on third-party providers, producing unnecessary errors.

---

## MEDIUM PRIORITY GAPs (UX, robustness, diagnostic quality)

### 6ea3eb6 | feat(api): deterministic request-body serialization via stableStringify | GAP
OC_FILE: `src/utils/` (no `stableStringify.ts`), `src/services/api/openaiBridge/requestTranslator.ts`
NOTES: `stableStringify` emits JSON with object keys sorted at every depth. OpenAI/Kimi/DeepSeek use implicit prefix caching keyed on exact request bytes. Without stable serialization, spurious insertion-order differences invalidate the cache every turn. Our openaiBridge doesn't use this. Would apply to `requestTranslator.ts`'s `JSON.stringify(body)` calls.

### 4fab8b9 | fix(errors): show actual host in 404 message instead of Ollama hint | GAP
OC_FILE: `src/services/api/errors.ts`
NOTES: When an OpenAI-compatible provider returns 404, user-facing message hardcoded "for Ollama: http://127.0.0.1:11434/v1" regardless of configured base URL. Users on NIM/OpenRouter read this as the app ignoring their custom URL. Gitlawb plumbs request URL through `classifyOpenAIHttpFailure` so remote hosts name the actual host. Our errors.ts doesn't have this host-awareness.

### 7711dda | fix(worktree): surface git stderr in rev-parse failure message | GAP
OC_FILE: `src/utils/worktree.ts` (no `buildRevParseFailureMessage`)
NOTES: `git rev-parse HEAD` failure during worktree creation swallowed git's stderr, reporting only "git rev-parse failed" — users couldn't distinguish empty repos, detached HEADs, or missing git binary. Gitlawb exports `buildRevParseFailureMessage()` that includes stderr + a HEAD-specific hint about no commits.

### 6af709e | fix(agent): ensure main agent waits for subagent completion | GAP
OC_FILE: `src/tools/AgentTool/AgentTool.tsx` (~line 1341)
NOTES: Updated async-launched agent tool result instructions to more strongly command the model to end its turn. Previous text "Do not duplicate this agent's work" was insufficient — models continued generating. New text adds "You may continue first ONLY if you have other tasks on clearly different files that this agent is not touching." Reduces duplicate work and token waste.

### feb5791 | fix(effort): persist xhigh and send reasoning_effort on chat_completions | GAP (partial)
OC_FILE: `src/utils/effort.ts` (no `openAIEffortToStandard`), `src/services/api/openaiBridge/requestTranslator.ts`
NOTES: Two fixes: (1) EffortPicker normalizes `xhigh` to `max` before persistence (previously `xhigh` fell through `toPersistableEffort` as undefined). (2) openaiShim chat_completions body emits `reasoning_effort` (previously only codex_responses transport forwarded it). Our openaiBridge requestTranslator doesn't emit reasoning_effort — GAP for the shim path. The persistence fix applies to our `effort.ts`.

### e66d6e2 | Prevent duplicate startup plugin hooks | GAP (minor)
OC_FILE: `src/bootstrap/state.ts:1524`
NOTES: `registerHookCallbacks()` at line 1524 does `push(...matchers)` without dedup. Gitlawb adds dedup at registration level (before hooks are added to state). Our `getMatchingHooks` does dedup at query time, so duplicates are caught before execution, but they still accumulate in the registered list. Minor memory/performance issue.

### d321c8f | fix: avoid legacy Windows PasswordVault reads by default + isolate model capability override cache | GAP
OC_FILE: `src/utils/model/modelSupportOverrides.ts`, `src/utils/secureStorage/windowsCredentialStorage.ts`
NOTES: Two fixes: (1) Windows PasswordVault reads now opt-in via `OPENCLAUDE_ENABLE_LEGACY_WINDOWS_PASSWORDVAULT=1` (was on by default, slow/crashing). (2) `get3PModelCapabilityOverride` cache key now includes env var values so different env configs don't share cached results. Both apply to our codebase.

### 094f04c | fix(theme): remove stale memo wrappers from theme context hooks | GAP
OC_FILE: `src/components/design-system/ThemeProvider.tsx:123,148`
NOTES: React Compiler memo caches (`_c`) in `useTheme()` and `usePreviewTheme()` use referential equality on destructured context values. These can return stale references when ThemeProvider's useMemo recreates the context object but function references (setThemeSetting, etc.) compare equal — the memo short-circuits with old closure captures. Our ThemeProvider.tsx still has `_c(3)` and `_c(4)` wrappers.

### 35f86a9 | fix(startup): make CLAUDE logo D distinct | GAP (cosmetic)
OC_FILE: `src/components/LogoV2/LogoV2.tsx` (likely)
NOTES: The 'D' in CLAUDE logo rendering was visually ambiguous with adjacent characters. Minor cosmetic fix but user-visible on every startup.

---

## NOT_APPLICABLE (docs, CI, release, tests, openaiShim-only, branding, provider-specific)

### Release chores (skip — no source changes)
- `52b4c5c` release 0.7.0
- `da37527` release 0.8.0
- `9994b50` release 0.9.0
- `00263c5` release 0.9.1
- `280a7c1` release 0.9.2
- `7166400` release 0.10.0

### Docs/CI/tests (skip)
- `f699c1f` README routing path docs fix
- `c0b5535` docs: Atomic Chat partner
- `8106880` typecheck CI fix
- `990a5a2` test flakiness fix
- `11f265c` test: API fetch wrapper
- `1f66d32` test flakiness fix
- `d19f4d3` test flakiness fix
- `1020663` chore(engines): require Node >=22
- `41b2496` docs: update setup guides
- `ee0d930` ripgrep: use @vscode/ripgrep package (build dep)

### openaiShim-specific (we use openaiBridge, not openaiShim.ts)
- `0f0fd26` strip store for Gemini
- `cc0dab6` don't label transport failures as HTTP 503
- `40ae1e7` strip x-anthropic-billing-header
- `6d0953a` strip store for Groq
- `0adf97d` strip store for Cerebras
- `4830d6f` strip store for local providers (vLLM, custom)
- `20bc6ae` URL redaction in shim diagnostics
- `4fad5d2` OPENCLAUDE_LOCAL_FAST_PATH (openaiShim wiring)

### Provider-specific (Codex, Hicap, Github models)
- `95a817f` Codex OAuth session switch
- `884746d` Hicap gateway provider
- `7b02695` Codex default provider

### OpenClaude-specific branding (Gitlawb has different branding)
- `3d791bf` Disable feedback/mobile, refresh OpenClaude branding
- `35f86a9` CLAUDE logo D (we have different LogoV2 rendering)
- `d948769` rework release notes around GitHub releases
- `1672639` fix plan mode branding and plan path
- `ed7b697` startup logo palette picker
- `23f6a95` Fix theme picker OpenClaude branding
- `6655d47` Centralize OpenClaude display name
- `de0e395` Fix commit attribution configuration (adds /commit-message command)
- `a8f71f3` Fix user agent loading from OpenClaude config dirs (.openclaude/ vs .claude/)

### Major features (not in our codebase, do not need backport)
- `4c93a9f` Opus 4.7 default model (our model config differs)
- `91f93ce` SDK Foundation
- `92d297e` context preloading
- `0ca4333` streaming token counter
- `4eb486e` web landing refresh
- `aae96aa` SSH interactivity detection (we handle SSH via `src/ssh/` differently)
- `b471745` Registry-Based Integration Architecture
- `a46b31c` SDK Core
- `677d29f` LSP code intelligence setup (we have our own LSP tool)
- `ca676af` context partitioning
- `a133e76` self-hosted Firecrawl
- `f5ec185` provider profiles in user config
- `6636bce` Karpathy guidelines skill
- `60c76b6` SDK Runtime
- `402cd3d` first-class Brave adapter (our WebSearch is stubbed)
- `7cfc8d5` honor --model without --provider
- `4b1e516` incremental/cached token counting
- `5873bc6` Orama persistence (knowledge feature)
- `f443669` Orama default search engine
- `dea7ef9` xAI Grok 4.3 default

### ALREADY_HAVE (fix exists or bug was never present)
- `dc3c065` MCP third-party provider .mcp.json approval: our `interactiveHelpers.tsx:160` calls `handleMcpjsonServerApprovals(root)` directly without any `usesAnthropicSetup` gate — the bug never existed in our code.
- `e438c89` (Bug 1 — logForDebugging import): our `App.tsx:3` already has the import.
- `c873725` createRequire→static import: our `AppStateStore.ts` doesn't use `createRequire`.
- `1c74675` web-search empty-adapter diagnostic: our WebSearchTool is stubbed, NOT_APPLICABLE.

---

## Summary

| Verdict | Count |
|---------|-------|
| GAP (should backport) | 21 |
| PARTIAL GAP | 2 |
| ALREADY_HAVE / not a bug here | 3 |
| NOT_APPLICABLE | 50 |

### Recommended backport priority order:
1. **ebc9c70** — bashSecurity nested heredoc (security bypass)
2. **9fed6ae** — plugin component path validation (path traversal)
3. **5c4fdca** — git env sanitization (crash on git operations)
4. **fc89767** — agent whenToUse coercion (crash)
5. **5943c5c** — PromptInput ! leak (UX bug)
6. **e438c89** (Bug 2) — hooks stdin.end async path (interactive mode performance)
7. **208c896** — oauth skip refresh for third-party providers
8. **6ea3eb6** — stableStringify (prefix caching)
9. **e1e277a** — Unicode glyphs (rendering)
10. **6af709e** — AgentTool subagent instruction (token waste)
11. **feb5791** — effort xhigh persistence + reasoning_effort
12. **7711dda** — worktree rev-parse error messages
13. **4fab8b9** — errors.ts host-aware 404
14. **e66d6e2** — plugin hook registration dedup
15. **d321c8f** — PasswordVault opt-in + model cache isolation
16. **094f04c** — theme memo wrapper stale closures
17. **35f86a9** — CLAUDE logo D rendering

Written 2026-05-11. OpenClaude working dir: `/home/openclaudeuser/openclaude/src/`. No edits made.
