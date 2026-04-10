# Changelog

## 11.04.2026

- `a1c7c6e` Improved brief mode to retry once when Claude responds with plain text instead of structured SendUserMessage
- `e9f6195` Added Monitor tool for streaming events from background scripts — real-time stdout→notification with 200ms batching, rate limiting, persistent mode, task detail dialog, permission request component
- `a6a5ba4` Fixed FuzzyPicker crash on arrow keys when item list is empty — guard against `clamp(i, 0, -1)` in `step()` and `useEffect`
- `a6a5ba4` Fixed resume picker: task-summary entries replacing conversation summaries — renamed `summary` field to `taskStatus` in `saveTaskSummary` to avoid collision with `extractLastJsonStringField`
- `a6a5ba4` Fixed resume picker: filter toggle wiping search state — `loadLogs` no longer sets loading spinner on filter reloads, preventing LogSelector unmount/remount
- `a6a5ba4` Fixed resume picker: `--resume <name>` opening with uneditable search — initialize `viewMode` to `"search"` when `initialSearchQuery` is provided
- `a6a5ba4` Fixed file-edit diffs disappearing on `--resume` for files >10KB — `UserToolSuccessMessage` now falls through with raw data when `outputSchema.safeParse` fails instead of returning null
- `a6a5ba4` Improved Vim mode: j/k in NORMAL mode now navigate history and select footer pill at input boundary — detects first/last line and delegates to base handler
- `7b8eef4` Added ● N running indicator in `/agents` next to agent types with live subagent instances — counts running/pending tasks from AppState
- `7b8eef4` Improved `/resume` filter hint labels — shows worktree directory name instead of generic "current worktree" text
- `ed80f5a` Fixed `ctrl+]`, `ctrl+\`, `ctrl+^` keybindings not firing in terminals sending raw C0 control bytes — extend parse-keypress to handle 0x1c-0x1e
- `ed80f5a` Fixed `permissions.deny` rules not overriding PreToolUse hook `permissionDecision:ask` — check deny rules before passing hook's ask to canUseTool
- `ed80f5a` Fixed RemoteTrigger tool `run` action sending empty body — use provided body param or omit data
- `ed80f5a` Fixed `/btw` writing entire conversation to disk on every use — set `skipTranscript` on side questions
- `eeca77b` Fixed crash when `settings.json` env values are numbers instead of strings — `filterSettingsEnv` now coerces all values via `String()` before `Object.assign` to `process.env`
- `fd58648` Improved settings resilience: unrecognized hook event name in `settings.json` no longer causes entire file to be ignored — `HooksSchema` key changed from `z.enum(HOOK_EVENTS)` to `z.string()`
- `2569482` Fixed command injection vulnerability in POSIX `which` fallback — replaced shell-interpolated `execa(\`which ${command}\`)` with `execa('which', [command])` and `execFileSync('which', [command])`
- `2569482` Fixed crash on `--resume` when persisted Edit/Write tool result missing `file_path` — added optional chaining for `filePath?.startsWith` and `originalFile?.split`
- `167cb90` Improved tool-not-available errors — now explains why (MCP server disconnected, mode/feature requirement) instead of just "No such tool available"
- `167cb90` Improved refusal error messages — includes API-provided explanation text extracted from content blocks before refusal stop_reason
- `b60045d` Fixed hardcoded 5-minute non-streaming fallback timeout ignoring `API_TIMEOUT_MS` — changed default from 300s to 600s to match streaming client
- `77ff208` Fixed `--setting-sources` without `user` causing cleanup to ignore `cleanupPeriodDays` — falls back to user settings directly
- `3554670` Fixed `claude -w <name>` failing with "already exists" after stale worktree cleanup — removes stale directories before `git worktree add`
- `98731af` Improved rate-limit retry messages — shows limit type (from `anthropic-ratelimit-unified-limit-name`) and reset time instead of opaque countdown
- `ff9a9b3` Improved `claude -p --resume <name>` — now accepts session titles from `/rename` or `--name` via `searchSessionsByCustomTitle` fallback
- `ff9a9b3` Fixed `claude --continue -p` not continuing `-p`/SDK sessions — bypasses `isNonInteractive` enrichment filter via direct `fetchLogs(1)`
- `ff9a9b3` Fixed `/login` OAuth URL padding preventing clean mouse selection
- `f7ea957` Improved plugin hooks from force-enabled plugins to run when `allowManagedHooksOnly` is set — checks `getManagedPluginNames` before skipping
- `fcb0b30` Improved focus mode: Claude writes self-contained summaries — `BriefTool` prompt instructs that user only sees `SendUserMessage` output
- `defb5cf` Fixed sub-agents in worktrees denied Read/Edit access — `allWorkingDirectories()` now includes `getCwd()` (async-local override) so worktree paths are recognized
- `f4b49cc` Improved `/plugin` and `claude plugin update` — warns when marketplace could not be refreshed instead of silently reporting stale version
- `295ecea` Fixed `/context` Free space and Messages breakdown disagreeing with header percentage — reconcile Free space with API usage total
- `295ecea` Fixed in-app settings writes not refreshing in-memory snapshot — `resetSettingsCache()` now clears `pluginSettingsBase`
- `55059e8` Fixed `/mcp` menu offering OAuth actions for `headersHelper` servers — shows Reconnect instead to re-invoke the helper script

## 10.04.2026

- `13b5000` Added cut/paste/column/awk/gawk/mawk to Bash COMMAND_ALLOWLIST — fixes false permission prompts for `cut -d /`, `paste -d /`, `column -s /`, and awk commands. Fixed `%` in filenames triggering false dangerous-redirect detection (now only flags Windows `%VAR%` patterns)
- `13b5000` Fixed compound Bash commands bypassing forced permission prompts in auto/bypass modes — deny rule check now runs on full compound command after pipe operator returns 'allow'
- `13b5000` Fixed read-only commands with env-var prefixes not prompting — `stripSafeWrappers` now runs in `isCommandReadOnly` so safe vars are stripped before read-only check (unsafe vars still prompt)
- `13b5000` Fixed Bash deny rules downgraded to ask for piped cd commands — per-segment deny checks now run before cd+git ask in `segmentedCommandPermissionResult`
- `13b5000` Improved pasted/attached image token budget — added `compressImageBufferWithTokenLimit` to clipboard paste and attachment paths, matching Read tool's 25K token budget
- `e9b0c9d` Improved Accept Edits mode — auto-approves filesystem commands prefixed with safe env vars or process wrappers (`NODE_ENV=prod rm file` now works)
- `e9b0c9d` Fixed `permissions.additionalDirectories` changes not applying mid-session — `applySettingsChange` now rebuilds directory map from fresh settings while preserving CLI-added directories
- `e9b0c9d` Added `--exclude-dynamic-system-prompt-sections` flag for print mode — excludes user-specific system prompt sections for improved cross-user prompt caching
- `e9b0c9d` Fixed managed-settings allow rules persisting after admin removal — `policySettings` now cleared in `syncPermissionRulesFromDisk` before re-applying fresh rules
- `33c3cd1` Fixed `--dangerously-skip-permissions` being silently downgraded to `acceptEdits` after approving write to protected path — `setMode` suggestion now only generated when current mode is `default` or `plan`
- `33c3cd1` Fixed removing directory from `additionalDirectories` revoking access to same directory passed via `--add-dir` — `removeDirectories` now preserves entries with `cliArg` or `session` source
- `8a6dd9e` Fixed agent team members not inheriting leader's permission mode — team members spawned in `bypassPermissions` mode now inherit that mode via `leaderPermissionMode` in spawn config
- `824cc2e` Fixed subagent worktree/cwd override leaking working directory back to parent session's Bash tool — `setCwd` now updates AsyncLocalStorage override instead of global `setCwdState` when inside `runWithCwdOverride` context
- `824cc2e` Fixed capital letters dropped to lowercase on xterm/VS Code with kitty keyboard protocol — infer shift flag from uppercase codepoints (65-90) in CSI u sequences, preserve uppercase in input text for shifted letters
- `824cc2e` Fixed Remote Control permission handler memory leak — `cancelRequest` now deletes handler from `pendingPermissionHandlers` map (previously only sent cancel to bridge, leaving closure alive for session lifetime)
- `824cc2e` Fixed MCP OAuth `authServerMetadataUrl` config override not honored on token refresh after restart — `discoveryState()` now checks config URL before cached state when issuer differs from cache
- `824cc2e` Improved auto mode and bypass-permissions mode to auto-approve sandbox network access prompts — `sandboxAskCallback` returns `true` immediately for `auto`/`bypassPermissions` modes
- `824cc2e` Fixed MCP HTTP/SSE connections accumulating ~50 MB/hr of unreleased buffers on reconnect — `onclose` handler now explicitly calls `transport.close()` to release SSE response bodies
- `07783d8` Fixed NO_FLICKER mode memory leak where API retries left stale streaming state — `StreamingToolExecutor.discard()` now called before `continue` on collapse-drain, reactive-compact, and max-output-tokens retry paths
- `9eb1902` Fixed messages typed while Claude is working not being persisted to transcript — concurrent query handler now adds user messages to React state via `setMessages` before re-enqueueing, so `useLogMessages` writes them to disk
- `d9432fc` Fixed crash in fullscreen mode when hovering over MCP tool results — added `parentNode` null check in `dispatchHover` before `onMouseEnter` (matching existing `onMouseLeave` guard)
- `d9432fc` Fixed copying wrapped URLs in fullscreen mode inserting spaces at line breaks — `extractRowText` now trims trailing spaces on soft-wrapped rows containing hyperlinked cells
- `d9432fc` Fixed custom status line not displaying in NO_FLICKER mode on terminals shorter than 24 rows — removed `isShort` guard from `PromptInputFooter.tsx` StatusLine render condition
- `c573e06` Fixed voice mode leaking space characters when re-holding push-to-talk key — swallow bare-char keypresses during `processing` state in `useVoiceIntegration.tsx`
- `c573e06` Improved `/reload-plugins` to pick up plugin-provided skills without restart — added `clearSkillCaches()` to `clearAllCaches()` in `cacheUtils.ts`
- `be20375` Fixed Shift+Enter and Alt/Cmd+arrow shortcuts not working in Warp with NO_FLICKER mode — added `WarpTerminal` to `EXTENDED_KEYS_TERMINALS` in `terminal.ts`
- `be20375` Fixed scroll rendering artifacts in NO_FLICKER mode inside zellij — disable DEC 2026 synchronized output when `ZELLIJ` env var is set
- `be20375` Fixed `claude plugin update` reporting "already at latest version" for git-based plugins — added `git pull --ff-only` before `calculatePluginVersion` in `pluginOperations.ts`

## 08.04.2026

- `6a7df35` Fixed compiled binary REPL hang — replaced all `await import()` with `require()` in Commander action handlers (`main.tsx`, `interactiveHelpers.tsx`, `dialogLaunchers.tsx`, `setup.ts`, `replLauncher.tsx`). Bun compiled binaries deadlock on dynamic import inside Commander callbacks
- `33e094d` Fixed compiled binary crash on `@ant/*` modules — removed `--external '@ant/*'` from build so stub packages get bundled. Previously the binary crashed with `Cannot find module '@ant/claude-for-chrome-mcp'`
- `a802b7b` Fixed Ink `patchStderr` swallowing all `process.stderr.write` output — disabled stderr interception (not needed without alt-screen)
- `2077965` Fixed Ink `createRoot` hang — made synchronous by removing `await Promise.resolve()` microtask yield
- `1980347` Fixed compiled binary REPL hang on startup — vendored ripgrep path was hardcoded to CI runner directory (`/home/runner/work/...`). Added fallback to system `rg` when vendor binary missing. Bootstrap auto-installs ripgrep
- `da8d2a0` Improved bootstrap.sh — auto-installs `libstdc++`/`libgcc` on musl/Alpine via `apk`
- `6a7df35` Improved compiled binary safety — added try/catch to `modifiers-napi` and `audio-capture-napi` external packages
- `b5de2f5` Added self-hosted release proxy on cs16.net — transparent GitHub Releases API mirror at `https://cs16.net/openclaude/`, auto-updater and bootstrap now default to cs16.net instead of api.github.com. Refactored binary download from `curl` subprocess to `axios`. Override with `OPENCLAUDE_UPDATE_ENDPOINT`
- `438e48e` Improved bootstrap.sh — added target argument (`stable`/`latest`/`VERSION`), SHA256 checksum verification via `manifest.json`, jq-optional fallback parser
- `6c299e5` Fixed CI artifact storage quota exhaustion — eliminated artifact upload/download, each matrix leg uploads binaries directly to GitHub Release via `gh` CLI. Manifest generated as separate job
- `4f26e89` Added musl/Alpine build targets — CI now produces 4 binaries: `linux-x64`, `linux-arm64`, `linux-x64-musl`, `linux-arm64-musl`. Bootstrap and auto-updater detect musl libc automatically
- `5f719c2` Fixed CI duplicate release race — only `linux-x64` matrix leg creates the release, others poll until it exists before uploading
- `16ec21b` Fixed collapsed search/read badge duplication in scrollback during parallel tool use and CLAUDE.md auto-load — `shouldRenderStatically` now returns true for completed collapsed groups. Added `writeToStdoutAsync` with drain backpressure to prevent pipe deadlock on 64KB+ NDJSON output (backport 2.1.89/90)
- `c15e26b` Fixed CJK/multibyte text corrupted with U+FFFD in stream-json mode — wrap `process.stdin` with `TextDecoder(stream:true)` to handle UTF-8 sequences split across chunk boundaries. Fixed partial assistant response lost on interrupt — flush accumulated `contentBlocks` before abort throw in `queryModel` (backport 2.1.94)
- `d08d839` Fixed `FORCE_HYPERLINK` env var ignored when set via `settings.json` env — added to `SAFE_ENV_VARS` so it's applied before hyperlink detection caches. Fixed alt-screen ghost lines from DECSTBM scroll when content height shrinks. Fixed hyperlinks opening two browser tabs in tmux — wrap OSC 8 with `wrapForMultiplexer()` (backport 2.1.94)
- `f96f807` Fixed Shift+Space inserting literal "space" in search inputs — handle `name='space'` in `keyFromParsed()`. Fixed multiline user prompts indenting wrapped lines under `❯` caret — use `Box flexDirection=row` to separate caret from text content (backport 2.1.94)
- `5380f82` Fixed agents appearing stuck after 429 rate-limit with long Retry-After — yield error message before sleeping in fast mode path of `withRetry.ts` (backport 2.1.94)
- `402e025` Added `keep-coding-instructions` frontmatter field for plugin output styles. Added `hookSpecificOutput.sessionTitle` to `UserPromptSubmit` hooks. Plugin skills now use frontmatter `name` for invocation name instead of directory basename (backport 2.1.94)

## 07.04.2026

- `41f8456` Added `/humanizer` dual-mode skill — `/humanizer` toggles session-wide humanizer mode (system prompt section applied to ALL output), `/humanizer [text]` for one-shot 29-pattern audit with draft→self-critique→revision. Ported from blader/humanizer (MIT). Complements undercover mode
- `8d07550` Fixed Sleep tool crash — call() returned wrong shape (`{type,text}` instead of `{data}`), mapper crashed on `content.text`
- `a386b74` Added undercover mode toggle to `/config` — `undercoverEnabled` setting (default: on) allows disabling AI attribution stripping in commits/PRs
- `9093779` Fixed Sleep tool crash — missing `mapToolResultToToolResultBlockParam` and Zod `inputSchema` (had raw JSON schema). Added `Sleep(5m)` duration display in tool name
- `d31a4ac` Fixed Sleep tool permanently disabled — `isEnabled()` used `isProactiveActive()` which returned false due to Bun dual module instance. Replaced with env var check. Model can now actually call Sleep on idle ticks
- `1c8875d` Fixed proactive Sleep/tick prompt never appearing — Bun's `feature()` from `bun:bundle` plugin was killing `getProactiveSection()` in prompts.ts (evaluated to false in nested function calls despite polyfill returning true). Replaced all `feature()` guards with direct env var check (`CLAUDE_CODE_PROACTIVE=1`). Also replaced module-level `require('../proactive/index.js')` with lazy function accessor (dual module instance issue). `/super` and `/proactive` now produce full "Autonomous work" prompt with Sleep/tick/pacing instructions
- `f85cf49` Fixed `/assistant` parity with `--assistant` — now sets brief mode (SendUserMessage), calls `initializeAssistantTeam()`, KAIROS addendum dynamically injected. `/proactive` now blocks in coordinator mode
- `bafc667` Removed redundant proactive/KAIROS prompt from systemPrompt.ts — prompts.ts is the authoritative source. KAIROS startup now activates proactive automatically
- `13565f0` Fixed `/super` and `/proactive` not activating proactive tick loop — both only set env vars but never called `activateProactive()` from the state machine
- `6302f39` Fixed `/proactive` and `/assistant` commands not appearing (Bun circular require), `/super` now sets bypassPermissions mode at runtime, added 7 missing settings to `/config` UI (verifyPlanEnabled, snipEnabled, autoDreamEnabled, autoMemoryEnabled, todoFeatureEnabled, voiceEnabled)
- `cdf4f99` Fixed missing `registerBundledSkill` import that silently killed the REPL on startup
- `a8ddf20` Added session ingress (transcript persistence with Last-Uuid concurrency), files API (multipart upload/download/list), and triggers API (CRUD + cron scheduler) to local CCR server — 11 new endpoints, 33 total
- `72202ad` Added local CCR server + BYOC/self-hosted runners — full Anthropic CCR API (~20 endpoints) as Bun HTTP server on localhost:3456, file-backed storage, v1+v2 protocol paths, SSE streaming. `claude ccr-server start/stop/status`, `claude submit "task"`, `claude environment-runner` (register/poll/spawn/heartbeat), `claude self-hosted-runner` (bridge credentials + SSE transport). BYOC_RUNNER + SELF_HOSTED flags now fully implemented
- `03f2a23` Implemented KAIROS persistent assistant mode — `/assistant on` activates daily append-only logs, proactive tick loop, BriefTool as primary output, and autoDream consolidation. Gate always true, autoDream enabled by default (bypasses `tengu_onyx_plover`). Added `/dream` skill for manual 4-phase memory consolidation. Cross-reference analysis of ccleaks.com + ccunpacked.dev vs codebase saved to `context/cross-reference-analysis.md`
- `70174e6` Enabled LSP tool (860-line, 9 operations), fixed autoDream KAIROS gate exclusion, unhided `/heapdump`. Audit found FORK_SUBAGENT already working (211 lines in AgentTool), BUDDY already rendering (18 species), ULTRAPLAN 70% but needs OAuth
- `b9cfb92` Refactored `/ultraplan` from CCR remote sessions to local forked agent — no OAuth/login needed, uses `runForkedAgent()` + `ExitPlanModeScanner`, spawns planning agent locally with parallel sub-agents
- `8c9dcf4` Implemented local voice mode via faster-whisper — persistent Python STT worker at `~/.claude/voice-stt/`, length-prefixed PCM protocol, auto-installs venv + model on first `/voice`. Original Anthropic voice_stream preserved behind `VOICE_STREAM_BASE_URL`
- `cee4eef` Implemented BUDDY speech bubbles (`sideQuery()` LLM quips, ~25% per turn), Snip Tool (fast history truncation, disabled by default via `snipEnabled`), and Workflow Tool (background agent workflows from `~/.claude/workflows/*.md`, built-in: `test-and-fix`, `lint-fix`)
- `d220110` Implemented daemon mode — `--bg` spawns tmux sessions with auto permission bypass, `claude ps/logs/attach/kill` for management, `claude daemon start/stop/status/restart` for supervised sessions with auto-restart (max 3 per 5min). State in `~/.claude/daemon-state.json`
- `1fc0202` Added tmux auto-install for daemon/bg mode — downloads prebuilt static binary from `tmux/tmux-builds` v3.6a to `~/.claude/bin/tmux` if system tmux not available. Supports linux-x86_64, linux-arm64, macos-x86_64, macos-arm64
- `abbb079` Implemented templates/jobs system — `claude new <template>` dispatches jobs from `~/.claude/templates/*.md`, job state tracked in `~/.claude/jobs/<id>/state.json` via classifier, `claude list` shows jobs, `claude reply` sends input, `claude daemon start --template` for supervised execution
- `8f60f43` Implemented 9 previously-disabled slash commands — `/env` (masked env vars), `/debug-tool-call` (raw JSON), `/good-claude` (easter egg), `/ctx_viz` (alias for `/context`), `/summary` (LLM session summary), `/bughunter` (adversarial bug finder skill), `/autofix-pr` (CI fix skill), `/share` (markdown export), `/teleport` (session state export/import)
- `b0f34a0` Refactored all 9 commands to production-quality TypeScript — proper `satisfies Command` descriptors, typed `LocalCommandCall`, path sanitization, schema validation, static imports
- `677eace` Implemented VerifyPlanExecution — background agent verifies approved plan vs actual implementation after ExitPlanMode. Checks git diff, verifies each item, runs tests, reports pass/partial/fail. Enabled via `CLAUDE_CODE_VERIFY_PLAN=true`, reminder every 10 turns, auto-allowed by classifier
- `bd768d2` Implemented PushNotification (terminal escape notifications for iTerm2/Kitty/Ghostty/bell) and SubscribePR (gh CLI polling for PR checks/reviews/merge with cron tasks, state in `~/.claude/pr-subscriptions/`). `/subscribe-pr` command lists active subscriptions

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
