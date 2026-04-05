# Upstream Backlog

Upstream features from anthropics/claude-code not yet implemented in OpenClaude.
Source: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md

Only entries after v2.1.87 (our fork base). Refresh by fetching:
`curl -fsSL https://raw.githubusercontent.com/anthropics/claude-code/refs/heads/main/CHANGELOG.md`

## 2.1.92

- [-] `Added forceRemoteSettingsRefresh policy setting` — SKIP (Anthropic managed infra)
- [ ] `Added interactive Bedrock setup wizard` — TODO
- [ ] `Added per-model and cache-hit breakdown to /cost` — TODO
- [ ] `/release-notes is now an interactive version picker` — TODO
- [-] `Remote Control session names use hostname prefix` — SKIP (bridge/remote feature)
- [ ] `Pro users see footer hint for prompt cache expiry` — TODO
- [ ] `Fixed subagent spawning failing after tmux windows killed` — TODO
- [ ] `Fixed prompt-type Stop hooks failing on ok:false` — TODO
- [ ] `Fixed tool input validation for streaming JSON strings` — TODO
- [ ] `Fixed API 400 on whitespace-only thinking text block` — TODO
- [-] `Fixed feedback survey auto-submissions` — SKIP (feedback disabled)
- [ ] `Fixed misleading esc hints in fullscreen mode` — TODO
- [-] `Fixed Homebrew install update prompts` — SKIP (we use GitHub Releases)
- [ ] `Fixed ctrl+e jumping in multiline prompts` — TODO
- [ ] `Fixed duplicate message in fullscreen scrollback` — TODO
- [ ] `Fixed idle-return token hint showing cumulative tokens` — TODO
- [ ] `Fixed plugin MCP servers stuck connecting` — TODO
- [ ] `Improved Write tool diff speed 60% faster` — TODO
- [-] `Removed /tag command` — SKIP (we keep /tag)
- [-] `Removed /vim command` — SKIP (we keep /vim)
- [-] `Linux sandbox apply-seccomp helper` — SKIP (sandbox infra)

## 2.1.91

- [x] `Added MCP tool result persistence override via _meta annotation (500K)` — DONE in 9de31ec
- [x] `Added disableSkillShellExecution setting` — DONE in 9de31ec
- [x] `Added multi-line prompts in deep links` — DONE in 9de31ec
- [x] `Plugins can ship executables under bin/` — DONE in 9de31ec
- [ ] `Fixed transcript chain breaks on --resume` — TODO
- [ ] `Fixed cmd+delete on iTerm2/kitty/WezTerm/Ghostty/Windows Terminal` — TODO
- [ ] `Fixed plan mode losing plan file after container restart` — TODO
- [ ] `Fixed JSON schema validation for permissions.defaultMode auto` — TODO
- [-] `Fixed Windows version cleanup` — SKIP (Windows-specific)
- [ ] `Fixed /feedback explains why unavailable` — TODO
- [ ] `Improved /claude-api skill guidance` — TODO
- [x] `Improved stripAnsi performance via Bun.stripANSI` — DONE in 9de31ec
- [ ] `Edit tool uses shorter old_string anchors` — TODO

## 2.1.90

- [ ] `Added /powerup interactive lessons` — TODO
- [x] `Added CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE` — DONE in 9de31ec
- [x] `Added .husky to protected directories` — DONE in 9de31ec
- [ ] `Fixed infinite loop rate-limit options dialog` — TODO
- [ ] `Fixed --resume prompt-cache miss with deferred tools` — TODO
- [ ] `Fixed Edit/Write failing with format-on-save hooks` — TODO
- [ ] `Fixed PreToolUse hooks with JSON stdout exit code 2` — TODO
- [ ] `Fixed collapsed search/read badge duplication in fullscreen` — TODO
- [ ] `Fixed auto mode not respecting explicit user boundaries` — TODO
- [ ] `Fixed click-to-expand hover text on light themes` — TODO
- [ ] `Fixed UI crash on malformed tool input in permission dialog` — TODO
- [ ] `Fixed headers disappearing in selection screens` — TODO
- [ ] `Hardened PowerShell tool permission checks` — TODO
- [ ] `Improved MCP tool schema cache-key performance` — TODO
- [ ] `Improved SSE transport large frame handling (quadratic → linear)` — TODO
- [ ] `Improved SDK transcript write performance` — TODO
- [ ] `Improved /resume parallel project loading` — TODO
- [ ] `Changed --resume to hide -p/SDK sessions` — TODO
- [x] `Removed DNS cache commands from auto-allow` — DONE in 9de31ec

## 2.1.89

- [x] `Added defer permission decision to PreToolUse hooks` — DONE in 9de31ec
- [ ] `Added CLAUDE_CODE_NO_FLICKER=1 alt-screen rendering` — TODO
- [ ] `Added PermissionDenied hook with retry` — TODO
- [ ] `Added named subagents to @ mention typeahead` — TODO
- [ ] `Added MCP_CONNECTION_NONBLOCKING for -p mode` — TODO
- [ ] `Auto mode denied commands show notification + retry in /permissions` — TODO
- [ ] `Fixed Edit/Read allow rules to check symlink targets` — TODO
- [-] `Fixed voice push-to-talk modifier bindings` — SKIP (voice not priority)
- [ ] `Fixed Edit/Write CRLF doubling on Windows` — TODO
- [ ] `Fixed StructuredOutput schema cache 50% failure rate` — TODO
- [ ] `Fixed memory leak in LRU cache keys` — TODO
- [ ] `Fixed crash removing message from 50MB+ sessions` — TODO
- [ ] `Fixed LSP server zombie state after crash` — TODO
- [ ] `Fixed prompt history CJK/emoji truncation at 4KB boundary` — TODO
- [ ] `Fixed /stats undercounting subagent tokens` — TODO
- [ ] `Fixed -p --resume hangs on 64KB+ deferred input` — TODO
- [-] `Fixed claude-cli:// deep links on macOS` — SKIP (desktop app)
- [x] `Fixed MCP tool errors truncating to first content block` — DONE in 9de31ec
- [ ] `Fixed skill reminders dropped with SDK image messages` — TODO
- [ ] `Fixed hook file_path not absolute for Write/Edit/Read` — TODO
- [x] `Fixed autocompact thrash loop (3x detection)` — DONE in 9de31ec
- [ ] `Fixed prompt cache misses from tool schema changes mid-session` — TODO
- [ ] `Fixed nested CLAUDE.md re-injection in long sessions` — TODO
- [ ] `Fixed --resume crash on older transcript format` — TODO
- [ ] `Fixed misleading rate limit message for entitlement errors` — TODO
- [ ] `Fixed hooks if condition not matching compound commands` — TODO
- [ ] `Fixed collapsed group badge duplication in parallel tool use` — TODO
- [ ] `Fixed notification invalidates not clearing immediately` — TODO
- [ ] `Fixed prompt disappearing after submit with background messages` — TODO
- [ ] `Fixed Devanagari/combining-mark text truncation` — TODO
- [ ] `Fixed rendering artifacts on main-screen terminals` — TODO
- [-] `Fixed voice mode macOS Apple Silicon permission` — SKIP (voice)
- [ ] `Fixed Shift+Enter on Windows Terminal Preview 1.25` — TODO
- [ ] `Fixed UI jitter in iTerm2 inside tmux` — TODO
- [-] `Fixed PowerShell stderr on Windows 5.1` — SKIP (Windows)
- [ ] `Fixed OOM crash on Edit for >1GiB files` — TODO
- [ ] `Improved collapsed tool summary for ls/tree/du` — TODO
- [ ] `Improved Bash tool warn on formatter modifying read files` — TODO
- [ ] `Improved @ typeahead ranking source files above MCP resources` — TODO
- [-] `Improved PowerShell prompt for 5.1 vs 7+` — SKIP (Windows)
- [x] `Changed Edit to work on files viewed via Bash sed/cat` — DONE in 9de31ec
- [x] `Changed hook output >50K saved to disk with preview` — DONE in 9de31ec
- [ ] `Changed cleanupPeriodDays: 0 rejected with validation error` — TODO
- [ ] `Changed thinking summaries off by default` — TODO
- [ ] `Documented TaskCreated hook event` — TODO
- [ ] `Preserved task notifications on Ctrl+B background` — TODO
- [-] `PowerShell argument-splitting hardening` — SKIP (Windows)
- [ ] `/env now applies to PowerShell tool` — TODO
- [ ] `/usage hides redundant Sonnet bar for Pro/Enterprise` — TODO
- [x] `Image paste no longer inserts trailing space` — DONE in 1decbda
- [x] `Pasting !command enters bash mode` — DONE (already in codebase, PromptInput.tsx:1206)
- [x] `/buddy April 1st creature` — DONE (already in our fork via BUDDY flag)
