# Gitlawb Gap Analysis — Batch 5 (commits 293–365)

**Date:** 2026-05-11  
**Range:** `git log --reverse main | tail -n +2 | sed -n '293,365p'` (71 commits)  
**Openclaude base:** `/home/openclaudeuser/openclaude/src/`

## Summary

| Verdict | Count |
|---------|-------|
| GAP (fix missing in openclaude) | 8 |
| ALREADY_HAVE | 11 |
| NOT_APPLICABLE | 52 |

---

## GAP Findings

### 1. 0951c8b — dangerous path check before auto-allow rm/rmdir in acceptEdits mode
**VERDICT:** GAP | **PRIORITY:** HIGH  
**OC FILE:** `src/tools/BashTool/modeValidation.ts:39-50`  
**NOTES:** Openclaude's `validateCommandForMode` returns `{behavior:'allow'}` for all filesystem commands (rm, rmdir, mv, cp, sed, mkdir, touch) in acceptEdits mode WITHOUT calling `checkDangerousRemovalPaths` first. This means `rm -rf ~` and `rm -rf /` bypass the dangerous path guard entirely in acceptEdits mode. Gitlawb's fix adds a guard block for rm/rmdir that calls `checkDangerousRemovalPaths` before returning allow. This is critical for 3P models (DeepSeek, Ollama) that lack built-in refusal training and would blindly execute destructive commands. Also requires exporting `checkDangerousRemovalPaths` from `pathValidation.ts` (openclaude already exports it at line 74). Fixes finding 3 from issue #244.

### 2. 01acc4c — auto-allow safe read-only commands in acceptEdits mode
**VERDICT:** GAP | **PRIORITY:** MEDIUM  
**OC FILE:** `src/tools/BashTool/modeValidation.ts:38-51`  
**NOTES:** Openclaude only auto-allows write commands (mkdir, touch, rm, rmdir, mv, cp, sed) in acceptEdits mode. Gitlawb adds read-only commands (grep, cat, ls, find, head, tail, echo, pwd, wc, sort, uniq, diff) with safety guards: shell redirection detection via `tryParseShellCommand`, and validation through existing `checkReadOnlyConstraints`. Openclaude's `modeValidation.ts` is the original 117-line file without these changes. The fix includes a new test file (`modeValidation.test.ts`) and restructures `ACCEPT_EDITS_ALLOWED_COMMANDS` into `ACCEPT_EDITS_WRITE_COMMANDS` + `ACCEPT_EDITS_READ_ONLY_COMMANDS`.

### 3. 284d9bd — image dimension limit fix (2000→1568)
**VERDICT:** GAP | **PRIORITY:** MEDIUM  
**OC FILE:** `src/constants/apiLimits.ts:42-43`  
**NOTES:** Openclaude has `IMAGE_MAX_WIDTH = 2000` and `IMAGE_MAX_HEIGHT = 2000`. The API's many-image mode rejects images at exactly 2000px (the dimension limit). Changing to 1568px (the API's internal downscale target) avoids this rejection with zero quality loss. Simple two-line constant change.

### 4. daf2c90 — duplicate marketplace plugin loading
**VERDICT:** GAP | **PRIORITY:** MEDIUM  
**OC FILE:** `src/utils/plugins/pluginLoader.ts:3264` (`mergePluginSources`)  
**NOTES:** Openclaude's `mergePluginSources` deduplicates session vs marketplace plugins by name, but does NOT deduplicate marketplace plugins against each other. If a user enables `frontend-design@claude-code-plugins` and `frontend-design@claude-plugins-official`, both load and the short-name collision causes interference. Gitlawb's fix collapses duplicate marketplace plugins by name: keeps the enabled copy when enabled state differs, otherwise keeps the later config entry. Requires a new warning for the dropped duplicate.

### 5. 8ece290 — suppress startup dialogs when input is buffered
**VERDICT:** GAP | **PRIORITY:** MEDIUM  
**OC FILE:** `src/screens/REPL.tsx:2239`  
**NOTES:** Openclaude only uses `if (isPromptInputActive) return undefined` to suppress dialogs. This misses the case where input is already buffered (e.g., `-p` mode, piped stdin) but the user isn't actively typing. Gitlawb adds `src/screens/replInputSuppression.ts` with `isPromptTypingSuppressionActive(isPromptInputActive, inputValue)` that also returns true when `inputValue.trim().length > 0`. Used in `getFocusedInputDialog()` and `hasSuppressedDialogs`. Prevents startup dialogs from stealing focus during headless/scripted usage.

### 6. f9ce81b — handle missing skill parameter in SkillTool
**VERDICT:** GAP | **PRIORITY:** LOW  
**OC FILE:** `src/services/tools/toolExecution.ts`  
**NOTES:** Openclaude doesn't have `getSchemaValidationErrorOverride()` or `getSchemaValidationToolUseResult()` functions that provide actionable error messages when the SkillTool is called without a `skill` parameter. Gitlawb adds these functions to produce a clear "Missing skill name. Pass the slash command name as the skill parameter..." message instead of a generic Zod validation error. The `SkillTool` directory exists in openclaude at `src/tools/SkillTool/`.

### 7. 4ac7367 — include retry timing in 429 error messages
**VERDICT:** GAP | **PRIORITY:** LOW  
**OC FILE:** `src/services/api/errors.ts` (429 handling section)  
**NOTES:** Openclaude doesn't extract the `retry-after` header from 429 API errors. Gitlawb's fix reads the header and includes timing guidance ("Try again in N seconds"). Minor UX improvement, but useful for users hitting rate limits.

### 8. 2caf2fd — defer startup checks and suppress recommendation dialogs during startup window
**VERDICT:** GAP | **PRIORITY:** MEDIUM  
**OC FILE:** `src/screens/REPL.tsx:849`  
**NOTES:** Openclaude calls `performStartupChecks(setAppState)` immediately on REPL mount (line 849), which can trigger plugin loading → LSP recommendation dialog → unmount PromptInput → CLI appears frozen. Gitlawb's fix defers startup checks until after first message submission (`submitCount > 0`), eliminating the startup freeze. Also suppresses lower-priority dialogs (LSP recommendation, plugin hint, desktop upsell) during the vulnerable startup window.

---

## ALREADY_HAVE

| SHA | Subject | OC File | Notes |
|-----|---------|---------|-------|
| b4bd95b | normalize malformed Bash tool args from OpenAI | `src/services/api/toolArgumentNormalization.ts` | Already has full normalization with STRING_ARGUMENT_TOOL_FIELDS, isBlankString, isLikelyStructuredObjectLiteral |
| 52d33a8 | MCP tool results in microcompact | `src/services/compact/microCompact.ts:60-61` | Already has `isCompactableTool()` with `mcp__` prefix check |
| 1e05702 | Fix GLM-5 reasoning model hang | `src/services/api/openaiBridge/streamTranslator.ts:518-525` | Already handles `reasoning_content` and `reasoning` fields |
| ccaa193 | preserve only originally-required properties in strict tool schemas | `src/utils/schemaSanitizer.ts:231-234` | Already filters `required[]` against actual properties |
| b4725c1 | skip Anthropic MCP registry fetch for 3P | `src/services/api/openaiBridge/` | Handled via openaiBridge architecture (different code path) |
| 08be518 | skip Anthropic preconnect for 3P | `src/services/api/openaiBridge/` | Handled via openaiBridge architecture |
| 4975cfc | strip Anthropic params from 3P resume paths | `src/utils/messages.ts:5279` (`stripSignatureBlocks`) + `src/query.ts:1072` | Has thinking-block stripping (gated on ant which is always true) |
| cdc92d1 | queue prompt guidance for next turn | Feature enhancement not present, but not a bug | UX only |
| fbf3385 | cross-provider model env var leaks | Openclaude only uses ANTHROPIC_MODEL (no GEMINI_MODEL/OPENAI_MODEL) | Not applicable architecture |
| d5852ca | coalesce consecutive same-role messages | `src/services/api/openaiBridge/requestTranslator.ts` | Each Anthropic msg → single OpenAI msg (different architecture, no coalescing needed) |
| 600c01f | Grep/Glob on OpenAI paths (Codex strict schemas) | Codex-specific, openclaude uses openaiBridge | Different architecture |

---

## NOT_APPLICABLE (selected)

Most of the 52 NOT_APPLICABLE commits fall into these categories:
- **Docs/CI/merge/version/test/build:** 5be5387, 80a2f14, 3b3aca7, 94de37d, 6c61790, 39f3b2b, 648ae80, af08b4f, 3188f6a, 5ef7954, 7350a79
- **Labeling/internal cleanup (ANT-ONLY, comments, source maps):** bd4daa3, 27e6505, 75d2543, 9e84d2f, 2f162af, 8fc40ee, 0d27ca5, ba1b991, 462a985, daa3aa2, 5ff3428
- **Gitlawb-specific features (openaiShim, Codex, gRPC, Gemini, GitHub, Ollama, etc.):** 280c973, ea335ae, ef881b2, c534aa5, 5012c16, 26eef92, ff7d499, ad724dc, 4ad6bc5, c328fdf
- **Windows-specific fixes:** c193497, c3c60b7, e4cf810
- **Feature gates / buddy activation:** d1a2df2, cdbe016
- **Dependency/security (lodash):** 3b9893b (lodash-es version pin, openclaude may have different deps)
- **Theme picker / TUI:** 8724d59, 537c469, e30ad17
- **3P-specific that openclaude handles differently:** 69ea1f1 (context window via NIM catalog), 600c01f (Codex schemas)
- **Web search custom provider:** 32fbd0c (Gitlawb feature, not in openclaude)
- **Dragged file paths:** 112df59 (TUI feature, not in openclaude)
- **CodeQL fixes:** a0bdab2, 4c3118e, e365cb4, b07bafa (may have differing coverage)
- **Provider-specific:** 72e6a94 (Gemini thought_signature), 60d3d89 (Ollama models)
- **infra-specific:** 85aa8b0 (Node < 20 polyfill), 42b121b (openclaude naming in Gitlawb)
- **PR intent scanner:** 7350a79 (CI workflow only)

---

## Priority Action Items

1. **HIGH:** `0951c8b` — Add dangerous path check to acceptEdits mode auto-allow for rm/rmdir (security-critical for 3P models)
2. **MEDIUM:** `01acc4c` — Add read-only command auto-allow in acceptEdits mode (reduces permission fatigue)
3. **MEDIUM:** `284d9bd` — Change IMAGE_MAX_WIDTH/HEIGHT from 2000 to 1568 (prevents API rejection)
4. **MEDIUM:** `daf2c90` — Deduplicate marketplace plugins by name (prevents interference)
5. **MEDIUM:** `8ece290` — Add buffered-input suppression for startup dialogs (prevents focus stealing in -p mode)
6. **MEDIUM:** `2caf2fd` — Defer startup checks until after first user submission (prevents CLI freeze at startup)
7. **LOW:** `f9ce81b` — Add actionable SkillTool error message for missing parameter
8. **LOW:** `4ac7367` — Extract retry-after header for 429 error messages

