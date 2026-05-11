# Gitlawb Gap Analysis — Batch 1 (commits 1–73)

## Classification

619b5fb | feat: add OpenAI-compatible provider shim | NOT_APPLICABLE | N/A | openclaude has own OpenAI bridge at src/services/api/openaiBridge/. Entirely different architecture (protocol translation vs shim layer).
fd10824 | docs: rewrite README | NOT_APPLICABLE | N/A | Documentation only.
3e652ca | feat: add build system, stubs, and npm packaging | NOT_APPLICABLE | N/A | New repo bootstrap — package.json, stubs, bun.lock. openclaude already has its own build system.
db04c3e | fix: bypass version gate by setting MACRO.VERSION to 99.0.0 | ALREADY_HAVE | scripts/build.ts:52 | openclaude doesn't have scripts/build.ts but its CLI entrypoint handles version gate differently via CLAUDE_AUTO_TRUST + USER_TYPE=ant pattern.
651335f | fix: skip auth and onboarding for OpenAI provider | ALREADY_HAVE | src/interactiveHelpers.tsx:105 | openclaude's showSetupScreens returns early via isEnvTruthy(process.env.CLAUDE_AUTO_TRUST) — broader bypass, same effect. openclaude's isAnthropicAuthEnabled already handles 3P providers.
747be9c | fix: restore interactive OpenAI REPL startup | NOT_APPLICABLE | N/A | React 18 patching of Ink + auto-bind dependency. openclaude runs React 19 with different Ink integration.
009c29d | refactor: update import paths for react/compiler-runtime | NOT_APPLICABLE | N/A | Gitlawb-specific import path changes + PLAYBOOK.md + provider bootstrap scripts. Not in openclaude's source tree.
e69cf09 | feat: enhance provider-launch script | NOT_APPLICABLE | N/A | scripts/provider-launch.ts — not in openclaude.
770e16d | fix: restore interactive OpenAI REPL on React 18 | NOT_APPLICABLE | N/A | React 18 compat: StatusNotices, ThemedBox, Box, ErrorOverview patching for React 18 Ink reconciler. openclaude uses React 19.
958f8c1 | chore: publish @gitlawb/openclaude package | NOT_APPLICABLE | N/A | npm version bump only.
ba5e1f0 | fix: suppress OpenAI startup warning and account banner | NOT_APPLICABLE | N/A | Gitlawb-specific — adds isOpenAI check to LogoV2 + client.ts banner suppression. openclaude uses its own notice system.
c957d49 | fix: prevent interactive stream crash on node removal | GAP | src/ink/dom.ts:230 | See GAPs section below.
752c71c | feat: add native Ollama provider | NOT_APPLICABLE | N/A | Python files only (ollama_provider.py, test_ollama_provider.py). Not relevant to TS codebase.
6b163e2 | feat: add intelligent smart auto-router | NOT_APPLICABLE | N/A | Python files only (smart_router.py, test_smart_router.py).
5eb7ab4 | Merge #1 (Ollama provider) | NOT_APPLICABLE | N/A | Merge commit.
55098bf | Merge #2 (smart auto-router) | NOT_APPLICABLE | N/A | Merge commit.
2d7aa9c | feat: rebrand as Open Claude and harden OpenAI REPL | NOT_APPLICABLE | N/A | Gitlawb branding changes (Clawd.tsx, CondensedLogo.tsx, WelcomeV2.tsx). openclaude has its own branding.
174eb8a | feat: add intelligent provider profile recommendation | NOT_APPLICABLE | N/A | New Gitlawb-specific system (providerRecommendation.ts + scripts). Not in openclaude.
8fe03cb | fix: harden provider recommendation safety | NOT_APPLICABLE | N/A | Gitlawb provider-profile system hardening. Not in openclaude.
d126739 | fix: resolve frozen terminal for OpenAI/3P provider users (#3) | NOT_APPLICABLE | N/A | Gitlawb's showSetupScreens restructured to skip UI but keep state-init. openclaude bypasses setup screens entirely via CLAUDE_AUTO_TRUST=1 — different approach, same effect.
4ce7dcf | fix: support Windows launcher import paths | NOT_APPLICABLE | N/A | Windows-specific bin/openclaude ESM import fix. openclaude targets Linux/Docker.
0a5827c | fix(openai-shim): preserve final streaming usage chunks | NOT_APPLICABLE | N/A | Gitlawb's openaiShim.ts. openclaude has own streamTranslator.ts — different codebase.
cbeed0f | Add Codex plan/spark provider support | NOT_APPLICABLE | N/A | New Codex shim (740 LOC) + Codex-specific changes to provider scripts. Not in openclaude.
6cf95f5 | fix: show actual OpenAI model name in welcome screen UI | NOT_APPLICABLE | N/A | Gitlawb-specific — adds OpenAI provider check to getPublicModelDisplayName + getDefaultMainLoopModelSetting. openclaude uses its own provider detection via getAPIProvider() in openaiBridge/index.ts.
cb24750 | security: remove runtime require of unverified modifiers-napi package | GAP | src/utils/modifiers.ts:17,34 | See GAPs section below.
5175dba | fix: stub internal-only modules in open build | NOT_APPLICABLE | N/A | Build script changes only.
b7bc3f3 | Merge #9 | NOT_APPLICABLE | N/A | Merge commit.
b16d46d | Merge #10 | NOT_APPLICABLE | N/A | Merge commit.
2e70fa1 | Merge #11 | NOT_APPLICABLE | N/A | Merge commit.
833c90f | Merge #12 | NOT_APPLICABLE | N/A | Merge commit.
24f1b52 | Merge #14 | NOT_APPLICABLE | N/A | Merge commit.
c1317ef | Merge #16 | NOT_APPLICABLE | N/A | Merge commit.
9ee20cf | fix: preserve tui styles while fixing freeze | NOT_APPLICABLE | N/A | React 18 reconciler refactor — changes shouldUpdate from returning boolean to returning UpdatePayload | null. openclaude uses React 19 (commitUpdate receives old/new props directly per comment at reconciler.ts:425). NOT_APPLICABLE.
2ee43e0 | Fix Windows ESM import by using file URL | NOT_APPLICABLE | N/A | Windows-specific bin/openclaude launcher fix. openclaude targets Linux/Docker.
6b64070 | Merge #17 | NOT_APPLICABLE | N/A | Merge commit.
f51cd3a | Merge origin/main into codex/provider-profile-recommendations | NOT_APPLICABLE | N/A | Merge commit.
a3d8ab0 | feat: add native Gemini provider | NOT_APPLICABLE | N/A | Gitlawb-specific Gemini provider integration into their openaiShim. openclaude uses its own provider bridge architecture.
e7c600d | chore: release 0.1.4 | NOT_APPLICABLE | N/A | Version bump only.
4ca94b2 | feat: add context window guard for OpenAI-compatible models | NOT_APPLICABLE | N/A | Adds openaiContextWindows.ts with context window sizes for 30+ models. openclaude has its own context window handling via getContextWindowForModel + NIM model catalog.
1431522 | Merge #19 | NOT_APPLICABLE | N/A | Merge commit.
cb86f73 | fix: prevent duplicate responses in OpenAI streaming | NOT_APPLICABLE | N/A | Fixes Gitlawb's openaiShim.ts stream handler. openclaude has own streamTranslator.ts.
0192dc0 | Merge #21 | NOT_APPLICABLE | N/A | Merge commit.
ce45bd0 | Merge origin/main into provider-profile-recommendations | NOT_APPLICABLE | N/A | Merge commit.
99543a2 | fix: correct double-slash in import path for structuredIO | GAP | src/cli/structuredIO.ts:7 | See GAPs section below.
598f59e | fix: map tool_choice 'none' in OpenAI shim | NOT_APPLICABLE | N/A | Gitlawb's openaiShim.ts tool_choice mapping. openclaude has own requestTranslator.ts.
11a3553 | Merge #5 | NOT_APPLICABLE | N/A | Merge commit.
fd5e954 | fix: restrict .openclaude-profile.json permissions to owner-only (0600) | NOT_APPLICABLE | N/A | Gitlawb-specific profile file (.openclaude-profile.json). openclaude doesn't have this file.
00744a8 | Merge #31 | NOT_APPLICABLE | N/A | Merge commit.
dda553e | fix: define MACRO.PACKAGE_URL and MACRO.NATIVE_PACKAGE_URL in build | NOT_APPLICABLE | N/A | Gitlawb's scripts/build.ts define block. openclaude doesn't have this build script and uses its own build pipeline.
7ef085c | test: cover deepseek max token limits | NOT_APPLICABLE | N/A | Tests for openaiContextWindows.ts — Gitlawb-specific file.
82e7168 | Merge #38 | NOT_APPLICABLE | N/A | Merge commit.
1278967 | fix: skip Anthropic credential check in CI for 3P providers | GAP | src/utils/auth.ts:278-285,1746 | See GAPs section below.
8750f84 | Merge #44 | NOT_APPLICABLE | N/A | Merge commit.
20b4176 | docs: note minimum Bun version for Windows builds | NOT_APPLICABLE | N/A | Documentation only.
372ba31 | feat: enhance tool conversion to support strict mode | NOT_APPLICABLE | N/A | Codex-specific shim changes (codexShim.ts). Not in openclaude (uses own bridge).
a44f45e | first commit (README only) | NOT_APPLICABLE | N/A | README change only.
6c46974 | fix: normalize tool schemas so required contains properties for OpenAI/Codex | NOT_APPLICABLE | N/A | Gitlawb's openaiShim.ts + codexShim.ts schema normalization. openclaude's OpenAI bridge (requestTranslator.ts) handles schemas differently.
788cfa3 | fix: handle empty string delta.content in OpenAI streaming | NOT_APPLICABLE | N/A | Gitlawb's openaiShim.ts stream handler. openclaude's streamTranslator.ts handles this independently.
39d9616 | fix: update DeepSeek context window from 64k to 128k | NOT_APPLICABLE | N/A | Gitlawb's openaiContextWindows.ts. openclaude handles DeepSeek context windows via getContextWindowForModel in context.ts.
481e608 | fix: show OpenAI/Gemini provider info in /status panel | NOT_APPLICABLE | N/A | Gitlawb's status.tsx provider labels. openclaude has its own provider status handling.
409e90c | fix: use correct default port for wss:// in NO_PROXY matching | GAP | src/utils/proxy.ts:100 | See GAPs section below.
65af739 | improved startup screen | NOT_APPLICABLE | N/A | UI/branding changes (Clawd.tsx, CondensedLogo.tsx, LogoV2.tsx). openclaude has its own branding.
58009bc | removed unnecessary changes | NOT_APPLICABLE | N/A | README only.
5a3573f | Merge #54 | NOT_APPLICABLE | N/A | Merge commit.
c3db3d8 | fix: add CLAUDE_CODE_USE_GEMINI to is3P check in isAnthropicAuthEnabled | NOT_APPLICABLE | N/A | Gitlawb's Gemini auth integration. openclaude doesn't use CLAUDE_CODE_USE_GEMINI.
b8ea6f8 | Merge #56 | NOT_APPLICABLE | N/A | Merge commit.
c8a780a | fix: follow up Codex launcher and input handling | GAP | src/ink/render-node-to-output.ts:717,966,1017,1294,1341,1348,1375,1427,1479 | See GAPs section below.
8da5614 | Merge #57 | NOT_APPLICABLE | N/A | Merge commit.
29493bd | test: cover gpt-4o max token limits | NOT_APPLICABLE | N/A | Tests for Gitlawb's openaiContextWindows.ts.
5f774cf | Merge #47 | NOT_APPLICABLE | N/A | Merge commit.
f0f6f1b | test: add GPT-5.4 token coverage | NOT_APPLICABLE | N/A | Tests for Gitlawb's openaiContextWindows.ts + adds GPT-5.4 to context windows.
6c35f4e | fix: guard transcript sandbox subscription | GAP | src/components/SandboxViolationExpandedView.tsx:35-36 | See GAPs section below.
c3ddc83 | fix: type PrBadge props | NOT_APPLICABLE | N/A | Compiled React Compiler output — both repos have compiled code. The type annotation on the source-level signature doesn't change compiled behavior.

## Summary
Total: 73. GAP: 7, ALREADY_HAVE: 2, NOT_APPLICABLE: 64.

### GAPs found:
1. **c957d49** — `src/ink/dom.ts:230`: `collectRemovedRects()` crashes when `removed` is null/undefined. Gitlawb fix adds `if (!removed || removed.nodeName === '#text') return` null-check, uses `?.` optional chaining for `elem.style?.position`, and guards `elem.childNodes` iteration with `Array.isArray`. OC file: src/ink/dom.ts line 230. Fix: add null-guard on `removed` param, convert `elem.style.position` to `elem.style?.position`, guard `childNodes` iteration.

2. **cb24750** — `src/utils/modifiers.ts:17,34`: Supply-chain security — `require('modifiers-napi')` still executes at runtime in openclaude. The `modifiers-napi` package is Anthropic-internal and a same-named npm package could be a supply chain attack vector. Gitlawb fix replaces both functions with safe no-ops (modifier key detection not needed in open-source build). OC file: src/utils/modifiers.ts lines 16-17, 32-34. Fix: replace both `require('modifiers-napi')` calls with no-ops (prewarmModifiers as no-op, isModifierPressed always returns false).

3. **99543a2** — `src/cli/structuredIO.ts:7`: Import path contains double-slash `'src//types/message.js'` which may cause unpredictable module resolution. Gitlawb fix: change to `'src/types/message.js'`. OC file: src/cli/structuredIO.ts line 7. Fix: remove double-slash.

4. **409e90c** — `src/utils/proxy.ts:100`: Default port resolution for NO_PROXY matching assigns port 80 to non-https protocols including `wss://` (should be 443). Gitlawb fix: `url.protocol === 'https:' || url.protocol === 'wss:' ? '443' : '80'`. OC file: src/utils/proxy.ts line 100. Fix: add `wss:` to the 443-branch of the port resolution ternary.

5. **1278967** — `src/utils/auth.ts:278-285,1746`: (a) `getAnthropicApiKeyWithSource()` at lines 278-285 throws `ANTHROPIC_API_KEY or CLAUDE_CODE_OAUTH_TOKEN env var is required` in CI mode without checking if a 3P provider is active. Gitlawb fix: adds `!isUsing3PServices() &&` guard before the throw. (b) `isUsing3PServices()` at line 1746 only checks Bedrock/Vertex/Foundry — misses new providers. OC file: src/utils/auth.ts lines 278-285, 1746-1751. Fix: add `!isUsing3PServices()` guard before the CI credential throw, extend `isUsing3PServices()` to cover all non-Anthropic providers used by openclaude (z.ai, DeepSeek, NIM, etc.).

6. **6c35f4e** — `src/components/SandboxViolationExpandedView.tsx:35-36`: `useEffect` callback calls `store.subscribe()` without null-checking `store` first. When sandboxing is disabled or on Linux, `getSandboxViolationStore()` may return null, causing `Cannot read properties of null (reading 'subscribe')`. Gitlawb fix: adds early-return guards inside useEffect before accessing store. OC file: src/components/SandboxViolationExpandedView.tsx lines 35-36. Fix: add `if (!store || typeof store.subscribe !== 'function') return;` after `getSandboxViolationStore()` call, and move the `!isSandboxingEnabled() || getPlatform() === "linux"` check inside the useEffect callback.

7. **c8a780a** — `src/ink/render-node-to-output.ts:717,966,1017,1294,1341,1348,1375,1427,1479`: Unsafe `as DOMElement` casts throughout without checking node types. The Gitlawb fix adds `isElementNode()` type guard and uses it before accessing `yogaNode`/`dirty`/etc. This prevents crashes when a text node or undefined slips into childNodes iteration. OC file: src/ink/render-node-to-output.ts at 9 locations with `as DOMElement` casts. Fix: add `isElementNode` helper (same as Gitlawb's) and use it to guard all `as DOMElement` casts in childNodes iteration.
