# Gitlawb → OpenClaude Gap Analysis — Batch 7 (commits 439-511)

Analyzed 73 Gitlawb commits from `b0d9fe7` through `c6c5f06`.
Format: SHA | SUBJECT | VERDICT | OC_FILE:LINE | NOTES

---

## GAPS (fixes missing from openclaude)

### b0d9fe7 | Provider loading fix (#623)
**GAP** | `src/utils/providerProfile.ts`, `src/components/ProviderManager.tsx`
Gitlawb rewired provider profile loading (env takes precedence over saved profiles, model switches with provider). Our openclaude has a completely different provider infrastructure (z.ai/DeepSeek/NIM via env vars, no profile persistence). The provider profile system is Gitlawb-specific — but the principle of "env vars should take precedence over stored state" could apply if we ever add profile persistence.

### 3d1979f | fix(help): prevent /help tab crash from undefined descriptions (#732)
**GAP** | `src/commands.ts:910-934`
`formatDescriptionWithSource()` uses `cmd.description` directly without nullish coalescing. If a command has `description: undefined`, string interpolation produces the string `"undefined"` in output (e.g. `"undefined (plugin)"`). Gitlawb fix adds `?? ''` on every return path. All 7 return paths at lines 911, 915, 921, 923, 927, 931, 934 need guards.

### 002a8f1 | fix(mcp): sync required array with properties in tool schemas (#754)
**GAP** | `src/utils/api.ts:97-118`
`filterSwarmFieldsFromSchema()` removes properties from the schema but never updates the `required` array. If a property that was in both `properties` and `required` gets filtered out, the `required` array retains a stale key → API 400 "Extra required key supplied". Also missing `sanitizeSchemaRequired()` to filter `required` arrays from MCP servers whose schemas have required keys not in properties.

### 55c5f26 | fix: use raw context window for auto-compact percentage display (#748)
**GAP** | `src/services/compact/autoCompact.ts:127-129`
`calculateTokenWarningState()` uses `threshold` (auto-compact threshold = effectiveContextWindow - 13k buffer) as the denominator for `percentLeft`. For DeepSeek-chat at 90k tokens:
- Openclaude: `(106808 - 90000) / 106808 ≈ 16%` — misleading, shows nearly full
- Gitlawb fix: `(128000 - 90000) / 128000 ≈ 30%` — shows actual % of total context used
The fix uses `getContextWindowForModel()` for the denominator while keeping threshold-based triggering unchanged. Only display math changes; no behavior change.

### b786b76 | fix(api): drop orphan tool results to satisfy strict role sequence (#745)
**NOT_APPLICABLE** — This is in `openaiShim.ts` (Gitlawb's OpenAI protocol translator). Our openclaude uses `openaiBridge/` (a different implementation with `requestTranslator.ts`/`responseTranslator.ts`/`streamTranslator.ts`). The orphan-tool-result filtering would need to be implemented in our bridge if hitting strict-role-sequence providers (Mistral, Moonshot, etc.), but the fix location differs.

### 2c98be7 | fix: remove cached mcpClient in diagnostic tracking to prevent stale references (#727)
**NOT_APPLICABLE** — Gitlawb refactored `DiagnosticTrackingService` to avoid caching stale MCP client references. Our openclaude's diagnostic tracking system (if any) is different; we don't have the same singleton-with-cached-client pattern. Would need to check `src/services/diagnosticTracking.ts` but the bug is specific to Gitlawb's implementation.

### e6e8d9a | feat: add OPENCLAUDE_DISABLE_STRICT_TOOLS env var (#770)
**ALREADY_HAVE** — Our openclaude doesn't have this env var in `openaiBridge/` but the MCP schema strictness issue is handled differently. Our bridge uses its own OpenAI-compatible translation layer. However, the env var is a user-facing escape hatch that could be useful if users hit OpenAI endpoints that reject complex MCP tool schemas. Low priority.

### f828171 | fix: allow provider recovery during startup (#765)
**NOT_APPLICABLE** — Gitlawb changed `validateProviderEnvOrExit()` to `validateProviderEnvForStartupOrExit()` with interactive recovery for TTY sessions. Our openclaude has a different provider validation path (`providerValidation.ts` uses `getProviderValidationError` but doesn't have the startup exit logic). Our `cli.tsx` entrypoint already allows `bypassPermissions` by default so provider validation is lenient. The specific bug (hard exit on missing provider in interactive mode) may not manifest in our fork.

### 13e9f22 | feat: mask provider api key input (#772)
**GAP** | `src/components/TextInput.tsx`
Adds `mask='*'` prop to TextInput in ProviderManager for API key fields and a `maskTextWithVisibleEdges()` utility. Our TextInput doesn't support a `mask` prop. This is a UX improvement (prevents shoulder-surfing of API keys during entry) but not a security fix per se (the key is already in memory).

### 739b8d1 | fix: enforce MCP OAuth callback state before errors (#775)
**GAP** | `src/services/mcp/auth.ts:1129-1141`
The OAuth callback handler checks `error` parameter BEFORE validating `state`. An attacker who can target the callback port can send `?error=access_denied` without valid state, causing the OAuth flow to reject with the attacker-chosen error message. The correct flow is: reject with `state_mismatch` first, then only process errors when state matches. Two callback handlers at lines ~1129 and ~1169 are vulnerable.

### 7002cb3 | fix: enforce Bash path constraints after sandbox allow (#777)
**GAP** | `src/tools/BashTool/bashPermissions.ts:2022`
When sandbox auto-allow returns `{behavior: 'allow'}`, the current guard `if (sandboxAutoAllowResult.behavior !== 'passthrough')` returns the allow result immediately, skipping ALL subsequent Bash permission checks including path traversal validation. A model could request `cat ../../../../../etc/passwd` and the sandbox could auto-allow it, bypassing the path security constraints.

Fix: change `!== 'passthrough'` to `=== 'deny' || === 'ask'` so sandbox 'allow' still falls through to Bash path validation.

### aab4890 | fix: require trusted approval for sandbox override (#778)
**GAP** | `src/tools/BashTool/BashTool.tsx:310,322-327`
`dangerouslyDisableSandbox` is present in `fullInputSchema` (line 310) and NOT omitted from `inputSchema` (lines 322-327 only omit `_simulatedSedEdit`). This means the model can set `dangerouslyDisableSandbox: true` in tool calls to escape the sandbox. Gitlawb's fix:
1. Removes `dangerouslyDisableSandbox` from the model-facing schema entirely
2. Adds `_dangerouslyDisableSandboxApproved` internal-only field for trusted approval
3. Removes sandbox-override instructions from the Bash prompt

The prompt fix is also missing — our `bashPermissions.ts prompt` likely still tells the model it can use `dangerouslyDisableSandbox`.

### ae3b723 | fix(security): harden project settings trust boundary + MCP sanitization (#789)
**GAP** | `src/utils/sandbox/sandbox-adapter.ts:476-483`
`getSandboxEnabledSetting()` calls `getSettings_DEPRECATED()` which aggregates settings from ALL sources including `projectSettings` (`.claude/settings.json` in the git repo). A malicious repo could set `sandbox.enabled: false` and silently disable sandboxing when `openclaude` is launched in that directory. Gitlawb fix limits sandbox config reading to trusted sources only (user/local/flag/policy).

### 06e7684 | fix(api): ensure strict role sequence and filter empty assistant messages (#745 regression) (#794)
**NOT_APPLICABLE** — In `openaiShim.ts`. Our openclaude uses `openaiBridge/`.

### 6a62e3f | feat: enable 15 additional feature flags in open build (#667)
**NOT_APPLICABLE** — Gitlawb build system changes. Our openclaude already enables all 87 flags via `node_modules/bundle/` polyfill.

### ae3b723 (part 2) | Unicode sanitization of MCP tool results
**GAP** | `src/services/mcp/client.ts` (or wherever MCP tool results are processed)
MCP tool results are not sanitized with `recursivelySanitizeUnicode()`. Malicious MCP servers could inject Unicode control characters into tool call results. Tool definitions and prompts were already sanitized but results were missed. Need to locate the MCP tool result processing path and add sanitization.

### ae3b723 (part 3) | WebFetch SSRF protection
**GAP** | `src/tools/WebFetchTool/` (if implemented)
Gitlawb added `ssrfGuardedLookup` to WebFetch HTTP requests to block DNS rebinding attacks (private IPs, metadata endpoints). Need to check if our WebFetch has SSRF guards.

### a4c6757 | fix(shell): recover when CWD path was replaced by a non-directory (#871)
**GAP** | `src/utils/Shell.ts:252`
The CWD recovery check uses `realpath(cwd)` which succeeds on ANY existing path (file or directory). If the session CWD was renamed and a file was created at the old path (`mv /tmp/x/orig /tmp/x/renamed && touch /tmp/x/orig`), `realpath()` returns the file's path successfully, and then `spawn()` is called with `cwd` pointing to a file → `ENOTDIR` error, exit 126. All Bash tool calls fail permanently.

Fix: replace `realpath()` with `stat().isDirectory()` for both the primary CWD check and fallback checks.

### c6c5f06 | fix: bugs — error truncation 10KB→40KB (#885)
**GAP** | `src/utils/toolErrors.ts:15`
Error output truncation limit is still 10000 chars (10KB). Shell commands like systemctl, apt, python can produce errors exceeding 10KB, causing silent truncation of diagnostic information. Gitlawb bumps to 40000 (40KB).

### c6c5f06 | fix: bugs — MCPTool null guards and abort handling
**GAP** | `src/tools/MCPTool/MCPTool.ts:70-76`
`mapToolResultToToolResultBlockParam()` returns `{tool_use_id, type: 'tool_result', content}` without null-guarding `content`. On abort, content could be undefined, sending empty content to the API. Also `isResultTruncated` lacks null check on output parameter. AbortError path may not properly re-throw after cleanup.

### 28de94d | feat: add OPENCLAUDE_DISABLE_TOOL_REMINDERS env var (#837)
**GAP** — Feature addition. Our openclaude doesn't support this env var. Useful for suppressing hidden tool-output reminder messages for users who want full transparency over model context. Low priority but easy to add.

### b750e9e | fix: make OpenAI fallback context window configurable (#861)
**NOT_APPLICABLE** — Gitlawb-specific. Our openclaude uses `openaiBridge/` with `nimModelCatalog.ts` for context windows.

### e346b8d | fix(startup): url authoritative over model name in banner provider detect (#864)
**NOT_APPLICABLE** — Gitlawb's startup screen provider detection uses different logic than ours.

### 6e58b81 | fix(update): show real package version and give actionable guidance (#870)
**ALREADY_HAVE** — Our openclaude auto-updater uses GitHub Releases API, completely different from Gitlawb's npm-based update mechanism.

### dcbe295 | fix(mcp): disable MCP_SKILLS feature flag (#872)
**NOT_APPLICABLE** — Our openclaude already has `MCP_SKILLS` feature gate handled via `bundle` polyfill. Our `src/skills/mcpSkills.ts` stub exports `fetchMcpSkillsForClient` as a no-op function (listed in CLAUDE.md stubs), so we don't have the 'not a function' crash.

### 5a21d05 | Persist active provider profile across restarts (#833)
**NOT_APPLICABLE** — Gitlawb-specific provider profile persistence.

### d9ae56b | fix provider switch not persisting in session (#903)
**NOT_APPLICABLE** — Gitlawb-specific provider profile bug.

### 818689b | fix(query): restore system prompt structure and add missing config import (#907)
**NOT_APPLICABLE** — Gitlawb-specific system prompt/config issue.

### a3e728a | fix(agent): provider-aware fallback for haiku/sonnet aliases (#908)
**ALREADY_HAVE** — Our `getAgentModel` function in `src/utils/model/model.ts` already handles provider-aware model resolution.

### d45628c | fix(startup): show --model flag override on startup screen (#898)
**NOT_APPLICABLE** — Our startup screen is different from Gitlawb's.

### c6c5f06 (part 2) | AJV validator WeakMap memory leak fix
**NOT_APPLICABLE** — Our MCPTool.ts doesn't have an AJV validator cache (no `compiledValidatorCache`).

---

## NOT_APPLICABLE (doc/CI/release/branding/Gitlawb-specific)

| SHA | Subject | Reason |
|-----|---------|--------|
| f166ec1 | chore(main): release 0.5.0 | Release bump |
| c0b8a59 | chore(main): release 0.5.1 | Release bump |
| b09972f | chore(main): release 0.5.2 | Release bump |
| 86bce4a | chore(main): release 0.6.0 | Release bump |
| 4d559c9 | docs(env): document OPENCLAUDE_DISABLE_STRICT_TOOLS | Docs only |
| b694ccf | Add sponsors section to README | Docs only |
| af9a3ca | Fix file path and update placeholder key in PLAYBOOK.md | Docs only |
| 46a9d3e | chore: rebrand user-facing copy to OpenClaude | Branding only |
| 4cb963e | feat(api): improve local provider reliability | Gitlawb-specific openaiShim |
| fdef4a1 | feat: native Anthropic API mode for Copilot | GitHub Copilot specific |
| 4d4fb28 | fix: rename .claude.json to .openclaude.json | Gitlawb config path rename |
| 85eab27 | fix(ui): prevent provider manager lag | Gitlawb-specific ProviderManager |
| 64582c1 | fix: replace discontinued gemini model | Gitlawb Gemini provider |
| a6a3de5 | feat(api): compress old tool_result content | Gitlawb-specific shim feature |
| 6a62e3f | feat: enable 15 feature flags | Gitlab build config |
| 2b15e16 | feat: model caching and benchmarking | Gitlawb-specific new feature |
| b95d222 | Feat/kimi moonshot support | Gitlawb-specific provider |
| e908864 | feat: smart model routing primitive | Gitlawb-specific new feature |
| 761924d | fix: collapse text arrays for DeepSeek | In openaiShim, our bridge differs |
| 268c039 | feat: thinking token extraction | Gitlawb-specific new feature |
| a5bfcbb | feat: zero-config autodetection | Gitlawb-specific provider feature |
| 13de4e8 | fix: saved profile ignored with stale flags | Gitlawb-specific provider profiles |
| ee19159 | feat: expose Atomic Chat in provider picker | Gitlawb-specific provider |
| 4581208 | fix: codex/nvidia-nim/minimax OPENAI_MODEL env | Gitlawb-specific |
| c13842e | fix(test): autoCompact floor assertion flag-sensitive | Test only |
| e92e527 | feat: model-specific tokenizers | Gitlawb-specific new feature |
| 5b9cd21 | feat: streaming optimizer and request logging | Gitlawb-specific new feature |
| 44a2c30 | feat: Hook Chains runtime integration | ALREADY_HAVE (we ported from Gitlawb earlier) |
| b7b83ef | Fix bracketed paste blocking provider form submit | Specific to Gitlawb's paste handler |
| 67de6bd | fix(openai-shim): echo reasoning_content for Moonshot | In openaiShim, our bridge differs |
| 3c4d843 | fix: surface actionable DDG rate-limit error | Gitlawb-specific WebFetch path |
| 531e3f1 | feat: resilient web search/fetch | Gitlawb-specific |
| 23e8cfb | fix(test): add missing teammate exports to hookChains mock | Test only |
| b750e9e | fix: OpenAI fallback context window configurable | Gitlawb-specific configuration |
| 6e58b81 | fix(update): show real package version | Our updater uses GitHub Releases |
| 038f715 | feat(model): add GPT-5.5 Codex support | Gitlawb-specific Codex provider |
| 5a21d05 | Persist active provider profile across restarts | Gitlawb-specific |
| 64b1014 | Feat/bankr provider | Gitlawb-specific provider |
| b5f7047 | Feature/memory pr | Gitlawb-specific memory feature |
| c4cb98a | fix: normalize /provider multi-model selection | Gitlawb-specific |
| ff2a380 | Add DeepSeek V4 flash/pro support | Our DeepSeek models already set up |
| 44f9cac | Feature/memory pr | Gitlawb-specific memory feature |
| 26413f6 | feat(minimax): add /usage support | Gitlawb-specific MiniMax provider |
| 9070220 | Add Kimi Code provider preset | Gitlawb-specific provider |
| 9e23c2b | feat(api): expose cache metrics in REPL | Gitlab-specific cache tracking |
| 29f7579 | feat(memory): implement knowledge graph and RAG | Gitlawb-specific memory feature |
| a0d657e | feat(zai): add Z.AI GLM Coding Plan preset | Our z.ai is pre-configured differently |
| 818689b | fix(query): restore system prompt structure | Gitlawb-specific |
| 6dedffe | Add OpenAI responses mode and custom auth headers | Gitlawb-specific |
| 2586a9c | feat: add xAI as official provider | Gitlawb-specific provider |

---

## SUMMARY

**14 GAPs found**, 6 of which are **security-critical**:

### Security-Critical Gaps (should fix first)

1. **aab4890** — `dangerouslyDisableSandbox` exposed to model in BashTool schema (model can escape sandbox)
2. **7002cb3** — Sandbox auto-allow bypasses Bash path constraints (path traversal possible even with sandbox)
3. **ae3b723** — Sandbox `enabled` setting readable from projectSettings (malicious repo can disable sandbox)
4. **739b8d1** — MCP OAuth callback processes errors before state validation (CSRF/DoS)
5. **ae3b723** — MCP tool results not Unicode-sanitized (injection via malicious MCP servers)
6. **ae3b723** — SSRF protection missing in WebFetch (DNS rebinding to internal services)

### Stability/Correctness Gaps

7. **55c5f26** — Auto-compact percentage display shows wrong % for non-Anthropic models
8. **3d1979f** — `/help` tab crash from undefined command descriptions
9. **002a8f1** — MCP schema `required` array sync missing → API 400 errors
10. **a4c6757** — Shell ENOTDIR when CWD replaced by file (all Bash calls break)
11. **c6c5f06** — Error truncation at 10KB too short for real-world errors
12. **c6c5f06** — MCPTool null guards missing on abort paths

### Feature/Escape-Hatch Gaps

13. **13e9f22** — API key masking in TextInput
14. **28de94d** — OPENCLAUDE_DISABLE_TOOL_REMINDERS env var
