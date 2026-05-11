# Gitlawb → OpenClaude Gap Analysis — Batch 2 (commits 74–146)

Analysis of Gitlawb commits from `802cb4e` through `3b7b974` compared against openclaude source at `/home/openclaudeuser/openclaude/src/`.
Generated: 2026-05-11

---

## GAP Summary

| # | SHA | Subject | Verdict | OC File | Notes |
|---|-----|---------|---------|---------|-------|
| 1 | `802cb4e` | fix: add OpenAI and Gemini to /login 3rd-party platform screen | NOT_APPLICABLE | — | UI text in ConsoleOAuthFlow.tsx; openclaude uses different login flow with z.ai/NIM/DeepSeek providers |
| 2 | `63adb95` | fix: support nested skill directories | ALREADY_HAVE | `src/skills/loadSkillsDir.ts:545-573` | buildNamespace(), getSkillCommandName(), and recursive findSkillMarkdownFiles() already present |
| 3 | `1d82022` | fix: clarify nested skill labels in skills menu | GAP (minor) | `src/components/skills/SkillsMenu.tsx` | No getSkillListLabel() function for displaying namespace:leaf-name format |
| 4 | `e8dd3d6` | fix: sort skills menu by namespace | GAP (minor) | `src/components/skills/SkillsMenu.tsx` | Sort comparison still uses getCommandName(a).localeCompare; Gitlawb uses a.name.localeCompare for namespace-aware ordering |
| 5 | `66f5981` | fix(codex): Support Multi-Agent framework schemas | NOT_APPLICABLE | `src/services/api/codexShim.ts` (does not exist) | openclaude uses openaiBridge/ instead of codexShim; different architecture |
| 6 | `3491dc3` | fix: preserve Gemini thought signatures for tools | NOT_APPLICABLE | `src/services/api/openaiShim.ts` (does not exist) | openclaude uses openaiBridge/; Gemini tool call extra_content handled differently |
| 7 | `9d464f3` | feat: add gradient startup screen | NOT_APPLICABLE | — | Gitlawb-specific branding feature (StartupScreen.ts, Messages.tsx LogoV2 removal) |
| 8 | `39d9616` | fix: update DeepSeek context window 64k→128k | ALREADY_HAVE | `src/utils/context.ts:156,259,262` | openclaude already has 128_000 DeepSeek context window via getContextWindowForModel() |
| 9 | `598f59e` | fix: map tool_choice 'none' in OpenAI shim | ALREADY_HAVE | `src/services/api/openaiBridge/requestTranslator.ts:345-346` | openaiBridge already maps `tool_choice: 'none'` → `'none'` |
| 10 | `217a864` | feat: support disabling commit co-author attribution | ALREADY_HAVE | `src/utils/attribution.ts:52-98` | Already supports isUndercover() + settings.includeCoAuthoredBy + settings.attribution |
| 11 | `4c9b9f0` | fix: support Azure Cognitive Services and Azure OpenAI endpoints | NOT_APPLICABLE | `src/services/api/openaiBridge/` | openaiBridge uses provider registry; Azure would be new provider, not a missing guard fix. openaiBridge does not yet have Azure provider |
| 12 | `c22045e` | fix: skip Anthropic setup flow for third-party providers | ALREADY_HAVE | `src/main.tsx` | showSetupScreens() is bypassed in openclaude; usesAnthropicAccountFlow() not needed |
| 13 | `42e614d` | removed telemetry noise | ALREADY_HAVE | `src/services/analytics/` | All analytics stubbed out; CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 set at entrypoint |
| 14 | `e524be7` | fix: show OpenAI/Gemini provider info in /status panel | NOT_APPLICABLE | `src/utils/status.tsx` | openclaude's getAPIProvider() only returns firstParty/bedrock/vertex/foundry; 3P routing through bridge layer |
| 15 | `ab911d1` | fix: make schema normalization provider-aware for Gemini | NOT_APPLICABLE | `src/services/api/openaiShim.ts` (does not exist) | Different architecture; openaiBridge handles schemas via requestTranslator |
| 16 | `5f75f67` | security: pin all dependencies to exact versions | NOT_APPLICABLE | — | openclaude has its own package.json with different dependency set |
| 17 | **`ffbc1f8`** | **fix: support CSI-u printable input on Windows** | **GAP** | `src/ink/parse-keypress.ts:494-506` | **Three missing sub-fixes:** (a) decodeModifier uses `const m = modifier - 1` — on Windows modifier=0 produces m=-1 which corrupts all modifier bits via two's complement; (b) no isPrivateUseCodepoint() guard; (c) keycodeToName only handles ASCII 32-126, not Unicode printable codepoints from CSI-u |
| 18 | `4918caa` | Update resume command in gracefulShutdown message | GAP (minor) | `src/utils/gracefulShutdown.ts:187` | Still prints `claude --resume` instead of `openclaude --resume` |
| 19 | **`2bade92`** | **fix: add clearer ripgrep install guidance** | **GAP** | `src/utils/ripgrep.ts` | No RipgrepUnavailableError class, no wrapRipgrepUnavailableError(), no platform-specific install hints (winget/brew/apt) |
| 20 | `0746802` | security: kill GrowthBook phone-home and auto-updater at build time | ALREADY_HAVE | `src/services/growthbook/`, `src/services/analytics/` | Already stubbed; CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 at entrypoint |
| 21 | `9590066` | fix: gracefully handle Docker/remote Ollama in system-check | NOT_APPLICABLE | `scripts/system-check.ts` | openclaude does not use Gitlawb's system-check script |
| 22 | **`310f1d3`** | **fix: provide local session title fallback for 3P providers** | **GAP** | `src/utils/sessionTitle.ts:135-141` | **catch block returns `null` on failure — no localFallbackTitle().** On non-Anthropic providers the Haiku API call fails and the terminal tab stays permanently blank/locked. Gitlawb adds a 7-word sentence-cased local fallback |
| 23 | `302d9d4` | fix: enable session title generation for non-firstParty | NOT_APPLICABLE | `src/screens/REPL.tsx` | Part of the same session title PR; openclaude has different REPL structure |
| 24 | `63546dc` | chore: rename default terminal title to Open Claude | NOT_APPLICABLE | — | Branding change |
| 25 | **`6c35f4e`** | **fix: guard transcript sandbox subscription (ctrl-o crash)** | **GAP** | `src/components/SandboxViolationExpandedView.tsx:34-41` | **useEffect callback calls `store.subscribe()` without checking if store is null or subscribe is a function.** Gitlawb adds `if (!store \|\| typeof store.subscribe !== "function") return;` before the subscribe call. Openclaude does NOT have this guard |
| 26 | **`d156aed`** | **fix(shim): implement tolerant bracket balancer for truncated tool JSON** | **GAP** | `src/services/api/openaiBridge/streamTranslator.ts:356-405` | **StreamTranslator finalize() has no bracket balancer.** When tool-use JSON is truncated mid-stream (finish_reason='length'), the incomplete JSON is emitted as-is. Gitlawb tries 10 suffix combinations (}, "}, ]}, etc.) to close the JSON before content_block_stop. Applied to openaiShim; analogous gap exists in openaiBridge streamTranslator |
| 27 | `537ac24` | fix: use max_completion_tokens instead of max_tokens for OpenAI APIs | NOT_APPLICABLE | `src/services/api/openaiShim.ts` (does not exist) | openaiBridge requestTranslator handles max_tokens differently via per-provider requestOptions |
| 28 | `f3ebd7d` | fix: convert max_tokens to max_completion_tokens for Azure OpenAI | NOT_APPLICABLE | — | Double NOT_APPLICABLE: openaiShim file + Azure-specific |
| 29 | `25c5987` | feat: add support for GitHub Models provider | NOT_APPLICABLE | — | New provider; not needed for openclaude |
| 30 | `577e654` | feat: add support for Atomic Chat provider | NOT_APPLICABLE | — | New provider; not needed for openclaude |
| 31 | **`01246f9`** | **fix: use correct default port for wss:// in NO_PROXY matching** | **GAP** | `src/utils/proxy.ts:100` | **`const port = url.port \|\| (url.protocol === 'https:' ? '443' : '80')` — does not handle wss:// protocol.** NO_PROXY entries with explicit ports will mismatch when connecting via WSS (WebSocket secure). Fix: add `\|\| url.protocol === 'wss:'` |
| 32 | `5fae22a` | fix: restrict .openclaude-profile.json to owner-only permissions (0600) | NOT_APPLICABLE | — | openclaude doesn't have .openclaude-profile.json or provider-bootstrap.ts |

---

## Priority GAPs (should fix)

### High Priority
1. **`parse-keypress.ts` decodeModifier bug** (`ffbc1f8`) — Windows CSI-u modifier=0 produces m=-1, setting all modifier bits to true due to two's complement. Breaks keyboard input on Windows terminals. Fix: `Math.max(modifier, 1) - 1`. Also missing: isPrivateUseCodepoint() and Unicode codepoint handling beyond ASCII 32-126.

2. **`SandboxViolationExpandedView.tsx` null store crash** (`6c35f4e`) — useEffect callback dereferences `store.subscribe(...)` without null check. If `getSandboxViolationStore()` returns null (common when sandboxing disabled), Ctrl-O transcript expansion crashes. Fix: add `if (!store \|\| typeof store.subscribe !== "function") return;` before the subscribe call.

### Medium Priority
3. **`sessionTitle.ts` 3P provider fallback** (`310f1d3`) — On non-Anthropic providers, session title generation fails silently and returns null. Terminal tab stays blank. Fix: add localFallbackTitle() that takes first 7 words of user's first message, sentence-cases them.

4. **`proxy.ts` wss:// default port** (`01246f9`) — NO_PROXY matching doesn't handle wss:// WebSocket connections. Fix: `url.protocol === 'https:' \|\| url.protocol === 'wss:' ? '443' : '80'`.

5. **`streamTranslator.ts` bracket balancer** (`d156aed`) — Truncated tool JSON in OpenAI-compatible streams leaves tool arguments incomplete. Fix: try suffix combinations to balance brackets before content_block_stop.

### Low Priority (polish)
6. **`ripgrep.ts` install guidance** (`2bade92`) — Missing RipgrepUnavailableError class with platform-specific install hints (winget/brew/apt).
7. **`gracefulShutdown.ts` resume command** (`4918caa`) — Says `claude --resume` instead of `openclaude --resume`.
8. **`SkillsMenu.tsx` nested labels** (`1d82022`/`e8dd3d6`) — Missing getSkillListLabel display and namespace-aware sort order.

---

## NOT_APPLICABLE Patterns

- **openaiShim.ts / codexShim.ts changes:** 10 commits modify these files. openclaude uses `openaiBridge/` (14 files) with a fundamentally different architecture — provider registry, request/response/stream translators. Commits: `66f5981`, `3491dc3`, `4c9b9f0`, `ab911d1`, `537ac24`, `f3ebd7d`, `d156aed`, `80df0c5`, `39d9616`, `598f59e`
- **Gitlawb-specific branding:** 3 commits — `9d464f3` (gradient screen), `63546dc` (rename title), `47b19c9` (accent color)
- **New provider additions:** 2 commits — `25c5987` (GitHub Models), `577e654` (Atomic Chat)
- **CI/docs/build/version:** `9951da5`, `6c0d262`, `93bc50f`, `2619401`, `8645dc4`, `cb8973e`, `f07f11b`, `36654c1`, `69f1d0b`, `b204ae7`, `7ce7dc1`, `1ce19b9`, `936107f`, `8466fc1`, `fd6f4e6`, `ac2ea6a`

---

## Verification Notes

- All `ALREADY_HAVE` verdicts confirmed by reading (not grepping) the specific openclaude source files at the lines listed.
- All `GAP` verdicts confirmed by reading both the Gitlawb diff AND the corresponding openclaude source file.
- Merge commits that only pull together existing changes without unique diffs are marked NOT_APPLICABLE.
- The `d156aed` bracket balancer gap was confirmed by reading `streamTranslator.ts:356-405` — the finalize() function closes tool blocks directly without attempting bracket recovery.
