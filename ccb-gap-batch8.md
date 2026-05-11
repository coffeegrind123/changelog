# CCB Batch 8 Gap Analysis (commits 575-648)

## Summary

| SHA | SUBJECT | VERDICT | OC_FILE:LINE | NOTES |
|-----|---------|---------|-------------|-------|
| 5c107e5f | Merge #416 (subagent-fork-render) | NOT_APPLICABLE | — | Merge commit |
| fd66ddc4 | docs: expand sub-agent architecture guide | NOT_APPLICABLE | — | Documentation only |
| 941bcbd2 | fix: third-party API user_id validation error (DeepSeek, etc.) | GAP | src/services/api/claude.ts:568-575 | OC `getAPIMetadata()` always sends full JSON user_id (device_id+account_uuid+session_id). CCB sends only device_id hex for third-party providers (non api.anthropic.com) because those validate against ^[a-zA-Z0-9_-]+$. OC users on DeepSeek/z.ai may see user_id validation errors. |
| 9e299a72 | Merge #420 (third-party user_id) | NOT_APPLICABLE | — | Merge commit |
| 68c7ebb2 | Merge #419 (sub-agents docs) | NOT_APPLICABLE | — | Merge commit |
| 2f150d3e | feat: status line refreshInterval | ALREADY_HAVE | src/components/StatusLine.tsx:355-363 | OC already has refreshInterval support with setInterval + doUpdate in useEffect. Zod schema field already present in types.ts. |
| c7efac6b | Merge #423 (statusline refresh) | NOT_APPLICABLE | — | Merge commit |
| 12f5aedf | fix: restore diff highlight rendering | ALREADY_HAVE | src/tools/FileEditTool/UI.tsx:15-23 | OC already imports StructuredDiffList, adjustHunkLineNumbers, readEditContext, findActualString, getPatchForEdit — full diff highlight rendering present. FileEditToolUpdatedMessage has structuredPatch + fileContent props. |
| 8cfe9b6d | feat: enable COORDINATOR_MODE feature flag | ALREADY_HAVE | node_modules/bundle/index.js | OC enables all 87 feature flags via bundle polyfill — no defines.ts gating needed. |
| 58953621 | chore: 2.2.0 | NOT_APPLICABLE | — | Version bump only |
| 958ac3a0 | feat: enable some closed features (UDS_INBOX, LAN_PIPES, EXPERIMENTAL_SKILL_SEARCH) | ALREADY_HAVE | node_modules/bundle/index.js | OC enables all features via bundle polyfill; FORK_SUBAGENT already implemented. |
| e8759f34 | fix: disable opus[1m] auto migration | GAP | src/migrations/migrateOpusToOpus1m.ts:24-44 | OC still has old migration logic that forces opus→opus[1m]. CCB makes it a no-op to respect user manual model choice. OC should adopt the no-op to avoid overriding user-specified models. |
| e3c0699f | feat: prompt cache hit rate detection and warning | GAP | — | OC has no cacheWarning.ts, no shouldShowCacheWarning, no createCacheWarningMessage, no cache hit rate display in ContextVisualization, no cache warning yield in query.ts:1234. New feature needs full port. |
| 771e3dbc | fix: non-Anthropic provider attribution model name error | GAP | — | OC has no attributionModel.ts. CCB's getRealModelName() checks provider-specific env vars (OPENAI_MODEL, GEMINI_MODEL, GROK_MODEL). OC would show wrong model name in attribution for non-Anthropic providers. |
| f7f69b75 | fix: model alias resolution showing "haiku" instead of real model name | GAP | — | OC has no attributionModel.ts. CCB removes getUserSpecifiedModelSetting() branch and unifies through getMainLoopModel()+resolveProviderModel(). |
| cb4a6e76 | feat: auto email mapping and attribution system | NOT_APPLICABLE | — | CCB-specific: attributionEmail.ts, PRODUCT_URL to CCB fork, attribution system for their fork branding |
| c43efecb | feat: attribution email to GitHub noreply format | NOT_APPLICABLE | — | CCB-specific: their attribution email mapping |
| aa06cea9 | fix: GLM model GitHub attribution email to zai-org | NOT_APPLICABLE | — | CCB-specific: their email mapping for GLM models |
| 7fe448d9 | feat: use ccb email | NOT_APPLICABLE | — | CCB-specific: their attribution email |
| 4230f0ff | chore: remove learn directory | NOT_APPLICABLE | — | Chore |
| 2fdfb844 | Merge #428 | NOT_APPLICABLE | — | Merge commit |
| 73e54d4b | chore: 2.2.1 | NOT_APPLICABLE | — | Version bump |
| 8ba51ede | fix: conditional hooks "Rendered fewer hooks than expected" error | GAP | src/screens/REPL.tsx, src/components/PromptInput/*.tsx | OC has some conditional hook patterns (feature('X') ? useHook() : default) that violate React rules. CCB moves ALL hook calls to unconditional top-level with value gating. OC has ~4 instances found; full audit needed across all components. |
| 02dd7967 | Merge #435 (conditional hooks) | NOT_APPLICABLE | — | Merge commit |
| c7cb3d8f | feat: /login support codex subscription login | NOT_APPLICABLE | — | CCB-specific: ChatGPT/codex subscription OAuth flow (chatgptAuth.ts, responsesAdapter.ts). OC uses z.ai/DeepSeek, not ChatGPT/Codex. |
| 7be08f53 | feat: Tool Search infrastructure (CORE_TOOLS whitelist + TF-IDF index + ExecuteTool + search) | GAP | — | OC has no services/toolSearch/ directory, no CORE_TOOLS whitelist, no ExecuteTool, no TF-IDF toolIndex. OC's existing tool deferral uses native tool_reference blocks (first-party Anthropic only) + text markers for third-party. CCB replaces all of that with a unified provider-agnostic system. Major feature diff. |
| 4fc95bd5 | feat: Remote Control conditional tool injection | GAP | — | CCB adds isBridgeEnabled() gates to PushNotificationTool/SendUserFileTool/BriefTool/ExecuteTool. OC has these tools but no bridge-gated isEnabled(). Also removes firstParty base URL check from toolSearch. |
| 8c157f07 | refactor: unified Tool Search — remove tool_reference/defer_loading | GAP | — | CCB removes all tool_reference/defer_loading dependency, renames ExecuteTool→ExecuteExtraTool, makes ToolSearchTool output pure text. OC still uses deferred tool tool_reference blocks (first-party path) and text markers (third-party path) in ToolSearchTool. System prompt simplified from ~120 lines to ~10 lines for tool guidance. |
| c14b7ead | fix: Tool Search cache invalidation — deferred tools no longer dynamically injected | GAP | — | CCB stabilizes tools[] array (only core+ToolSearch+ExecuteExtraTool), prevents prompt cache breakage from tool list changes. OC's current approach (adding discovered tools to tools[]) would cause cache misses. |
| 3ac866be | fix: cache hit rate warning messages not showing (system type bypass isMeta filter) | GAP | — | Part of e3c0699f (cacheWarning). OC has no cacheWarning.ts at all. |
| af0d7dc8 | feat: Agents/Teams tools into Tool Search on-demand discovery | GAP | — | CCB moves TeamCreate/TeamDelete/SendMessage from CORE_TOOLS to deferred (ToolSearch). OC doesn't have this architecture. SendMessage always loaded in swarm mode. |
| b52c10dd | fix: CI format check failure | NOT_APPLICABLE | — | CI only |
| bd225384 | refactor: Tool Search directory rename + prompt strengthen | GAP | — | CCB renames toolSearch/→searchExtraTools/, ToolSearchTool→SearchExtraToolsTool. OC doesn't have these modules. |
| 2cf18c4c | docs: ToolSearch design guide + disable turn-zero tool recommendation popup | GAP | — | CCB disables getTurnZeroSearchExtraToolsPrefetch (eliminates frequent popups on user input). OC's skillSearch prefetch might have the same popup issue. |
| 547ce9e8 | fix: prefetch test — turn-zero recommendation disabled | NOT_APPLICABLE | — | Test update only |
| 2f86485d | refactor: slim system prompt — merge sections, trim memory/tool desc, truncate gitStatus | GAP | src/constants/prompts.ts, src/context.ts:424, src/memdir/memoryTypes.ts | CCB reduces gitStatus MAX_STATUS_CHARS from 2000 to 1000, removes detailed auto-memory type descriptions, deletes forkExamples/currentExamples from Agent tool prompt, merges outputEfficiency+toneStyle sections. OC still has verbose prompts. Token savings for low-context-mode providers. |
| df8c4f4b | Merge #438 (codex subscription) | NOT_APPLICABLE | — | Merge commit |
| 7e2b8e81 | Merge #442 (tool_search) | NOT_APPLICABLE | — | Merge commit |
| 84f12f34 | fix: elevate CLAUDE.md instruction weight — independent project-instructions + deferred tools position | GAP | src/utils/api.ts:451-475, src/services/api/claude.ts:1407-1412 | OC's prependUserContext still wraps claudeMd inside generic <system-reminder> with "may or may not be relevant" disclaimer, degrading instruction weight. CCB extracts claudeMd as separate <project-instructions> message at messages[0]. Also moves deferred tools from prepend to append (so they don't steal position 0). |
| 07072849 | docs: update CLAUDE.md | NOT_APPLICABLE | — | Documentation only |
| 2006ab25 | fix: React Error Boundary — prevent production rendering crashes | GAP | src/components/SentryErrorBoundary.ts:17-23 | OC's ErrorBoundary returns null on error (silent failure). CCB's enhanced version: outputs diagnostic info to stderr + renders error Box with message in UI + wraps Messages + replLauncher. OC crash = blank screen with no diagnostics. |
| eebda578 | chore: CI config, codecov, test mock | NOT_APPLICABLE | — | CI/test infrastructure only |
| b8d86e52 | feat: Local Vault encrypted storage service | NOT_APPLICABLE | — | New feature (CCB-specific): AES-256-GCM vault with OS keychain + scrypt KDF. Not a fix/backport. Could port if needed. |
| a2ea69c0 | feat: Session Memory multi-store support | NOT_APPLICABLE | — | New feature (CCB-specific): multi-store local memory under ~/.claude/local-memory/. No OC equivalent. Could port if needed. |
| 5bb0306d | feat: LocalMemoryRecallTool and VaultHttpFetchTool | NOT_APPLICABLE | — | New feature (CCB-specific): cross-session local note recall + authenticated HTTP fetch with vault keys. No OC equivalent. Could port if needed. |
| ee63c176 | feat: login auth enhancement (workspace key, host guard, auth status) | NOT_APPLICABLE | — | CCB-specific: workspace API key guard + OAuth subscription plane + AuthPlaneSummary/WorkspaceKeyInput UI. OC's auth is z.ai/DeepSeek token-based, not Anthropic OAuth. |
| 2437040b | feat: cloud management commands (/memory-stores, /vault, /schedule, /skill-store, /agents-platform) | NOT_APPLICABLE | — | CCB-specific: cloud commands depending on CCB cloud backend. Not applicable to OC. |
| 4f0aa861 | feat: local Memory/Vault management commands (/local-memory, /local-vault) | NOT_APPLICABLE | — | CCB-specific: local commands for CCB's vault/memory system. Not in OC. |
| 6766f08e | feat: GitHub integration commands (/issue, /share, /autofix-pr) | NOT_APPLICABLE | — | New feature (CCB-specific): gh CLI wrappers. OC has separate GitHub integration (team memory backend) but not these commands. Could port if needed. |
| fdddb6db | feat: utility commands (/teleport, /recap, /break-cache, /env, /tui) | NOT_APPLICABLE | — | New features (CCB-specific): teleport from claude.ai, session recap, prompt cache management, env info display. OC has some via different paths. |
| efaf4afd | feat: Provider Registry, StatusLine, Cache Stats, and other enhancements | NOT_APPLICABLE | — | Large feature package: providerRegistry/, cacheStats.ts, BuiltinStatusLine, ultrareviewPreflight, MagicDocs. New subsystems not in OC. Could port individual pieces if needed. |
| 6a182e45 | feat: register all new commands to command system and tool registry | NOT_APPLICABLE | — | Wiring for the new commands/tools from preceding commits (efaf4afd etc.). Not applicable on its own. |
| 4f493c83 | chore: remove deprecated ctx_viz type declarations | NOT_APPLICABLE | — | Chore |
| 82be5ff0 | fix: code review fixes — security, performance, correctness | NOT_APPLICABLE | — | Fixes in CCB-specific files (local-vault, schedule, vault, skill-store, share) not present in OC. |
| 66b49d70 | chore: 2.3.0 | NOT_APPLICABLE | — | Version bump |
| 8fccd323 | fix: sanitize probe-subscription-endpoints API base URL in logs | NOT_APPLICABLE | — | Script only: scripts/probe-subscription-endpoints.ts. OC may not have this script; fix is to truncate URL to origin only in log output. |
| 80d4e095 | fix: setupAxiosMock multi-test file concurrency mock loss | NOT_APPLICABLE | — | Test infrastructure only: tests/mocks/axios.ts. OC uses Bun test runner with different mock infrastructure. |
| 5c499d31 | fix: further sanitize probe-subscription-endpoints orgUUID in logs | NOT_APPLICABLE | — | Script only: truncate orgUUID from 8 chars to 4 chars in log output. |
| 3f0f699c | Merge #445 (many-feature-package) | NOT_APPLICABLE | — | Merge commit |
| 998890b4 | Merge #446 (prompt-cut-down) | NOT_APPLICABLE | — | Merge commit |
| dc3d3e88 | fix: remove auto mode provider and model whitelist | GAP | src/utils/betas.ts:160-195 | OC's modelSupportsAutoMode still has: firstParty-only gate (line 166), GrowthBook allowModels override, USER_TYPE=ant denylist (blocks claude-3-* and old claude-4), external allowlist (only claude-(opus\|sonnet)-4-6). CCB removes ALL of this and just returns feature('TRANSCRIPT_CLASSIFIER') ? true : false — auto mode works on ANY model/provider. Since OC uses z.ai/DeepSeek (non-firstParty), auto mode is effectively disabled by line 166. |
| 6e1d3d8f | fix: fix feature usage issue | GAP | src/utils/betas.ts:160 | Minor variant of dc3d3e88 — CCB adds `? true : false` ternary to modelSupportsAutoMode. OC doesn't have this change (still has full whitelist logic). |
| 0ce8f7a1 | feat: GBK encoding auto-detection for non-UTF-8 file read/write | NOT_APPLICABLE | — | REVERTED by aaabf0c1 due to round-trip byte corruption (17c06690). Both add and revert are in this batch. OC should NOT port — the approach was broken. |
| ea5df0ab | chore: 2.4.0 | NOT_APPLICABLE | — | Version bump |
| 89800137 | fix: issue-template test accidentally deleting .github/workflows | NOT_APPLICABLE | — | Test fix only |
| 17c06690 | fix: non-UTF-8 encoding file read/write round-trip byte corruption | NOT_APPLICABLE | — | Fix for 0ce8f7a1 but then REVERTED by 43c20a43. Don't port. |
| 43c20a43 | Revert "fix: non-UTF-8 encoding file read/write round-trip byte corruption" | NOT_APPLICABLE | — | Revert |
| aaabf0c1 | Revert "feat: add GBK encoding auto-detection" | NOT_APPLICABLE | — | Revert of broken feature |
| 5486d3c0 | fix: Bun mock.module cross-file pollution causing 87 test failures | NOT_APPLICABLE | — | Test infrastructure only |
| 4a39fd74 | fix: CI test stage test failures not exiting on error | NOT_APPLICABLE | — | CI only |
| 27a01113 | fix: CI 10 tests Bun mock.module cross-file pollution | NOT_APPLICABLE | — | Test infrastructure only |
| db606b55 | docs: update contributors | NOT_APPLICABLE | — | Documentation only |
| 8570b6ba | chore: 2.4.1 | NOT_APPLICABLE | — | Version bump |

## GAP Summary (commits needing backport)

### Security Gaps
1. **941bcbd2** — Third-party API user_id validation fix (DeepSeek/z.ai users may get 400 errors)
2. **2006ab25** — React Error Boundary enhancement (blank screen on crash vs. diagnostic output)

### Correctness Gaps
3. **8ba51ede** — Conditional hooks React violation fix ("Rendered fewer hooks than expected" crashes)
4. **dc3d3e88** — Remove auto mode provider/model whitelist (auto mode broken on z.ai/DeepSeek)
5. **6e1d3d8f** — Fix feature() usage in modelSupportsAutoMode (minor ternary fix)
6. **e8759f34** — Disable opus[1m] auto-migration (respects user model choice)

### Feature/UX Gaps
7. **84f12f34** — Elevate CLAUDE.md instruction weight via independent <project-instructions> block
8. **e3c0699f** — Prompt cache hit rate detection and warning (complete new feature: ~130 LOC)
9. **2f86485d** — Slim system prompt (token savings for low-context providers)
10. **771e3dbc + f7f69b75** — Attribution model name fixes (shown wrong model name for non-Anthropic providers)

### Large Architecture Gaps (would need substantial porting)
11. **7be08f53 + 8c157f07 + c14b7ead + 4fc95bd5 + af0d7dc8 + bd225384 + 3ac866be** — Unified Tool Search system (CORE_TOOLS whitelist + TF-IDF + ExecuteExtraTool). OC currently has anthropic-first tool deferral via tool_reference blocks. CCB replaces entirely with provider-agnostic text-based system. Large port but aligns with OC's existing third-party focus.

## Commits Already Present
- 2f150d3e: refreshInterval already in StatusLine.tsx
- 12f5aedf: diff highlight rendering already in FileEditTool/UI.tsx
- 8cfe9b6d, 958ac3a0: feature flags already all enabled via bundle polyfill

## Total: 73 commits analyzed
- GAP (fix needed): ~15 substantive commits across 6 categories
- ALREADY_HAVE: 3 commits
- NOT_APPLICABLE: 55 commits (merges, docs, CI/test, chores, CCB-specific features)
