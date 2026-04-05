# Upstream Backlog

Upstream features from anthropics/claude-code not yet implemented in OpenClaude.
Source: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md

Only entries after v2.1.87 (our fork base). Refresh by fetching:
`curl -fsSL https://raw.githubusercontent.com/anthropics/claude-code/refs/heads/main/CHANGELOG.md`

## 2.1.92

- [-] `Added forceRemoteSettingsRefresh policy setting` — SKIP (Anthropic managed infra)
- [-] `Added interactive Bedrock setup wizard` — SKIP (Anthropic cloud infra, needs AWS SDK integration)
- [x] `Added per-model and cache-hit breakdown to /cost` — DONE in bb4fad9
- [x] `/release-notes is now an interactive version picker` — DONE in 64c457b
- [-] `Remote Control session names use hostname prefix` — SKIP (bridge/remote feature)
- [ ] `Pro users see footer hint for prompt cache expiry` — TODO
- [x] `Fixed subagent spawning failing after tmux windows killed` — DONE in 7b8f28c
- [x] `Fixed prompt-type Stop hooks failing on ok:false` — DONE in 2d14581
- [x] `Fixed tool input validation for streaming JSON strings` — DONE in 861dbd0
- [x] `Fixed API 400 on whitespace-only thinking text block` — DONE (already in codebase, messages.ts:2313-2324 filterWhitespaceOnlyAssistantMessages)
- [-] `Fixed feedback survey auto-submissions` — SKIP (feedback disabled)
- [x] `Fixed misleading esc hints in fullscreen mode` — DONE in 24fffc1
- [-] `Fixed Homebrew install update prompts` — SKIP (we use GitHub Releases)
- [x] `Fixed ctrl+e jumping in multiline prompts` — DONE in 2d14581
- [x] `Fixed duplicate message in fullscreen scrollback` — DONE (already in codebase, ink.tsx:586-591 BSU/ESU atomicity for DECSTBM scroll)
- [x] `Fixed idle-return token hint showing cumulative tokens` — DONE in 2d14581
- [x] `Fixed plugin MCP servers stuck connecting` — DONE in 7b8f28c
- [x] `Improved Write tool diff speed 60% faster` — DONE in 24c7f5b
- [-] `Removed /tag command` — SKIP (we keep /tag)
- [-] `Removed /vim command` — SKIP (we keep /vim)
- [-] `Linux sandbox apply-seccomp helper` — SKIP (sandbox infra)

## 2.1.91

- [x] `Added MCP tool result persistence override via _meta annotation (500K)` — DONE in 9de31ec
- [x] `Added disableSkillShellExecution setting` — DONE in 9de31ec
- [x] `Added multi-line prompts in deep links` — DONE in 9de31ec
- [x] `Plugins can ship executables under bin/` — DONE in 9de31ec
- [x] `Fixed transcript chain breaks on --resume` — DONE in 653d2b6
- [x] `Fixed cmd+delete on iTerm2/kitty/WezTerm/Ghostty/Windows Terminal` — DONE in bb4fad9
- [x] `Fixed plan mode losing plan file after container restart` — DONE (already in codebase, plans.ts copyPlanForResume + persistFileSnapshotIfRemote)
- [x] `Fixed JSON schema validation for permissions.defaultMode auto` — DONE (already in codebase, all 87 flags on so TRANSCRIPT_CLASSIFIER includes 'auto' in PERMISSION_MODES)
- [-] `Fixed Windows version cleanup` — SKIP (Windows-specific)
- [x] `Fixed /feedback explains why unavailable` — DONE in 653d2b6
- [x] `Improved /claude-api skill guidance` — DONE in 64c457b
- [x] `Improved stripAnsi performance via Bun.stripANSI` — DONE in 9de31ec
- [x] `Edit tool uses shorter old_string anchors` — DONE in 0673875

## 2.1.90

- [-] `Added /powerup interactive lessons` — SKIP (content-heavy Anthropic marketing feature with animated demos)
- [x] `Added CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE` — DONE in 9de31ec
- [x] `Added .husky to protected directories` — DONE in 9de31ec
- [x] `Fixed infinite loop rate-limit options dialog` — DONE in 24c7f5b
- [x] `Fixed --resume prompt-cache miss with deferred tools` — DONE (already in codebase, USER_TYPE=ant enables isDeferredToolsDeltaEnabled → delta mode persists deferred tool announcements across resume)
- [x] `Fixed Edit/Write failing with format-on-save hooks` — DONE in 24c7f5b
- [x] `Fixed PreToolUse hooks with JSON stdout exit code 2` — DONE in 1d66372
- [ ] `Fixed collapsed search/read badge duplication in fullscreen` — TODO
- [x] `Fixed auto mode not respecting explicit user boundaries` — DONE in 7b8f28c (populated empty classifier prompt files)
- [ ] `Fixed click-to-expand hover text on light themes` — TODO
- [x] `Fixed UI crash on malformed tool input in permission dialog` — DONE in 2d14581
- [ ] `Fixed headers disappearing in selection screens` — TODO
- [-] `Hardened PowerShell tool permission checks` — SKIP (PowerShell-specific)
- [x] `Improved MCP tool schema cache-key performance` — DONE in 7b8f28c
- [x] `Improved SSE transport large frame handling (quadratic → linear)` — DONE in 1839702
- [x] `Improved SDK transcript write performance` — DONE in 79b1753
- [x] `Improved /resume parallel project loading` — DONE in 64c457b
- [x] `Changed --resume to hide -p/SDK sessions` — DONE in 653d2b6
- [x] `Removed DNS cache commands from auto-allow` — DONE in 9de31ec

## 2.1.89

- [x] `Added defer permission decision to PreToolUse hooks` — DONE in 9de31ec
- [x] `Added CLAUDE_CODE_NO_FLICKER=1 alt-screen rendering` — DONE (already in codebase, fullscreen.ts:112-116)
- [x] `Added PermissionDenied hook with retry` — DONE (already in codebase, hooks.ts:2934, toolExecution.ts:1096)
- [ ] `Added named subagents to @ mention typeahead` — TODO
- [x] `Added MCP_CONNECTION_NONBLOCKING for -p mode` — DONE (already in codebase, cli.tsx:38)
- [ ] `Auto mode denied commands show notification + retry in /permissions` — TODO
- [x] `Fixed Edit/Read allow rules to check symlink targets` — DONE in 24c7f5b
- [-] `Fixed voice push-to-talk modifier bindings` — SKIP (voice not priority)
- [-] `Fixed Edit/Write CRLF doubling on Windows` — SKIP (Windows-specific)
- [x] `Fixed StructuredOutput schema cache 50% failure rate` — DONE (already in codebase, api.ts:142-146 cache key includes inputJSONSchema)
- [x] `Fixed memory leak in LRU cache keys` — DONE in 24c7f5b
- [x] `Fixed crash removing message from 50MB+ sessions` — DONE (already in codebase, sessionStorage.ts MAX_TOMBSTONE_REWRITE_BYTES guard)
- [x] `Fixed LSP server zombie state after crash` — DONE in bb4fad9
- [x] `Fixed prompt history CJK/emoji truncation at 4KB boundary` — DONE (already in codebase, fsOperations.ts:730-733 raw byte carry across chunk boundaries)
- [x] `Fixed /stats undercounting subagent tokens` — DONE in bb4fad9
- [ ] `Fixed -p --resume hangs on 64KB+ deferred input` — TODO
- [-] `Fixed claude-cli:// deep links on macOS` — SKIP (desktop app)
- [x] `Fixed MCP tool errors truncating to first content block` — DONE in 9de31ec
- [x] `Fixed skill reminders dropped with SDK image messages` — DONE in 653d2b6
- [x] `Fixed hook file_path not absolute for Write/Edit/Read` — DONE in 40965ea
- [x] `Fixed autocompact thrash loop (3x detection)` — DONE in 9de31ec
- [x] `Fixed prompt cache misses from tool schema changes mid-session` — DONE (already in codebase, toolSchemaCache.ts + api.ts:151)
- [x] `Fixed nested CLAUDE.md re-injection in long sessions` — DONE (already in codebase, attachments.ts:1719-1723 loadedNestedMemoryPaths Set)
- [x] `Fixed --resume crash on older transcript format` — DONE in 64c457b
- [x] `Fixed misleading rate limit message for entitlement errors` — DONE in 2d14581
- [x] `Fixed hooks if condition not matching compound commands` — DONE (already in codebase, BashTool.tsx:487-510 preparePermissionMatcher splits compound commands)
- [ ] `Fixed collapsed group badge duplication in parallel tool use` — TODO
- [x] `Fixed notification invalidates not clearing immediately` — DONE (already in codebase, notifications.tsx invalidatesCurrent clears current + filters queue)
- [x] `Fixed prompt disappearing after submit with background messages` — DONE (already in codebase, REPL.tsx userInputBaselineRef bump on background messages)
- [x] `Fixed Devanagari/combining-mark text truncation` — DONE (already in codebase, intl.ts grapheme segmenter + useTypeahead.tsx:36 \p{M} combining marks + fsOperations.ts:731 UTF-8 byte boundary)
- [ ] `Fixed rendering artifacts on main-screen terminals` — TODO
- [-] `Fixed voice mode macOS Apple Silicon permission` — SKIP (voice)
- [-] `Fixed Shift+Enter on Windows Terminal Preview 1.25` — SKIP (Windows-specific)
- [ ] `Fixed UI jitter in iTerm2 inside tmux` — TODO
- [-] `Fixed PowerShell stderr on Windows 5.1` — SKIP (Windows)
- [x] `Fixed OOM crash on Edit for >1GiB files` — DONE (already in codebase, FileEditTool.ts:80-195 MAX_EDIT_FILE_SIZE guard)
- [x] `Improved collapsed tool summary for ls/tree/du` — DONE (already in codebase, BashTool.tsx BASH_LIST_COMMANDS + CollapsedReadSearchContent.tsx listCount)
- [x] `Improved Bash tool warn on formatter modifying read files` — DONE in 24fffc1
- [x] `Improved @ typeahead ranking source files above MCP resources` — DONE in 64c457b
- [-] `Improved PowerShell prompt for 5.1 vs 7+` — SKIP (Windows)
- [x] `Changed Edit to work on files viewed via Bash sed/cat` — DONE in 9de31ec
- [x] `Changed hook output >50K saved to disk with preview` — DONE in 9de31ec
- [x] `Changed cleanupPeriodDays: 0 rejected with validation error` — DONE in ec02901
- [x] `Changed thinking summaries off by default` — DONE (already in codebase, betas.ts:274 defaults to redacted thinking)
- [x] `Documented TaskCreated hook event` — DONE (already in codebase, coreSchemas.ts:601-607)
- [ ] `Preserved task notifications on Ctrl+B background` — TODO
- [-] `PowerShell argument-splitting hardening` — SKIP (Windows)
- [-] `/env now applies to PowerShell tool` — SKIP (PowerShell-specific)
- [x] `/usage hides redundant Sonnet bar for Pro/Enterprise` — DONE (already in codebase, Usage.tsx:236 showSonnetBar only for max/team/null)
- [x] `Image paste no longer inserts trailing space` — DONE in 1decbda
- [x] `Pasting !command enters bash mode` — DONE (already in codebase, PromptInput.tsx:1206)
- [x] `/buddy April 1st creature` — DONE (already in our fork via BUDDY flag)
