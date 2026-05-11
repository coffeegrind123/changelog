# CCB Fix Audit — openclaude backport catalog

Systematic review of every commit from [claude-code-best/claude-code](https://github.com/claude-code-best/claude-code) main branch (oldest→newest, skipping initial build commit `f90eee85`). Pure documentation — a separate session will apply selected fixes using this file as context.

**Started:** 2026-05-11  
**Total commits to review:** 647  
**Status key:** `[ ]` TODO | `[x]` APPLIED (future) | `[-]` SKIP | `[~]` PARTIAL

---

## Audit changelog

- **2026-05-11 (initial setup)** — Created tracking document. Agents launched for batch processing.
- **2026-05-11 (batch 5/8 complete)** — Commits 326-406 processed: 4 APPLY found, 73 SKIP, 3 FEATURE_SKIP

---

## Scope & Methodology

Each CCB commit is examined for:
- **Which files changed** and what the change does
- **Whether the affected files exist** in openclaude (`/home/openclaudeuser/openclaude/src/`)
- **Fix vs feature**: genuine bug fix (logic error, crash, leak, race, API compat, security, tool behavior, error handling) vs new feature vs refactor/docs/CI

**Relevance:**
- **DOCUMENTED** — Fix applies to code both repos share; worth backporting
- **NOT_RELEVANT** — CCB-only (CI/docs/lockfile/build/Windows/macOS/nodejs-specific/features not in openclaude/langfuse/CCB chrome/CCB RCS)

---

## APPLY Candidates (fixes worth backporting)

### 1. `e4ce08fe` (extracted) — Context counter flash to 0% on third-party APIs
- **Date:** 2026-04-20
- **Files:** `src/utils/tokens.ts`, `src/utils/context.ts`
- **Fix:** `getCurrentUsage()` skips all-zero usage objects (third-party APIs return placeholder). `calculateContextPercentages()` returns null when `totalInputTokens === 0`.
- **Impact:** z.ai/DeepSeek users see context flash to 0% during loading
- **Risk:** Low — simple guard clauses

### 2. `8442aaad` — n keybinding causes accidental dialog close
- **Date:** 2026-04-14
- **Files:** `src/keybindings/defaultBindings.ts`
- **Fix:** Remove `y: 'confirm:yes'` and `n: 'confirm:no'` from Confirmation context (keep Enter/Escape only)
- **Impact:** Typing `n` during confirmation accidentally dismisses dialog

### 3. `cee62bc6` — Model alias infinite recursion stack overflow
- **Date:** 2026-04-21
- **Files:** `src/utils/model/model.ts`
- **Fix:** `isAliasOrAliasWithSuffix()` guard in `getDefaultOpus/Sonnet/Haiku` fallback paths
- **Impact:** `parseUserSpecifiedModel()` calls back to these for aliases — recursion possible

### 4. `be97a0b0` (extracted) — Empty beta header filtering
- **Date:** 2026-04-22
- **Files:** `src/services/api/claude.ts`
- **Fix:** `betasParams.filter(Boolean)` before sending — empty-string beta headers cause 400 errors

### 5. `4b440479` — iTerm2 terminal response sequences leak into REPL input
- **Date:** 2026-04-07
- **Files:** `src/utils/earlyInput.ts`
- **Fix:** Proper CSI/string sequence handling instead of naive "skip until 0x40-0x7E"
- **Impact:** Terminal query responses (DA1, etc.) appear as garbage in input buffer

### 6. `bb078362` — CRLF SSE frame parsing
- **Date:** 2026-04-09
- **Files:** `src/cli/transports/SSETransport.ts`
- **Fix:** Support `\r\n\r\n` frame delimiter + strip trailing `\r` from lines
- **Impact:** SSE streams with CRLF line endings produce malformed frames

*(More APPLY candidates will be added as remaining batches complete)*

---

## Batch Progress

| Batch | Commits | Agent | Status | APPLY found |
|-------|---------|-------|--------|-------------|
| A | 1-82 | a6c2c726 | Running | — |
| B | 83-164 | ae3f9629 | Running | — |
| C | 165-246 | aacc4469 | Running | — |
| D | 247-328 | a1253485 | Running | — |
| E | 329-410 | a0c49df7 | **DONE** | 4 |
| F | 411-492 | a3b91cfa | Running | — |
| G | 493-574 | a64b8770 | Running | — |
| H | 575-647 | a622ead0 | Running | — |

---

## Full Commit Catalog

*(Being populated as agents complete. Each batch adds its table below.)*

### Batch E (commits 329-410) — COMPLETE

| SHA | Date | Subject | Type | Files | FileInOC | Relevance | Notes |
|-----|------|---------|------|-------|----------|-----------|-------|
| cee62bc6 | 2026-04-21 | fix: model alias recursion | fix | model/model.ts | YES | DOCUMENTED | isAliasOrAliasWithSuffix guard |
| e4ce08fe | 2026-04-20 | fix: context counter flash | fix | tokens.ts, context.ts | YES | DOCUMENTED | Skip all-zero usage for 3rd-party APIs |
| 8442aaad | 2026-04-14 | fix: n keybinding close | fix | defaultBindings.ts | YES | DOCUMENTED | Remove y/n from Confirmation context |
| be97a0b0 | 2026-04-22 | feat: Bedrock client (extracted fix) | feat | claude.ts | YES | DOCUMENTED | betasParams.filter(Boolean) |
| 227083d3 | 2026-04-12 | fix: screenshot MIME type | fix | computer-use-mcp | NO | NOT_RELEVANT | CCB CU package |
| 513ccc30 | 2026-04-12 | fix: auth issue | fix | main.tsx | NO | NOT_RELEVANT | CCB chrome MCP |
| 8399d9ed | 2026-04-12 | fix: type issue | fix | coreSchemas.ts | NO | NOT_RELEVANT | CCB auto-mode type |
| bd6448ec | 2026-04-12 | fix: ordering fix | fix | WebSearch | NO | NOT_RELEVANT | Minor reorder |
| 3cf94fbd | 2026-04-12 | fix: poor mode dream skip | fix | stopHooks.ts | YES | NOT_RELEVANT | Already handled via isLowContextMode |
| 9b8503d1 | 2026-04-13 | fix: node env no bun | fix | build.ts | NO | NOT_RELEVANT | Build-only |
| e0484e28 | 2026-04-13 | fix: chrome bridge | fix | chrome | NO | NOT_RELEVANT | CCB chrome |
| d4b30d32 | 2026-04-13 | fix: chrome link | fix | chrome | NO | NOT_RELEVANT | CCB chrome |
| a7e03a5b | 2026-04-13 | fix: interrupt log | fix | query.ts | NO | NOT_RELEVANT | Langfuse-only |
| be80da4c | 2026-04-13 | fix: cache | fix | cache | NO | NOT_RELEVANT | Langfuse+cache |
| ecbd5a93 | 2026-04-13 | fix: Bun.hash | fix | build.ts | NO | NOT_RELEVANT | Build-only |
| 1a4e9702 | 2026-04-15 | fix: type issues | fix | packages/ | NO | NOT_RELEVANT | CCB packages |
| b80483c2 | 2026-04-14 | fix: node ws not bundled | fix | build | NO | NOT_RELEVANT | CCB build |
| ac42ce2d | 2026-04-17 | fix: node loading calc | fix | RCS web | NO | NOT_RELEVANT | CCB RCS |
| c5ab83a3 | 2026-04-17 | fix: linux install | fix | scripts/ | NO | NOT_RELEVANT | CCB install script |
| a0dc4540 | 2026-04-19 | fix: double slash | fix | RCS | NO | NOT_RELEVANT | CCB RCS |
| a57ca085 | 2026-04-19 | fix: node ES version | fix | build | NO | NOT_RELEVANT | CCB build |
| f9d01116 | 2026-04-19 | fix: crypto.randomUUID | fix | RCS web | NO | NOT_RELEVANT | CCB RCS frontend |
| 13a0bfc4 | 2026-04-20 | fix: build import failure | fix | build | NO | NOT_RELEVANT | CCB vite build |
| 956e98a4 | 2026-04-21 | fix: duplicate dependency | fix | package.json | NO | NOT_RELEVANT | CCB package.json |
| 71144047 | 2026-04-12 | Add brave WebSearch | feat | WebSearch | NO | NOT_RELEVANT | Feature addition |
| e770f1ef | 2026-04-12 | mcp-chrome integration | feat | chrome | NO | NOT_RELEVANT | CCB chrome MCP |
| b8d86e52 | 2026-04-25 | Local Vault service | feat | vault/ | NO | NOT_RELEVANT | CCB-specific feature |
| a2ea69c0 | 2026-04-25 | Session Memory multi-storage | feat | session/ | NO | NOT_RELEVANT | CCB-specific feature |
| 2fb1c9dc | 2026-04-13 | tool/MCP major refactor | feat | 70+ files | NO | NOT_RELEVANT | Massive restructure |
| 8cfe9b6d | 2026-05-07 | COORDINATOR_MODE flag | feat | feature.ts | NO | NOT_RELEVANT | CCB feature flag |
| e8759f34 | 2026-05-07 | opus[1m] auto migration | fix | model.ts | NO | NOT_RELEVANT | CCB-specific |
| 771e3dbc | 2026-05-07 | non-Anthropic attribution | fix | attribution | NO | NOT_RELEVANT | CCB attribution system |
| f7f69b75 | 2026-05-07 | model alias attribution | fix | attribution | NO | NOT_RELEVANT | CCB attribution system |
| aa06cea9 | 2026-05-07 | GLM email fix | fix | attribution | NO | NOT_RELEVANT | CCB attribution system |
| 8ba51ede | 2026-05-08 | conditional hook error | fix | hooks | NO | NOT_RELEVANT | CCB hook architecture |
| c14b7ead | 2026-05-09 | Tool Search cache | fix | toolSearch | NO | NOT_RELEVANT | CCB Tool Search (ours is different) |
| 3ac866be | 2026-05-09 | cache hit rate warning | fix | cache | NO | NOT_RELEVANT | CCB cache system |
| 12f5aedf | 2026-05-06 | diff highlight rendering | fix | highlight | MAYBE | NOT_RELEVANT | CCB highlight system |
| 2006ab25 | 2026-05-09 | React Error Boundary | fix | ErrorBoundary | NO | NOT_RELEVANT | CCB UI component |
| 82be5ff0 | 2026-05-10 | code review fixes | fix | various | NO | NOT_RELEVANT | CCB-specific |
| 8fccd323 | 2026-05-10 | API base URL masking | fix | logging | NO | NOT_RELEVANT | CCB logging |
| 80d4e095 | 2026-05-10 | setupAxiosMock | fix | test | NO | NOT_RELEVANT | CCB test infra |
| 5c499d31 | 2026-05-10 | orgUUID masking | fix | logging | NO | NOT_RELEVANT | CCB logging |
| dc3d3e88 | 2026-05-10 | auto mode whitelist | fix | autoMode | NO | NOT_RELEVANT | CCB auto mode |
| 6e1d3d8f | 2026-05-10 | feature usage | fix | feature | NO | NOT_RELEVANT | CCB feature system |
| 89800137 | 2026-05-10 | issue-template test | fix | test | NO | NOT_RELEVANT | CCB test |
| 17c06690 | 2026-05-10 | GBK encoding round-trip | fix | file tools | NO | NOT_RELEVANT | Chinese encoding (reverted) |
| 5486d3c0 | 2026-05-11 | Bun mock.module pollution | fix | test | NO | NOT_RELEVANT | CCB test infra |
| 4a39fd74 | 2026-05-11 | CI test exit bug | fix | CI | NO | NOT_RELEVANT | CCB CI |
| 27a01113 | 2026-05-11 | CI test mock pollution | fix | CI | NO | NOT_RELEVANT | CCB CI |
