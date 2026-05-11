# Gitlawb Gap Analysis — Batch 6 (commits 366–438)

Analysis date: 2026-05-11
Analyzed: 73 commits from Gitlawb main branch  
Method: git show + Read() openclaude source files for comparison

## GAPS (missing in openclaude)

| SHA | Subject | Verdict | OC File:Line | Notes |
|-----|---------|---------|-------------|-------|
| 08cc6f3 | fix(read/edit): make compact line prefix unambiguous for tab-indented files | **GAP** | `src/utils/file.ts:306` | Our `addLineNumbers()` uses `\t` (tab) separator in compact mode: `` `${index + startLine}\t${line}` ``. For tab-indented files (Makefiles, etc.), `N\t\tcontent` is ambiguous — is the first `\t` the prefix separator or file indentation? Gitlawb switches to `→` (arrow): `` `${index + startLine}→${line}` ``. Our `stripLineNumberPrefix` already handles both separators (line 326: `[\u2192\t]`), so the parse side is ready — only the output side needs the switch. |
| eed77e6 | fix: prevent crash in commands tab when description is undefined | **GAP** | `src/utils/truncate.ts:140` | Our `truncate(str, maxWidth, singleLine)` does NOT guard against `str` being `undefined`. If a command lacks a description, `str.indexOf('\n')` throws TypeError, crashing the /help commands tab. Gitlawb adds an early return for falsy values at the top of the function. |
| b280c74 | fix serialize git worktree mutations and forward teammate PATH (partial) | **GAP** | `src/utils/swarm/spawnUtils.ts:96` | Our `TEAMMATE_ENV_VARS` does NOT include `PATH` or `CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST`. Source builds may rely on user shell PATH for rg/node/bun and other tools. Teammates should also inherit the leader-selected provider route. The serialization part (`withGitWorktreeMutationLock`) is ALREADY_HAVE. |
| 25ce2ca | fix: resolve 12 bugs (context overflow 500 handler) | **GAP** | `src/services/api/errors.ts` | Our `errors.ts` does NOT have detection for 500 errors caused by context overflow (when the API returns 500 instead of 400 for oversized conversations). Gitlawb adds keyword-based detection (`'too many tokens'`, `'request too large'`, `'context length'`, etc.) and surfaces a user-friendly recovery message. |
| 25ce2ca | fix: resolve 12 bugs (continuation nudge) | **GAP** | `src/query.ts` | Our `query.ts` does NOT have continuation signal detection — the model can say "so now I have to do it" without tool calls and the agent loop interprets this as task completion. Gitlawb adds regex-based continuation signal detection with a `MAX_CONTINUATION_NUDGES` cap (3) and completion marker exclusion. |
| 25ce2ca | fix: resolve 12 bugs (circuit breaker safety net) | **GAP** | `src/query.ts` | Our `query.ts` does NOT have the auto-compact circuit breaker safety net. When auto-compact fails 3+ consecutive times and reactive-compact is also exhausted/disabled, the oversized context goes straight to the API and gets a 500. Gitlawb adds a pre-API-call check that blocks the request with a clear message instead of burning an API call. |
| 25ce2ca | fix: resolve 12 bugs (SendMessage race condition) | **GAP** | `src/tools/SendMessageTool/SendMessageTool.ts` | Our `SendMessageTool` does NOT double-check task status before auto-resuming stopped agents. Two concurrent SendMessage calls to the same stopped agent could both trigger `resumeAgentBackground()`, causing duplicate task registration. Gitlawb adds a fresh status re-check after acquiring the task reference. |
| 25ce2ca | fix: resolve 12 bugs (AgentTool defensive cleanup) | **GAP** | `src/tools/AgentTool/AgentTool.tsx` | Our `AgentTool` cleanup for backgrounded agents may not wrap each call individually. If `clearInvokedSkillsForAgent` throws, `clearDumpState` is skipped and dump state leaks. Gitlawb wraps each in its own `try/catch`. |
| 25ce2ca | fix: resolve 12 bugs (MCP URL elicitation abort check) | **GAP** | `src/services/mcp/client.ts` | Our `callMCPToolWithUrlElicitationRetry` does NOT check `signal.aborted` before each retry attempt. A cancelled elicitation retry loop continues spinning until MAX retries. Gitlawb adds an abort guard at the top of each loop iteration. |
| 6b2121d | fix(models): prevent /models crash from non-string saved model values | **GAP** | `src/utils/model/model.ts:67` | Our `getUserSpecifiedModelSetting()` at line 75 does `settings.model` without a `typeof === 'string'` runtime guard. A saved non-string value (e.g. `{bad: true}` from a corrupted config) passes the truthy check at line 79 but can crash downstream string methods. Gitlawb adds a `typeof model !== 'string'` guard. |

## ALREADY_HAVE (present in openclaude)

| SHA | Subject | Verdict | Notes |
|-----|---------|---------|-------|
| c385047 | feat: add auto-fix service | ALREADY_HAVE | Ported from Gitlawb in 2026-04-25 (263 LOC source + skill + notice). Settings schema, runner, hook wiring all present. |
| aeaa658 | fix: prevent infinite auto-compact loop (partial) | ALREADY_HAVE | Our `getEffectiveContextWindowSize()` at `src/services/compact/autoCompact.ts:59-61` already has the floor: `Math.max(effectiveContext, reservedTokensForSummary + getAutoCompactBufferTokens(model))`. Our unknown-model fallback is 200k (MODEL_CONTEXT_WINDOW_DEFAULT), not 8k — no negative context issue. MiniMax entries N/A (different context window table). |
| b280c74 | fix serialize git worktree mutations (partial) | ALREADY_HAVE | `withGitWorktreeMutationLock` at `src/utils/worktree.ts:207` already has proper promise-chained serialization with cleanup. |
| 25ce2ca | fix: resolve 12 bugs (MCP tool timeout) | ALREADY_HAVE | `getMcpToolTimeoutMs()` at `src/services/mcp/client.ts:227` returns `MCP_TOOL_TIMEOUT` env or `DEFAULT_MCP_TOOL_TIMEOUT_REASONABLE_MS = 600_000` (10 min). The old `DEFAULT_MCP_TOOL_TIMEOUT_MS = 100_000_000` is a stale constant not actually used. |
| 25ce2ca | fix: resolve 12 bugs (MCP tools/list retry) | ALREADY_HAVE | `fetchToolsForClient` at line 1814 has 1-attempt retry on transient failure (upstream 2.1.132), with sleep-based backoff. |
| 31be66d | feat: add allowBypassPermissionsMode setting | ALREADY_HAVE | Superseded by our fork's default bypassPermissions behavior. Our `permissionSetup.ts` appends `bypassPermissions` to `orderedModes` as the final fallback. The setting would be a minor UX improvement but doesn't change behavior for our users. |

## NOT_APPLICABLE (to this fork)

| SHA | Subject | Reason |
|-----|---------|--------|
| 598651f | fix: rebrand prompt identity to openclaude | Gitlawb branding — we maintain our own identity |
| 9ccaa7a | feat: add /cache-probe diagnostic command | OpenAI-specific diagnostic — our fork doesn't use openai-shim for API calls |
| 68c2968 | fix: restore Ollama auto-detect in first-run setup | Provider-specific UI — our fork has different provider management |
| 6924718 | fix: update theme preview on focus change | Different component architecture |
| 07621a6 | fix: scrub canonical Anthropic headers from 3P shim requests | We don't have a 3P shim layer — we use openaiBridge/ for NIM |
| cb8f8b7 | fix: let saved provider profiles win on restart | No provider profile system in our fork |
| a7f5982 | fix: add GitHub Copilot model context windows and output limits | Different model context window system |
| 8aaa4f2 | fix: add store:false to Chat Completions and /responses fallback | Different API shim architecture |
| f4ac709 | fix: report cache reads in streaming and correct cost calculation | Different streaming architecture |
| 91e4cfb | fix: WebSearch providers + MCPTool bugs | Our WebSearch routes through zendriver MCP — no custom providers. MCPTool output schema difference is minor (zod string vs union). |
| 6e94dd9 | fix(ink): restore host prop updates in React 19 reconciler | Specific to Gitlawb's Ink/React setup |
| b126e38 | fix: display selected model in startup screen | No StartupScreen.ts in our fork |
| 4c50977 | Decouple and fix mistral | Provider-specific (Mistral) |
| 7817fe8 | fix(web-search): stop leaking abort listeners in custom provider retry | Our WebSearch has no custom providers |
| a02c441 | fix(web-search): close SSRF bypasses in custom provider hostname guard | Our WebSearch has no custom providers — routes through zendriver |
| 2e0e14d | fix: add LiteLLM-style aliases for GitHub Copilot context windows | Different model context window architecture |
| b3f3dc4 | Prefer AGENTS.md over CLAUDE.md | Convention preference — we maintain CLAUDE.md convention |
| 40ac164 | ci: add secure automated release workflow | CI |
| 3cefe22 | ci: remove invalid release-please input | CI |
| a3633ac | chore(main): release 0.2.0 | Release |
| 2e39d26 | Fix/release please invalid input | CI |
| 812facf | Fix/release please invalid input | CI |
| 15de1d6 | Fix/release please invalid input | CI |
| d03d77b | ci: keep manual publish path for current release | CI |
| fa4b6a9 | Fix/manual publish current release | CI |
| 41a86d0 | ci: publish from release events | CI |
| 9419e8a | fix(provider): add recovery guidance for missing OpenAI API key | Provider-specific (OpenAI key) |
| ad11414 | chore(main): release 0.2.1 | Release |
| 84fcc7f | ci: publish npm in release workflow | CI |
| d2a057c | chore(main): release 0.2.2 | Release |
| f6a4455 | chore(main): release 0.2.3 | Release |
| 30c866d | fix(openai-shim): preserve tool result images and local token caps | packages/openai-shim — different architecture |
| 64298a6 | feat: implement /loop command | Different feature set — we have cron/autonomy |
| 7c8bdcc | fix: route OpenAI Codex shortcuts to correct endpoint | Different architecture |
| 03e0be6 | fix: extend provider guard to protect anthropic profiles from cross-terminal override | No providerProfiles.ts in our fork — no multi-provider profile system |
| adbe391 | fix: replace broken bun:bundle shim with source pre-processing | Our fork uses `node_modules/bundle/` polyfill — different approach entirely |
| df2b9f2 | fix: improve fetch diagnostics for bootstrap and session requests | Specific to Gitlawb's provider bootstrap flow |
| 99a1714 | feat: activate coordinator mode in open build | Our fork already has coordinator mode |
| 24d485f | feat: activate local-only team memory in open build | Our fork already has team memory |
| b818dd5 | feat: implement Monitor tool for streaming shell output | Our fork has MonitorTool already |
| 0e48884 | feat: local feature flag overrides via ~/.claude/feature-flags.json | Our fork uses CLAUDE_INTERNAL_FC_OVERRIDES + bundle polyfill |
| 252808b | feat: activate message actions in open build | Our fork already has all features |
| fc7dc9c | Add Codex OAuth provider flow for ChatGPT account sign-in | Provider-specific (Codex/ChatGPT OAuth) |
| 1741f32 | docs: add GitLawb mirror to README | Docs |
| a07e5ef | fix: bump axios 1.14.0 -> 1.15.0 | Dependency version |
| 658d076 | feat: add Docker image build and push to GHCR on release | Docker/CI |
| c1beea9 | feat: open useful USER_TYPE-gated features to all users | Our fork already enables everything |
| 131b31b | chore(main): release 0.3.0 | Release |
| 0ed50cc | Fix Docker deployment | Docker/CI |
| 7187fc0 | docs: add Star History chart to README | Docs |
| 114f772 | tests: avoid global fetch mutation in GitHub device flow tests | Test |
| 12dd375 | feat: add ripgrep to Dockerfile for faster file searching | Docker |
| a00b792 | fix: strip comments before scanning for missing imports | Different build system — we don't use `scripts/build.ts` |
| c207cdb | ci: skip release-please on fork repositories | CI |
| 51191d6 | feat: add NVIDIA NIM and MiniMax provider support | Our fork has NIM via openaiBridge/ — different architecture |
| b66633e | Feat/multi model provider support | Different architecture |
| 77083d7 | Fix/MCP exposure v2 TODO's | OAuth-secure-storage change (different auth architecture), skip-official-registry prefetch (different MCP discovery), experimental-beta-default-off (different API setup) |
| fbcd928 | feat(vscode): add full chat interface to OpenClaude extension | VSCode extension — not in our fork |
| d32a2a1 | docs: add Ollama launch integration documentation | Docs |
| d6f5130 | fix: focus "Done" option after completing provider manager actions | Different provider UI |
| 2ff5710 | fix retry Codex and OpenAI fetches via proxy-aware helper | Different API architecture (no codexShim/openaiShim) |
| 80a00ac | feat(api): classify openai-compatible provider failures | Different error handling architecture |
| 43ac6db | feat: add Alibaba Coding Plan (DashScope) provider support | Provider-specific |
| 3424663 | fix(ui): show correct endpoint URL in intro screen for custom Anthropic endpoints | Different startup UI |
| 651123d | chore(main): release 0.4.0 | Release |

## Summary

- **Total commits analyzed:** 73
- **GAPS found:** 10 (across 4 unique commits)
- **ALREADY_HAVE:** 7
- **NOT_APPLICABLE:** 56

**Highest-priority gaps (security/stability):**
1. `eed77e6` — prevent crash in commands tab (undefined guard in truncate)
2. `6b2121d` — prevent /models crash from non-string saved model values
3. `08cc6f3` — tab-indented file ambiguity in compact line prefix

**Medium-priority gaps (robustness):**
4. `25ce2ca` — context overflow 500 handler in errors.ts
5. `25ce2ca` — circuit breaker safety net for auto-compact failures
6. `25ce2ca` — SendMessage race condition double-check
7. `25ce2ca` — AgentTool defensive cleanup (individual try/catch)
8. `25ce2ca` — MCP URL elicitation abort signal check

**Low-priority gaps (enhancement):**
9. `25ce2ca` — agent continuation nudge (prevents premature completion)
10. `b280c74` — forward PATH to teammates
