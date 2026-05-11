# CCB Batch 2 Gap Analysis (Commits 83-164)
# OpenClaude vs CCB comparison — generated 2026-05-11

28e40ddc | refactor: Bun native define for globalThis injection | NOT_APPLICABLE | — | Build tooling only (scripts/dev.ts, build.ts). No openclaude source impact.
4f323efb | test: Phase 5 — 12 test files | NOT_APPLICABLE | — | Test files only.
4d1bc87e | Merge branch claude-code-best:main into main | NOT_APPLICABLE | — | Merge commit.
2e4d6e21 | Update hooks.ts — sandbox hook commands | GAP | src/utils/hooks.ts:execCommandHook | CCB wraps hook shell commands with SandboxManager (network-only sandbox). Openclaude has SandboxManager but does NOT sandbox hook commands. Hook commands run unsandboxed, risking data exfiltration via `curl`/`wget` in malicious hook configs.
3c5eb0ed | Merge branch test/test-most-core-func | NOT_APPLICABLE | — | Merge commit.
5fda8724 | docs: update docs | NOT_APPLICABLE | — | Docs.
e815002f | Merge branch main into main | NOT_APPLICABLE | — | Merge commit.
9c3803d1 | docs: test plan | NOT_APPLICABLE | — | Docs.
006ad97f | test: new test files | NOT_APPLICABLE | — | Test.
1086f683 | docs: test + auto mode docs | NOT_APPLICABLE | — | Docs.
8697c916 | feat: complete test 16-17 | NOT_APPLICABLE | — | Test.
799dacc4 | test: batch of test files | NOT_APPLICABLE | — | Test.
ac1f0295 | fix: batch fix "external" literals → process.env.USER_TYPE | NOT_APPLICABLE | src/buddy/useBuddyNotification.tsx + 10 files | CCB replaced `"external" as string` bundler constants with `process.env.USER_TYPE` runtime checks. Openclaude uses the upstream pattern (`"external" === 'ant'`) which Bun DCEs at build time via `bun:bundle`. No runtime bug — DCE handles it.
6f5623b2 | docs: new test docs | NOT_APPLICABLE | — | Docs.
ce29527a | test: add more test files | NOT_APPLICABLE | — | Test.
4ab4506d | fix: USER_TYPE=ant TUI startup — undefined globals | GAP (minor) | src/components/Spinner.tsx:223 | `computeTtftText` is called at runtime but never defined in openclaude source (was a bundler-injected global). CCB polyfilled it. Openclaude uses it from react-compiler-runtime `_c` memoization; works from Bun source but could fail in compiled binary if the `react/compiler-runtime` import path isn't resolved by the build. Also: `getKairosActive`/`getUserMsgOptIn`/`getFeatureValue_CACHED_MAY_BE_STALE` are used in Spinner.tsx brief-only check — all stubbed in openclaude so fine.
68ccf28b | feat: attempt to fix auto mode | NOT_APPLICABLE | — | Docs + prompt templates (yolo-classifier-prompts/). Openclaude has /super mode with different architecture.
88b45e0e | chore: delete junk scripts | NOT_APPLICABLE | — | Chore.
be82b71c | feat: auto mode classifier prompts + FEATURE_* env injection | NOT_APPLICABLE | — | Build/dev.ts FEATURE_* scanning + prompt files. build.ts changes NOT_APPLICABLE. cli.tsx AUTO_MODE_ENABLED_DEFAULT feature gate is already handled differently in openclaude.
991ccc67 | chore: delete src under src | NOT_APPLICABLE | — | Chore.
87fdd455 | chore: delete debug code | NOT_APPLICABLE | — | Chore.
70f32e25 | Merge branch main into pr/smallflyingpig/36 | NOT_APPLICABLE | — | Merge commit.
47d88478 | docs: correct feature usage | NOT_APPLICABLE | — | Docs.
0d0304d6 | Merge branch pr/smallflyingpig/36 | NOT_APPLICABLE | — | Merge commit.
7dfbcd0e | feat: update buddy features | NOT_APPLICABLE | src/commands.ts, src/commands/buddy/buddy.ts, src/entrypoints/cli.tsx | CCB updated buddy command registration (feature gate, alias). Openclaude has full buddy implementation via direct imports bypassing feature gates. No gap.
4337b82e | Merge branch pr/programming-pupil/33 | NOT_APPLICABLE | — | Merge commit.
b6f37082 | Learn/20260401 (#39) | NOT_APPLICABLE | — | PR merge with learning/docs content.
919cf555 | feat: add developer default features | NOT_APPLICABLE | — | scripts/dev.ts only. Build tooling.
22ca3a11 | Merge remote-tracking branch origin/main | NOT_APPLICABLE | — | Merge commit.
5ee49fd1 | docs: add feature descriptions | NOT_APPLICABLE | — | Docs.
c252294d | feat: remove anti-distillation code | GAP (minor) | src/constants/betas.ts:30, src/utils/betas.ts:286-291 | Openclaude still has SUMMARIZE_CONNECTOR_TEXT_BETA_HEADER sending `summarize-connector-text-2026-03-13` beta header to API. CCB identified this as anti-distillation and removed it. Harmless for z.ai (ignored), but dead code. Also: ANTI_DISTILLATION_CC flag enabled in bundle polyfill but the fake_tools code was already absent from openclaude's claude.ts.
d04e00fc | feat: adjust preflight check code | NOT_APPLICABLE | src/utils/preflightChecks.tsx | CCB removed react-compiler-runtime `_c` memoization from preflightChecks.tsx. Openclaude retains it — works from source with `react/compiler-runtime` available.
e48da395 | feat: fix WebSearch tool — Bing API adapter | GAP | src/tools/WebSearchTool/ | CCB added Bing Web Search API adapter (adapters/bingAdapter.ts ~200 LOC, adapters/apiAdapter.ts ~170 LOC) as serverless fallback when Anthropic API server-side search is unavailable. Openclaude's WebSearchTool uses browserNavigateAndGetHtml (browser automation) only — no API fallback. Browser-based search is slower and less reliable. Missing: adapters/bingAdapter.ts, adapters/apiAdapter.ts, adapters/types.ts, adapters/index.ts.
1f0a2e44 | feat: complete debug config | NOT_APPLICABLE | — | .vscode/launch.json + README.md + package.json. Dev tooling.
74e51e7e | feat: enable Remote Control (BRIDGE_MODE) | GAP | src/bridge/ | CCB implemented peerSessions.ts (cross-session messaging via bridge API, ~76 LOC) and webhookSanitizer.ts (secret redaction, ~60 LOC). Openclaude's peerSessions.ts is a stub (`export {}`) and webhookSanitizer.ts does not exist. Openclaude has remoteControlServer command but bridge peer messaging layer is missing.
1d38eae5 | fix: CodeRabbit review — webhookSanitizer/peerSessions | GAP | — | Fixes to files that don't exist in openclaude (subsumed by 74e51e7e gap).
8645d37b | fix: add Authorization header to peer messages | GAP | src/bridge/peerSessions.ts:1 | Openclaude's peerSessions.ts is a stub. CCB added getBridgeAccessToken() Bearer auth. Subsumed by 74e51e7e gap.
e784f231 | fix: validate and encode target sessionId in peer messages | GAP | src/bridge/peerSessions.ts:1 | Openclaude's peerSessions.ts is a stub. CCB added validateBridgeId() + URL-encode compatTarget. Subsumed by 74e51e7e gap.
11951859 | feat: update sentry error reporting | ALREADY_HAVE | src/utils/sentry.ts | Openclaude has telemetry stubbed (src/services/analytics/). Sentry auto-disabled. CCB's version integrates Sentry for error tracking; openclaude intentionally does not.
e32c159f | feat: disable auto-update | ALREADY_HAVE | src/utils/config.ts | Openclaude has its own auto-updater using GitHub Releases API. CCB disabled Anthropic's npm/GCS updater via config.ts. Same intent, different mechanism.
78144b4d | feat: disable Datadog logging | ALREADY_HAVE | src/services/analytics/datadog.ts | Openclaude already has telemetry stubbed. Datadog disabled.
e74c009e | feat: GrowthBook custom server adapter | ALREADY_HAVE | src/services/analytics/growthbook.ts | Openclaude disables GrowthBook (returns defaults). CCB added custom adapter for self-hosted GrowthBook. Both achieve "no upstream GrowthBook calls" but via different paths.
5278ce1f | docs: two new docs | NOT_APPLICABLE | — | Docs.
8e4aea45 | docs: maintain two new docs | NOT_APPLICABLE | — | Docs.
67caa5d0 | docs: Remote Control entry to DEV-LOG | NOT_APPLICABLE | — | Docs.
cb046b4d | docs: add docs | NOT_APPLICABLE | — | Docs.
e944633d | fix: getAntModels is not defined | ALREADY_HAVE | src/utils/model/modelOptions.ts:2 | Openclaude already imports `{ getAntModels } from './antModels.js'`. Fix already present.
a02a9fc4 | fix: definition import missing | GAP (minor) | src/components/PromptInput/PromptInputFooterLeftSide.tsx:365 | CCB added `typeof TungstenPill === 'function'` guard before rendering TungstenPill. Openclaude uses `"external" === 'ant'` literal (DCE'd to false). Minor — TungstenPill never renders in openclaude (not needed).
a7604f65 | feat: /login custom anthropic terminal login | ALREADY_HAVE | src/components/ConsoleOAuthFlow.tsx | Openclaude already has full /login with provider picker (z.ai, DeepSeek, Anthropic, NIM) via commands/login/providerPicker.tsx. CCB's "Custom Platform" option is superset of functionality openclaude already has.
7935bfb4 | fix: fix debug startup method | NOT_APPLICABLE | — | package.json + README.md. Dev tooling.
99111949 | refactor(buddy): align companion system with official CLI | ALREADY_HAVE | src/buddy/ | Openclaude has full buddy implementation (CompanionSprite.tsx, observer.ts, useBuddyNotification.tsx, etc.). CCB's 7-file refactor added CompanionCard.tsx + companionReact.ts — openclaude has equivalent via different components.
c9c14c81 | feat: simplify debug method | NOT_APPLICABLE | — | Dev scripts only.
7d4adce1 | fix(buddy): CodeRabbit review — type fixes | NOT_APPLICABLE | — | Fixed buddy.ts return type + CompanionCard.tsx stat clamp. Openclaude buddy uses different implementation — not applicable.
9dd180dc | Merge branch pr/amDosion/82 | NOT_APPLICABLE | — | Merge commit.
e74d1f08 | fix(buddy): second round CodeRabbit — unsafe cast + JSON parse | NOT_APPLICABLE | — | Falls under same buddy refactor as above. Not applicable to openclaude's buddy.
cf44cc32 | Merge branch pr/amDosion/60 | NOT_APPLICABLE | — | Merge commit.
5a7d06fe | Merge PR #82 — refactor buddy | NOT_APPLICABLE | — | Merge of already-assessed buddy changes.
7e888ce3 | feat: add test agent + docs | NOT_APPLICABLE | — | .claude/agents/ + README_EN.md. Docs + sample agent.
a6bef451 | fix: fix rg file passing | NOT_APPLICABLE | — | Build (ripgrep download script). Openclaude doesn't bundle ripgrep this way.
4c5a1222 | docs: adjust docs | NOT_APPLICABLE | — | Docs.
eb86e340 | Merge PR #88 — enable schedule remote agents | NOT_APPLICABLE | — | Merge commit.
2cc626c1 | fix: fix test files | NOT_APPLICABLE | — | Test.
4a9e9185 | docs: update docs | NOT_APPLICABLE | — | Docs.
9e6fe9b4 | feat: add discord group | NOT_APPLICABLE | — | Social/community, not source.
29db9d99 | docs: make text better | NOT_APPLICABLE | — | Docs.
7ae94327 | feat: enable /voice mode with native audio binaries | ALREADY_HAVE | src/services/voice.ts, src/utils/voiceLocal/ | Openclaude has voice via faster-whisper local STT (src/utils/voiceLocal/). CCB added native audio-capture .node binaries. Different approach — both achieve voice input. Openclaude's audio-capture-napi is stubbed because voice capture is handled by faster-whisper's Python worker, not native .node.
6738a761 | feat: enable Claude in Chrome MCP | ALREADY_HAVE | src/utils/browserMcp/setup.ts | Openclaude uses zendriver-mcp for browser automation (auto-installs from coffeegrind123/Zendriver-MCP-fork). CCB implemented the official @ant/claude-for-chrome-mcp. Different browser MCP backend, same capability.
465e9f01 | test: coverage for formatRelativeTimeAgo + formatLogMetadata | NOT_APPLICABLE | — | Test.
e3264a16 | feat: enable Computer Use with multi-platform support | ALREADY_HAVE | src/utils/computerUse/ | Openclaude has computer-use-mcp (domdomegg) auto-installed. CCB ported @ant/computer-use-mcp with Linux backends. Different implementations — openclaude uses domdomegg's well-maintained package.
00b044e8 | feat: OpenAI Chat compatible protocol (#99) | GAP | src/services/api/openaiBridge/ | CCB added full OpenAI Chat API compatibility layer (services/api/openai/ — client.ts, convertMessages.ts, convertTools.ts, streamAdapter.ts, modelMapping.ts ~1,200 LOC total). Openclaude has NVIDIA NIM bridge (openaiBridge/) which translates Anthropic→OpenAI specifically for NIM + OpenRouter. CCB's version is a generic OpenAI-compatible provider adapter. Openclaude's NIM bridge covers the same use case for NIM/OpenRouter but lacks generic OpenAI provider support (e.g., raw OpenAI, Groq, Together without OpenRouter).
fdb2442a | test: coverage for toRelativePath + getDirectoryForPath | NOT_APPLICABLE | — | Test.
4c0b2aae | feat: bypass Claude Code account requirement | ALREADY_HAVE | src/main.tsx, src/commands.ts | Openclaude already bypasses account/OAuth requirements (CLAUDE_AUTO_TRUST=1, USER_TYPE=ant at entrypoint, showSetupScreens bypassed). CCB's bypass is redundant for openclaude.
3707c3c0 | feat: Windows Computer Use enhancement | NOT_APPLICABLE | — | Windows-specific (PrintWindow, UI Automation, OCR via win32 backends). Openclaude runs in Linux containers.
8cef1b6a | Merge remote-tracking branch amDosion/feat/enable-chrome-mcp | NOT_APPLICABLE | — | Merge commit.
8cb1a15c | Merge branch pr/amDosion/93 | NOT_APPLICABLE | — | Merge commit.
52d8b83b | docs: update README | NOT_APPLICABLE | — | Docs.
ca086b04 | fix: Windows Computer Use request_access + screenshot errors | NOT_APPLICABLE | — | Windows-specific fix (swiftLoader.ts, executor.ts for win32).
13146509 | Merge branch pr/amDosion/92 | NOT_APPLICABLE | — | Merge commit.
86d2c8f9 | Merge remote-tracking branch amDosion/feat/computer-use-windows | NOT_APPLICABLE | — | Merge commit.
913702d9 | feat: built-in status line with usage quota display (#89) | ALREADY_HAVE | src/components/FuelgaugeStatusLine.tsx | Openclaude has FuelgaugeStatusLine.tsx (folder, branch, model, ctx-bar, 5h-bar, 7d-bar). CCB added BuiltinStatusLine.tsx with usage quota display. Different implementation, same capability.
a67b4a40 | docs: update latest instructions | NOT_APPLICABLE | — | Docs.
c9f95fc3 | claude-code with OpenAI mode fix | NOT_APPLICABLE | — | Full-file write of project scaffolding (CLAUDE.md, biome.json, .github/, build.ts, etc.). Not a source change — configuration/bootstrap files.

# Summary
Total commits analyzed: 82
- NOT_APPLICABLE: 56 (docs, tests, merges, chores, build, Windows-specific, dev tooling)
- ALREADY_HAVE: 19
- GAP: 7

# GAPs requiring attention (priority order):

1. **2e4d6e21** — Sandbox hook command execution (HIGH)
   Openclaude hooks.ts execCommandHook does NOT wrap hook shell commands with sandbox. Hooks execute arbitrary commands from settings.json and could exfiltrate data via curl/wget. CCB added SandboxManager.wrapWithSandbox() with network-only restrictions.

2. **e48da395** — Bing WebSearch API adapter (MEDIUM)
   Openclaude WebSearchTool relies solely on browser automation (browserNavigateAndGetHtml). CCB added a Bing API adapter as fast serverless fallback. Missing: adapters/bingAdapter.ts, adapters/apiAdapter.ts, adapters/types.ts, adapters/index.ts (~500 LOC total).

3. **74e51e7e** — Remote Control peer sessions + webhook sanitizer (MEDIUM)
   Openclaude's src/bridge/peerSessions.ts is an empty stub. webhookSanitizer.ts does not exist. CCB implemented cross-session bridge messaging and secret redaction for webhook payloads.

4. **00b044e8** — Generic OpenAI Chat compatibility (LOW-MEDIUM)
   Openclaude has NIM bridge only. CCB added generic OpenAI-compatible adapter (client.ts, convertMessages.ts, convertTools.ts, streamAdapter.ts, modelMapping.ts). NIM bridge covers NIM + OpenRouter; doesn't cover raw OpenAI/Groq/Together.

5. **c252294d** — SUMMARIZE_CONNECTOR_TEXT anti-distill beta header (LOW)
   Openclaude still sends `summarize-connector-text-2026-03-13` beta header. CCB removed it as anti-distillation. Harmless for z.ai but dead code on non-Anthropic endpoints.

6. **4ab4506d** — computeTtftText undefined in compiled binary (LOW)
   Spinner.tsx uses computeTtftText which is a bundler-injected global. Works from Bun source but may fail in compiled binary if react-compiler-runtime isn't in the bundle.

7. **a02a9fc4** — TungstenPill typeof guard (TRIVIAL)
   PromptInputFooterLeftSide.tsx uses `"external" === 'ant'` literal (always false) and lacks typeof guard. Not harmful since branch is DCE'd, but CCB's pattern is cleaner.
