# CCB Gap Analysis — Batch 3 (commits 165-246)

fa5329db | Merge remote main | NOT_APPLICABLE | — | Merge commit
21b28545 | 1.0.4 | NOT_APPLICABLE | — | Version bump
fc9faa2a | docs: update docs | NOT_APPLICABLE | — | Docs only
419d1e8b | docs: update CLAUDE.md | NOT_APPLICABLE | — | Docs only
6fefff2e | OpenAI mode fix (#102) | ALREADY_HAVE | auth.ts:127-149 | hasExternalAuthToken path covers this via ANTHROPIC_AUTH_TOKEN
dfe25b18 | Merge branch | NOT_APPLICABLE | — | Merge commit
ad1f90a0 | feat: restore mac Computer Use | NOT_APPLICABLE | — | macOS-specific
765569b3 | feat: Computer Use user guide docs | NOT_APPLICABLE | — | Docs only
6a3fd223 | fix download-ripgrep MODULE_NOT_FOUND | NOT_APPLICABLE | — | CCB-specific script, not in openclaude
840d4574 | fix F5 debug | NOT_APPLICABLE | — | VSCode launch config, IDE-specific
ea06f507 | docs: add computer use description | NOT_APPLICABLE | — | Docs only
ab7556e3 | auto dream enabled | ALREADY_HAVE | dream.ts, autoDream/ | /dream skill + autoDream already implemented
462fe69d | fix OpenAI cost calculation | ALREADY_HAVE | claude.ts:2387-2393 | All providers go through claude.ts cost tracking via bridge
f83198e5 | remove npm deprecation warning | NOT_APPLICABLE | — | CCB-specific UI, not in openclaude
b5d1dbc9 | /provider command switch model type | NOT_APPLICABLE | — | Feature addition, openclaude uses ANTHROPIC_BASE_URL env var instead
ec5dfed1 | fix provider command | NOT_APPLICABLE | — | CCB-specific /provider command
d3a607e4 | fix code highlighting + LRU cache | GAP | queryHelpers.ts:388-397, fileStateCache.ts:37 | Write tool content can be non-string from JSON deser; LRU size calc doesn't handle nested objects
354c11f0 | improve LRU cache size calculation | GAP | fileStateCache.ts:37 | Same fix as d3a607e4 — nested object handling in sizeCalculation
eb6fbe51 | separate OpenAI env vars | NOT_APPLICABLE | — | CCB-specific OpenAI model config, openclaude uses ANTHROPIC_MODEL
0da5ec09 | Gemini protocol adapter | NOT_APPLICABLE | — | CCB-specific Gemini support, openclaude uses bridge approach
e88dcb2f | fix OpenAI adapter tool calling compat | GAP | schemaSanitizer.ts:251-255 | const→enum conversion missing; OpenAI rejects 'const' in tool schemas
6f80e96f | modelType precedence fix | NOT_APPLICABLE | — | CCB-specific provider priority model, openclaude uses ANTHROPIC_BASE_URL
eca1acc6 | OpenAI image compatibility | NOT_APPLICABLE | — | Gemini adapter tests, not OpenAI image compat
e8f417e5 | Merge computer-use/mac-support | NOT_APPLICABLE | — | Merge commit
bd6707ad | Merge AgentArc/main | NOT_APPLICABLE | — | Merge commit
d720580e | docs: rg download tip | NOT_APPLICABLE | — | Docs only
affc826b | Merge branch main | NOT_APPLICABLE | — | Merge commit
c99021d5 | fix windows no unzip | NOT_APPLICABLE | — | Windows-specific
4fa75824 | Merge branch main | NOT_APPLICABLE | — | Merge commit
7631c0f4 | Merge remote main | NOT_APPLICABLE | — | Merge commit
3ae973c7 | ReWrite | NOT_APPLICABLE | — | Large rewrite, not a specific fix
e548369f | ReWrite | NOT_APPLICABLE | — | Large rewrite, not a specific fix
02694918 | docs/buid scripts update | NOT_APPLICABLE | — | Docs/build only
ad104449 | Merge branch main | NOT_APPLICABLE | — | Merge commit
5b1a52b8 | update tsx + login panel | NOT_APPLICABLE | — | CCB-specific migration
0c9fd37e | Merge branch main | NOT_APPLICABLE | — | Merge commit
f49c7d7e | Revert docs | NOT_APPLICABLE | — | Docs revert
c33d5dcb | Merge branch main | NOT_APPLICABLE | — | Merge commit
a0141c1b | ConsoleOAuthFlow format restore | NOT_APPLICABLE | — | CCB-specific formatting
1e53943e | fix small issues | NOT_APPLICABLE | — | CCB-specific minor fixes
282f2f43 | remove misleading comment | NOT_APPLICABLE | — | Comment removal
41f733a6 | validate OAuth base_url | NOT_APPLICABLE | — | CCB-specific OAuth validation
a50971f2 | ConsoleOAuthFlow base_url URL validation | NOT_APPLICABLE | — | CCB-specific OAuth validation
7a2ade0a | add .agents/.codex/.omx to .gitignore | NOT_APPLICABLE | — | .gitignore only
c17edcb1 | Computer Use Windows cross-platform | NOT_APPLICABLE | — | Windows-specific + CCB feature
4e5a0dd2 | fix code highlighting (#126) | NOT_APPLICABLE | — | Same fix as d3a607e4 (duplicate)
918defad | Merge PR #127 | NOT_APPLICABLE | — | Merge commit
2f95d1a3 | Merge branch main | NOT_APPLICABLE | — | Merge commit
714ef13e | fix absolute path in dev.ts | NOT_APPLICABLE | — | CCB-specific dev script
ba97889c | Merge PR #135 | NOT_APPLICABLE | — | Merge commit
ecac0ab9 | Merge branch main | NOT_APPLICABLE | — | Merge commit
2b843339 | Merge PR #137 | NOT_APPLICABLE | — | Merge commit
96f6d2c7 | enable feature flags (SHOT_STATS etc) | ALREADY_HAVE | bundle/index.ts | All feature flags already enabled in openclaude
5916ecff | docs: DEV-LOG for feature flags | NOT_APPLICABLE | — | Docs only
27825293 | Merge PR #140 | NOT_APPLICABLE | — | Merge commit
1f8f90eb | Merge branch main | NOT_APPLICABLE | — | Merge commit
522a1a36 | enable Computer Use on Win+Linux | NOT_APPLICABLE | — | Platform-specific feature
ced50800 | enable mouse click functionality | NOT_APPLICABLE | — | CCB-specific Computer Use feature
cd70c1b7 | fix MACRO fallback | ALREADY_HAVE | cli.tsx:19-25 | MACRO already defined at top of cli.tsx
26245e0b | Merge branch main | NOT_APPLICABLE | — | Merge commit
dee2ffd6 | support simplified rg download | NOT_APPLICABLE | — | CCB-specific download script
a7a9659d | resolve errors | NOT_APPLICABLE | — | CCB-specific fixes
fc0bebf6 | fix MACRO fallback (#146) | NOT_APPLICABLE | — | Already covered by cd70c1b7
258cc720 | docs: add documentation | NOT_APPLICABLE | — | Docs only
14dc54a0 | Gemini model env var separation | NOT_APPLICABLE | — | CCB-specific Gemini support
3923af48 | fix login panel left-right switching | NOT_APPLICABLE | — | CCB-specific UI fix
919011a3 | fix login form enter coverage | NOT_APPLICABLE | — | CCB-specific UI fix
81ecd82b | Test | NOT_APPLICABLE | — | Test commit
eb62b470 | e | NOT_APPLICABLE | — | Misc commit
a15340f5 | Merge branch main | NOT_APPLICABLE | — | Merge commit
5bf3c938 | add contributors auto-update workflow | NOT_APPLICABLE | — | CI/automation
fec8ec6a | fix contributors link in README | NOT_APPLICABLE | — | Docs only
7d88b4df | docs: update contributors | NOT_APPLICABLE | — | Docs only
6e598fc4 | Merge PR #149 | NOT_APPLICABLE | — | Merge commit
767d6fae | Merge branch main | NOT_APPLICABLE | — | Merge commit
f05a6c9f | Merge PR #129 | NOT_APPLICABLE | — | Merge commit
ca630488 | docs: update contributors | NOT_APPLICABLE | — | Docs only
dd2bd126 | add yellow [local] tag for project skills | NOT_APPLICABLE | — | CCB-specific UI feature
3fff2a07 | add teach-me skill | ALREADY_HAVE | skills/bundled/teach-me/ | Already ported from CCB (CLAUDEMd:268)
dc8ce1bb | add interview mode | NOT_APPLICABLE | — | CCB feature addition, not a fix
4d62f631 | docs: update contributors | NOT_APPLICABLE | — | Docs only
c16fc628 | chore: update | NOT_APPLICABLE | — | Chore, not a specific fix
