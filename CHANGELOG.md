# Changelog

## 07.04.2026

- `03f2a23` Implemented KAIROS persistent assistant mode — `/assistant on` activates daily append-only logs, proactive tick loop, BriefTool as primary output, and autoDream consolidation. Gate always true, autoDream enabled by default (bypasses `tengu_onyx_plover`). Added `/dream` skill for manual 4-phase memory consolidation. Cross-reference analysis of ccleaks.com + ccunpacked.dev vs codebase saved to `context/cross-reference-analysis.md`
- `70174e6` Enabled LSP tool (860-line, 9 operations), fixed autoDream KAIROS gate exclusion, unhided `/heapdump`. Audit found FORK_SUBAGENT already working (211 lines in AgentTool), BUDDY already rendering (18 species), ULTRAPLAN 70% but needs OAuth
- `b9cfb92` Refactored `/ultraplan` from CCR remote sessions to local forked agent — no OAuth/login needed, uses `runForkedAgent()` + `ExitPlanModeScanner`, spawns planning agent locally with parallel sub-agents
- `8c9dcf4` Implemented local voice mode via faster-whisper — persistent Python STT worker at `~/.claude/voice-stt/`, length-prefixed PCM protocol, auto-installs venv + model on first `/voice`. Original Anthropic voice_stream preserved behind `VOICE_STREAM_BASE_URL`

## 06.04.2026

- `4a62f06` Added proactive tick loop feature notice (4 sessions)
- `0272c1d` Implemented proactive tick loop — `--super` and `--proactive` now have a working autonomous agent mode with `<tick>` messages, Sleep tool for pacing, pause/resume via Esc, and automatic turn-completion detection
- `94ad446` Fixed `--super` permission bypass not working with `--resume` (destructure timing)
- `3227e2c` Fixed autocomplete not clearing on empty input — suggestions stayed open after `/clear` or backspace. Also fixed thinking block gate in Message.tsx that broke interactive mode
- `614c883` Updated ghidra-re skill — `import_file` runs `analyzeHeadless` directly, no curl needed
- `483abc8` Ghidra headless import + permission fix — `chmod +x` on scripts after zip extraction, `import_file` uses `/load_program` to open binary in server
- `9f89796` 5% chance Clawd has a little extra between his legs
- `9bba5a3` Restored MCP registry stub — telemetry-only, not needed in this fork
- `8747b45` Fixed thinking block rendering — Message.tsx was filtering out thinking blocks before they reached the display component. Now shows reasoning inline when "Show reasoning" is enabled
- `5587518` Added inline reasoning display — new "Show reasoning" toggle in `/config`, thinking support for z.ai/DeepSeek (sends `type: "enabled"` not `adaptive`), explicit `type: "disabled"` for providers with default-on thinking, `showThinking` setting in settings.json
- `f5f010a` Robust MCP server installation — all three (browser, ghidra, computer-use) now install and connect reliably. Fixed broken pip venv auto-recreation, proper dep verification with retry, npm install for computer-use (npx --prefix broken), MCPSettings shows loading state instead of dismissing, Ghidra flat classpath launcher
- `4ccf522` Fixed MCPB manifest schema — `McpbManifestSchema` moved to `vAny` namespace in `@anthropic-ai/mcpb`, was breaking all MCPB plugin installs including computer-use MCP
- `1d1ae0d` Fixed MCP setup race conditions — MCPSettings 5s delay before "no servers" dismiss, browser dep check includes `mcp` package, computer-use switched to MCPB-only (npm installs were broken), Ghidra headless launcher fixed (flat classpath, no module system), `application.properties` health check, zip kept for re-extraction recovery
- `08e9d47` Completed full 1:1 CLIProxyAPI fingerprinting parity — wired thinking signature cache (3h TTL), proxy header scrubbing (`X-Forwarded-*`, `Sec-Ch-Ua-*`, `Sec-Fetch-*`, etc.), `X-Stainless-Retry-Count`, `Anthropic-Dangerous-Direct-Browser-Access`, `Connection: keep-alive`. Verified against claude-code-proxy + openclaw-billing-proxy — both lack most features we have
- `e644bb6` Added CLIProxyAPI fingerprinting — device profile stabilization (7d TTL), fake user IDs (`user_{hex}_account_{uuid}_session_{uuid}`, 1h cache), session ID caching (1h), sensitive word obfuscation (U+200B), cloaking system (auto/always/never). All configurable via `fingerprint.json`
- `345a595` Added dynamic /model picker — queries `ANTHROPIC_BASE_URL/v1/models` for available models, falls back to hardcoded list. Pretty display names from API (e.g. `GLM-4.7` not `glm-4.7`), sorted newest first. /model selection updates logo immediately
- `01ee9f4` Added live API model display — logo/status line shows actual model from API response + provider domain (e.g. `GLM-4.7 (api.z.ai)`), updates reactively on every response
- `cae8e84` Resilient MCP installs — verify deps on every startup (import check), retry pip if missing. Fixes ghidra pip silently failing
- `4a5f246` Fixed startup hang — COMMANDS() array missing .filter(Boolean), null pr_comments command crashed meetsAvailabilityRequirement
- `c57f843` Pinned lru-cache to 11.2.7 (newer versions use top-level await, breaks bun --compile)
- `8407941` Populated all 34 stub prompt files from Piebald v2.1.91 extraction — claude-api skill (26 .md), verify skill (3 .md), new Agent Design Patterns skill, memory attachment prompt v2.1.91, MagicDocs stubbed, /pr-comments nulled. 7478 lines added
- `e33e717` Fixed YOLO classifier — force external permissions template (ant template was wrong extraction)
- `f0b3352` Fixed /mcp dialog freeze — local JSX commands now register as overlays, disabling typeahead/autocomplete keybindings that stole up/down/esc. Also clears suggestion list when dialog opens
- `90fc452` Fixed mouse copy — fullscreen defaults off for all users (ant was defaulting on, enabling DEC 1003 mouse tracking)
- `97afd0f` Reverted Ghidra to Python launcher + bridge (in-process TS bridge crashed React by stealing stdio)
- `33fbd2e` Added MCP server health verification and self-healing — spawns server, checks MCP handshake, nukes broken installs for auto-repair on next startup
- `1884b5a` Added download resume support — Range header for interrupted downloads, .incomplete files, Content-Length verification. Ghidra 400MB zip was silently truncating
- `9e28e0a` Fixed browser MCP missing pip install -e ., fixed large zip extraction (python3 fallback for >50MB)
- `ad43d65` Fixed slash command autocomplete — commands with undefined names (null stubs) crashed generateCommandSuggestions silently, killing the entire suggestion pipeline
- `308414e` Removed CLAUDE_CODE_NO_FLICKER=0 from docker-compose files (was disabling fullscreen)
- `7e02694` Disabled all three feedback surveys (session, memory, post-compact) — telemetry is stubbed
- `6d94a23` Added NEVER rule to CLAUDE.md — don't run untested binaries in live session container
- `441cc16` Fixed useBuiltinMcpServers — static import instead of require() in render body (was breaking React hooks ordering, may have caused slash command autocomplete failure)
- `5a908af` Added prompt cache expiry hint — shows '~Xk uncached · /clear to start fresh' when returning after 1h cache TTL with >50K tokens (last 2.1.92 TODO)
- `90d72cc` Applied upstream 2.1.92 changes: removed tengu_attribution_header killswitch (always enabled), added CLAUDE_CODE_SKIP_FAST_MODE_ORG_CHECK and CLAUDE_REMOTE_CONTROL_SESSION_NAME_PREFIX env vars, added binary extraction section to protocol doc
- `228e476` Added unified upstream update protocol (context/upstream-protocol.md) — covers all 4 sources (Anthropic changelog, Piebald-AI prompts, minzique RE, CLIProxyAPI), step-by-step procedure, cross-reference table, quick commands

## 05.04.2026

- `05d07dc` Async MCP server setup — all three built-in servers install/connect after UI renders via useBuiltinMcpServers hook. Non-blocking startup, notifications on connect. Dockerfiles stripped of all MCP installs
- `c211c21` Ghidra MCP bridge now runs in-process via InProcessTransport (same pattern as Chrome MCP) — no Bun/Python subprocess needed, works in compiled binary
- `3ac1576` Replaced Python Ghidra bridge with TypeScript — 1:1 port of bridge_mcp_ghidra.py (1425 lines), uses @modelcontextprotocol/sdk, starts Java server itself. Ghidra MCP no longer requires Python
- `5119670` Unified MCP install helpers — shared downloadFile/extractZip/extractTarGz/downloadGitHubRepo. Browser MCP now uses GitHub API tarball (no git dependency). All pip calls use python3 -m pip
- `c0e85f3` Replaced all bash/python calls in Ghidra MCP setup with native JS — axios for downloads, fflate for zip/tar.gz extraction. Zero shell dependencies for install
- `4f7570f` Updated internal ghidra-re skill to v1.2 for GhidraMCP v5.0.0 — V6 protocol, 158 tools, set_variables, breaking changes documented
- `4a50b60` Fixed GhidraMCP bridge race condition — launcher waits for Java server to be ready before exec'ing bridge (was showing 7 tools, now 158+)
- `0155b57` Fixed GhidraMCP extension extraction path (double-nesting), use Python unzip instead of bash
- `fcbccae` Upgraded GhidraMCP from v4.2.0 to v5.0.0 — downloads pre-built release (no Maven), Python launcher (no bash), naming convention enforcement, completeness scoring redesign, 3 new tools
- `77e6ec7` Added MCPB fallback for computer-use MCP — downloads .mcpb from GitHub releases via existing plugin pipeline when npm unavailable
- `f735d48` Removed npx fallback from computer-use MCP — local install only
- `f741364` Moved all built-in MCP server installs from hardcoded /opt/ to ~/.claude/mcp-servers/ — browser, ghidra, computer-use. JDK detection checks JAVA_HOME → PATH (any 21+) → portable Temurin download (x64/arm64, linux/mac). Computer Use now npm-installs locally instead of npx-y every run. Added OPENCLAUDE_SKIP_MCP_INSTALL=1 env var to disable
- `feebccd` Replaced sharp and turndown stubs with real packages — sharp 0.34.5 (native image resizing works), turndown 7.2.4 (WebFetch HTML→markdown works)
- `e6bdd4e` Populated 3 empty .txt prompt files from upstream bundle — permissions_anthropic.txt (14K ant-only YOLO classifier rules), ultraplan/prompt.txt (multi-agent planning prompt). Previously 0-byte files that only worked in compiled builds
- `ec77e4a` Fixed color-diff-napi stub missing render() causing "REPL entered fallback mode" crash — stub now re-exports from native TS port at src/native-ts/color-diff/ instead of broken no-op classes
- `24b057e` Updated ghidra-re skill to v1.1 and browser-automation skill to v1.2 from external repos — 7-phase Ghidra workflow, expanded error handling/pitfalls, 9 bundled reference files, self-refinement protocols, authenticated proxy docs
- `728a072` Fixed shift+tab mode cycling stuck on default — ant-specific carousel only had bypassPermissions/auto (both gated), removed ant branch so full carousel works: default → acceptEdits → plan → bypassPermissions → default. Also made bypass permissions always available for USER_TYPE=ant
- `a9bd302` Fixed startup notices showing all 6 at once — now shows only the most recent eligible notice, auto-rotates as each expires after N sessions
- `8b6da6e` Removed settings seeding and MCP auto-registration from both Dockerfiles — users configure their own
- `7c9f9c9` Added Dockerfile.interactive + docker-compose.interactive.yml for manual use/testing — full-featured container with bash shell, writable rootfs, Docker socket, no autonomous mode
- `41a99e0` Restored MCP official registry fetch (previously stubbed), removed CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC guard, added open modelcontextprotocol.io registry — both fetched in parallel on startup via Promise.allSettled
- `69867f3` Added centralized fingerprinting config mirroring CLIProxyAPI (`src/config/claudeFingerprint.ts`), implemented CCH body signing via xxHash64 (`src/services/api/cchSigning.ts`), added reference doc (`context/fingerprinting.md`) with update procedure and cross-reference table
- `d406425` Added Computer Use MCP feature notice (4 sessions), updated CLAUDE.md convention: notices must be in same commit as feature
- `0625930` Replaced CHICAGO_MCP (Anthropic internal, macOS-only, disabled) with open-source domdomegg/computer-use-mcp — cross-platform, runs via `npx -y computer-use-mcp`, MIT licensed. Transparent replacement: server name `computer-use` and tool `mcp__computer-use__computer` unchanged. Removed in-process server intercept from client.ts
- `c1784ad` Disabled anti-distillation fake tool injection (`anti_distillation=['fake_tools']` removed from API requests). Converted connector text summarization from hardcoded ant+GrowthBook to user setting `connectorTextSummarization` in settings.json (off by default)
- `850256f` Backported 2 upstream UI fixes: click-to-expand hover text uses themed `color="inactive"` instead of `dimColor` for light theme visibility (2.1.90), tab headers in /model /config use `flexShrink=0` unconditionally so they don't disappear on scroll (2.1.90). Also confirmed 3 items already in codebase: auto mode denied commands notification + /permissions retry, task notifications on Ctrl+B, named subagents in @ typeahead
- `c77f13e` Fixed /release-notes version picker for our changelog format — terminal-height-aware scrolling, note truncation, j/k scroll within versions, bullet count in sidebar
- `64c457b` Backported 7 upstream features/fixes: /release-notes interactive version picker (2.1.92), @ typeahead ranks source files above MCP resources (2.1.89), /resume parallel project loading (2.1.90), --resume crash on older transcript format — filter orphaned tool_results (2.1.89), /claude-api skill guidance for agent design patterns (2.1.91), confirmed /usage Sonnet bar + deferred tools delta already in codebase
- `653d2b6` Backported 4 more upstream fixes: transcript writes re-queue on failure instead of silently losing entries on --resume (2.1.91), system-reminder text block prepended for image-only SDK messages so skill reminders aren't dropped (2.1.89), /feedback explains why unavailable instead of hiding (2.1.91), --resume picker filters -p/SDK sessions by entrypoint (2.1.90)
- `bb4fad9` Backported 4 upstream fixes: cmd+delete (super+backspace) deletes to line start on iTerm2/kitty/WezTerm/Ghostty/Windows Terminal (2.1.91), /cost shows per-model + cache-hit breakdown for subscription users (2.1.92), LSP server auto-restarts on next request after crash instead of staying dead (2.1.89), /stats counts subagent sidechain token usage from main session file (2.1.89)
- `24fffc1` Backported 2 upstream fixes: misleading esc hints suppressed in fullscreen when text selection exists (2.1.92), Bash tool warns when formatter/linter commands (`prettier --write`, `eslint --fix`, `black`, etc.) modify previously-read files and auto-refreshes readFileState (2.1.89)
- `7b8f28c` Backported 4 upstream fixes + populated auto mode classifier prompts: tmux subagent spawning permanent failure after windows killed (stable `#{window_id}` + cache invalidation), plugin MCP servers stuck "connecting" on duplicate claude.ai connectors (dedup handles pending state), MCP tool schema cache-key performance (memoize `jsonStringify` on tool object), auto mode classifier `.txt` prompts populated with upstream content (were empty — classifier ran without system prompt)
- `2d14581` Backported 5 upstream fixes: prompt-type Stop hooks only set preventContinuation for Stop events (2.1.92), ctrl+e no longer jumps to next line at wrapped-line boundary (2.1.92), permission dialog crash on malformed tool input caught by try/catch (2.1.90), idle-return hint shows last request's input tokens instead of cumulative total (2.1.92), entitlement 429s now show actual error for all users not just subscribers (2.1.89)
- `b812c7e` Added auto-updater GitHub Releases integration — compiled binaries now route to `AutoUpdater` → `installGlobalPackage()` → GitHub Releases instead of broken Anthropic native installer (GCS). Includes: compile-time version injection via `--define`, native installer GitHub fallback with SHA256 verification, push-to-main CI builds, manifest.json in releases, GITHUB_TOKEN auth header for rate limit hardening
- `1839702` Improved SSE transport large frame handling — quadratic → linear string accumulation via array chunks (backport from 2.1.90)
- `79b1753` Improved SDK transcript write performance — array accumulation in `drainWriteQueue` reduces GC pressure (backport from 2.1.90)
- `861dbd0` Fixed tool input validation for streaming JSON strings — coerce stringified arrays/objects before Zod validation (backport from 2.1.92)
- `0673875` Improved Edit tool — shorter `old_string` anchors hint now shown to all users, not just ant (backport from 2.1.91)
- `24c7f5b` Backported 5 upstream fixes: LRU cache memory leak (hash-based keys in `parseJSONCached`), Edit/Read allow rules check symlink targets, Edit/Write format-on-save hooks (refresh `readFileState` mtime after PostToolUse hooks), infinite loop rate-limit options dialog (module-level guard), Write tool diff speed ~60% faster (`getPatchFromContents` direct path)
- `1d66372` Fixed PreToolUse hooks with JSON stdout exit code 2 — use stdout when hook outputs JSON and exits with code 2 instead of falling back to stderr (backport from 2.1.90)
- `40965ea` Fixed hook `file_path` not absolute for Write/Edit/Read — normalize `tool_input.file_path` to absolute path in PreToolUse/PostToolUse/PostToolUseFailure hooks (backport from 2.1.89)
- `ec02901` Fixed `cleanupPeriodDays: 0` now rejected with validation error — changed schema from `.nonnegative()` to `.positive()`, directs users to `--no-session-persistence` (backport from 2.1.89)
- `1decbda` Fixed image paste inserting trailing space — disabled `pendingSpaceAfterPillRef` arming after image pill insertion (backport from 2.1.89)
- `8743d66` Added feature notice system — individual startup notices for major features (Ghidra MCP, Browser MCP, /super, multi-provider API, backports) in `src/components/LogoV2/`. Auto-dismiss after N sessions. Convention added to CLAUDE.md
- `9558634` Improved version display — dynamically fetches latest date + commit SHA from coffeegrind123/changelog at startup (e.g. "05.04.2026 (9de31ec)"). Disabled Opus 1M merge notice and npm deprecation notice
- `9de31ec` Backported 13 upstream features from 2.1.89–2.1.91 (via fazxes/Claude-code diff): `disableSkillShellExecution` setting, MCP `maxResultSizeChars` 500K override, multi-line deep links, plugin `bin/` executables on PATH, `Bun.stripANSI` optimization (new `stripAnsi.ts` + 12 import rewrites), `.husky` protected directory, DNS commands removed from PowerShell auto-allow, `KEEP_MARKETPLACE_ON_FAILURE` env var, `defer` permission in hooks, autocompact actionable error, MCP tool errors all content blocks, Edit works on Bash-viewed files (`cat`/`sed`/`head`/`tail`), hook output >50K saved to disk
- `b4ef4b3` Fixed copy/paste broken in container REPL — `USER_TYPE=ant` enables fullscreen (alt-screen + mouse tracking) by default, capturing all mouse events. Set `CLAUDE_CODE_NO_FLICKER=0` to opt out
- `0396781` Fixed REPL fallback mode crash — guard `getCommandName()` in useTypeahead.tsx against null/nameless commands from MCP stubs
- `968d071` Added DeepSeek API support — pass `ANTHROPIC_MODEL` and `ANTHROPIC_DEFAULT_HAIKU_MODEL` through docker-compose.yml

## 04.04.2026

- `961b400` Fixed interactive mode REPL hang — bypassed `showSetupScreens()` which deadlocks in Bun's async function entry; fixed 8 command stubs (buddy, fork, peers, torch, workflows, etc.) exporting `{}` instead of `null` which crashed `getCommandName()`
- `511a47a` Fixed container hang root cause — 16 tool stubs exported `{}` instead of `null`, crashing `getTools()` when `.isEnabled()` was called on empty objects; switched Ghidra MCP `await import()` to `require()` to avoid Bun ESM dynamic import deadlock inside Commander action handler; removed `CLAUDE_CODE_SIMPLE=1` workaround from docker-compose.yml
- `ead3133` Fixed container hang — root cause: non-bare startup hangs on hooks/LSP/plugin sync without TTY. Fix: `CLAUDE_CODE_SIMPLE=1` in docker-compose.yml skips these while keeping MCP/skills/core available. `CLAUDE_AUTO_TRUST=1` skips blocking setup screens. `-p` mode now works, interactive REPL needs `docker exec -it` with TTY
- `4215d78` Fixed Bun 1.3.11 rejecting TypeScript syntax in `.js` stubs — stripped type annotations from 4 ant-package stubs. Added `ANTHROPIC_API_KEY` passthrough in docker-compose.yml (confirmed `--bare` mode works with z.ai proxy)
- `182e4e8` Fixed color-diff-napi broken re-export path — self-contained stub replacing native-ts import that broke in node_modules copy. Reordered Dockerfile: COPY after JDK/Ghidra/zendriver downloads so source changes don't re-download 486MB+
- `0b6f32f` Fixed rendering hang — ported `stdinKeepAlive` from oboard/claude-code-rev to `ink/components/App.tsx` (stdin.ref on mount, guards raw mode ref/unref), added `ReplRuntimeBoundary` error boundary in REPL.tsx, `BootstrapBoundary` in App.tsx, try/catch in onInit(). Prevents blank screen when stubs throw during render.
- `0b6f32f` Upgraded 5 ant-package stubs from empty exports to full typed implementations — `@ant/computer-use-input` (93 lines), `@ant/computer-use-mcp` (195 lines, 22 tool defs), `@ant/computer-use-swift` (297 lines), `@ant/claude-for-chrome-mcp` (113 lines, 17 tool defs), `color-diff-napi` (rewired to native-ts reimplementation)
- `0b6f32f` Added `.dockerignore` — excludes node_modules/dist/.git, reduces build context from 70MB to 16MB
- `1f5cc49` Fixed interactive mode hanging — MCP server connections (browser + Ghidra) were blocking UI. Set `MCP_CONNECTION_NONBLOCKING=1` at entrypoint so servers connect in background while UI appears immediately.
- `5e90ef4` Reverted 194 import rewrites — use `node_modules/bundle/` polyfill instead (matching beita6969/claude-code approach). Bun resolves `from 'bun:bundle'` via `node_modules/bundle/index.js` created by `scripts/postinstall.sh`. Zero source modifications for feature flags.
- `bc0aff2` Added `CLAUDE_AUTO_TRUST=1` env var — auto-accepts workspace trust dialog and auto-approves all API keys. Set at entrypoint. Eliminates the two interactive prompts blocking headless/container execution.
- `de873e9` Fixed `MACRO is not defined` crash — added runtime MACRO global definition at entrypoint (VERSION, BUILD_TIME, PACKAGE_URL etc. normally inlined at compile time). Fixed 8 missing ant-only imports: getAntModelOverrideConfig (3 files), resolveAntModel (5 files), getAntModels (1 file).
- `1ddf503` Fixed 8 module stubs crashing at runtime when all feature flags enabled — added no-op exports to assistant/index.ts, assistant/gate.ts, proactive/index.ts, proactive/useProactive.ts, dream.ts, hunter.ts, runSkillGenerator.ts, WorkflowTool/bundled/index.ts
- `042cf5e` Fixed root privilege check blocking `--dangerously-skip-permissions` in container — added `IS_SANDBOX=1` env var
- `042cf5e` Changed sandbox from `-p` (headless) to `--append-system-prompt` (interactive, proactive tick loop keeps agent working)
- `569d2bf` Fixed sandbox build: use `bun run` wrapper instead of compiled binary (`bun build --compile` can't use runtime feature polyfill), install Bun to `/usr/local` (survives /root bind mount)
- `569d2bf` Added 6 stub modules for compile: cli/bg.ts, cli/handlers/templateJobs.ts, daemon/main.ts, daemon/workerRegistry.ts, environment-runner/main.ts, self-hosted-runner/main.ts
- `6a032f7` Added `CLAUDE_PROMPT` env var passed via `--append-system-prompt` for autonomous task injection
- `08ba78a` Fixed sandbox Dockerfile: added missing Claude Code install, fixed bashrc self-reference loop, moved workspace seeding to startup script (bind mount shadows image layers at /root)
- `6f6d583` Added `Dockerfile.sandbox` — locked-down container for autonomous self-development with `claude --super`
- `da56f24` Added `docker-compose.yml` reading `.env` for z.ai auth, GitHub PAT, workspace mount
- `301870e` Security hardening: read-only rootfs, `--cap-drop=ALL`, `no-new-privileges`, 8GB memory cap, 4 CPU cap, 256 PID limit, GitHub access scoped via fine-grained PAT
- `befc4f6` Added `CLAUDE.md` project guide with changelog rules, architecture decisions, debugging guide
- `befc4f6` Added release notes system pointing to public `coffeegrind123/changelog` repo with date-based version support
- `9371826` Rewrote auto-updater to use GitHub Releases instead of npm/GCS — downloads compiled binary directly
- `fd950da` Added `bootstrap.sh` installer and GitHub Actions build workflow for 4 platforms
- `5005d1d` Added startup notification when MCP server dependencies are missing
- `ddbc00d` Added full auto-install chain for Ghidra MCP — JDK 21, Ghidra 12.0.3, GhidraMCP jar, bridge scripts
- `6ffda9b` Added smart dependency detection for browser and Ghidra MCP — skips gracefully without deps
- `8408a02` Integrated Ghidra MCP as built-in server + bundled `/ghidra-re` skill (193 tools)
- `90e2f9d` Integrated zendriver-mcp browser as built-in MCP + bundled `/browser-automation` skill (48 tools)
- `bbd13c3` Disabled all built-in browser/web tools — replaced by external MCP server as sole provider
- `67b0840` Added `--super` CLI flag and `/super` slash command for fully autonomous mode
- `ec3d0f0` Added `/proactive`, `/assistant`, `/coordinator`, `/dump-prompt` slash commands
- `394f06f` Removed `CYBER_RISK_INSTRUCTION` system prompt injection
- `394f06f` Disabled domain blocklist, metrics check, MCP registry prefetch, SSRF guard
- `394f06f` Set `USER_TYPE=ant` and `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` at entrypoint
- `d2e5a29` Replaced `bun:bundle` across 194 files with runtime feature module — all 87 flags enabled

## 03.04.2026

- `7357ffb` Neutralized all product telemetry — 10 files replaced with no-op stubs preserving 1,019 call sites
- `7357ffb` Disabled GrowthBook, remote killswitches, version enforcement, auto-update caps
- `ce7532e` Eliminated 12 npm dependencies with inline vendor modules
- `ce7532e` Added `DEPENDENCY-AUDIT.md` with security analysis of 55 remaining dependencies

## 31.03.2026

- `15fb6a5` Initial buildable research fork of Claude Code source
