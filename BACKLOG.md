# Upstream Backlog

Upstream features from anthropics/claude-code not yet implemented in OpenClaude.
Source: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md

Only entries after v2.1.87 (our fork base). Refresh by fetching:
`curl -fsSL https://raw.githubusercontent.com/anthropics/claude-code/refs/heads/main/CHANGELOG.md`

## 2.1.113

- [-] `Changed the CLI to spawn a native Claude Code binary (via a per-platform optional dependency) instead of bundled JavaScript` — SKIP (we build our own Bun-compiled binary; we don't use Anthropic's distribution pipeline)
- [x] `Added sandbox.network.deniedDomains setting to block specific domains even when a broader allowedDomains wildcard would otherwise permit them` — DONE in 6c8092c
- [x] `Fullscreen mode: Shift+↑/↓ now scrolls the viewport when extending a selection past the visible edge` — DONE in 6c8092c
- [x] `Ctrl+A and Ctrl+E now move to the start/end of the current logical line in multiline input, matching readline behavior` — DONE in 6c8092c
- [-] `Windows: Ctrl+Backspace now deletes the previous word` — SKIP (Linux container only)
- [x] `Long URLs in responses and bash output stay clickable when they wrap across lines (in terminals with OSC 8 hyperlinks)` — DONE in 6c8092c
- [-] `Improved /loop: pressing Esc now cancels pending wakeups, and wakeups display as "Claude resuming /loop wakeup" for clarity` — SKIP (our /loop is a static-cron skill; the dynamic /loop + ScheduleWakeup tool isn't in our fork, nothing to cancel)
- [-] `/extra-usage now works from Remote Control (mobile/web) clients` — SKIP (Remote Control infra)
- [-] `Remote Control clients can now query @-file autocomplete suggestions` — SKIP (Remote Control infra)
- [~] `Improved /ultrareview: faster launch with parallelized checks, diffstat in the launch dialog, and animated launching state` — PARTIAL in 6c8092c (parallel agents were already in place via Promise.all; diffstat now shown in the launch dialog; animated launching state not ported — our /ultrareview is a background task with a single system-message launch line, no slider component)
- [x] `Subagents that stall mid-stream now fail with a clear error after 10 minutes instead of hanging silently` — DONE in 6c8092c
- [x] `Bash tool: multi-line commands whose first line is a comment now show the full command in the transcript, closing a UI-spoofing vector` — DONE in 6c8092c
- [x] `Running cd <current-directory> && git … no longer triggers a permission prompt when the cd is a no-op` — DONE in 6c8092c
- [-] `Security: on macOS, /private/{etc,var,tmp,home} paths are now treated as dangerous removal targets under Bash(rm:*) allow rules` — SKIP (macOS-specific path rules)
- [x] `Security: Bash deny rules now match commands wrapped in env/sudo/watch/ionice/setsid and similar exec wrappers` — DONE in 6c8092c (also covers unshare, systemd-run, taskset, nocache, bwrap, chrt via stripLeadingExecWrapperForDeny)
- [x] `Security: Bash(find:*) allow rules no longer auto-approve find -exec/-delete` — DONE in 6c8092c (also -execdir, -ok, -okdir, -fprint, -fprintf)
- [-] `Fixed MCP concurrent-call timeout handling where a message for one tool call could silently disarm another call's watchdog` — SKIP (bug lives in @modelcontextprotocol/sdk's _onprogress/_cleanupTimeout; our outer wrapper in client.ts:3104-3156 already uses per-call Promise.race + independent setTimeout so concurrent calls don't share external watchdog state; a proper fix belongs upstream in the SDK package, patching node_modules is fragile)
- [-] `Fixed Cmd-backspace / Ctrl+U to once again delete from the cursor to the start of the line` — SKIP (no-op — our fork never applied the 2.1.111 "clear entire buffer" change; `useTextInput.ts:236` still maps Ctrl+U → killToLineStart → deleteToLineStart, matching the 2.1.113 fix)
- [x] `Fixed markdown tables breaking when a cell contains an inline code span with a pipe character` — DONE in 6c8092c
- [x] `Fixed session recap auto-firing while composing unsent text in the prompt` — DONE in 6c8092c
- [x] `Fixed /copy "Full response" not aligning markdown table columns for pasting into GitHub, Notion, or Slack` — DONE in 6c8092c
- [-] `Fixed messages typed while viewing a running subagent being hidden from its transcript and misattributed to the parent AI` — SKIP (requires a subagent-messaging pipeline — no sendMessageToAgent/deliverToAgent plumbing in our codebase — a significant feature addition beyond a bug backport)
- [x] `Fixed Bash dangerouslyDisableSandbox running commands outside the sandbox without a permission prompt` — DONE in 6c8092c
- [x] `Fixed /effort auto confirmation — now says "Effort level set to max" to match the status bar label` — DONE in 6c8092c
- [x] `Fixed the "copied N chars" toast overcounting emoji and other multi-code-unit characters` — DONE in 6c8092c
- [-] `Fixed /insights crashing with EBUSY on Windows` — SKIP (Windows-specific)
- [-] `Fixed exit confirmation dialog mislabeling one-shot scheduled tasks as recurring — now shows a countdown` — SKIP (our ExitFlow/WorktreeExitDialog doesn't warn about scheduled tasks — this fix targets a UI feature not present in our fork)
- [x] `Fixed slash/@ completion menu not sitting flush against the prompt border in fullscreen mode` — DONE in 6c8092c
- [x] `Fixed CLAUDE_CODE_EXTRA_BODY output_config.effort causing 400 errors on subagent calls to models that don't support effort and on Vertex AI` — DONE in 6c8092c
- [x] `Fixed prompt cursor disappearing when NO_COLOR is set` — DONE in 6c8092c
- [x] `Fixed ToolSearch ranking so pasted MCP tool names surface the actual tool instead of description-matching siblings` — DONE in 6c8092c
- [ ] `Fixed compacting a resumed long-context session failing with "Extra usage is required for long context requests"` — NEEDS INVESTIGATION (without upstream diff the root cause is speculative across several candidate paths: betas not re-added on resume, compact call not dynamically adding 1M beta, or 429 entitlement not handled with a fallback)
- [-] `Fixed plugin install succeeding when a dependency version conflicts with an already-installed plugin — now reports range-conflict` — SKIP (marketplace/plugin infra)
- [-] `Fixed "Refine with Ultraplan" not showing the remote session URL in the transcript` — SKIP (our ultraplan is local-only, no remote session URL)
- [x] `Fixed SDK image content blocks that fail to process crashing the session — now degrade to a text placeholder` — DONE in 6c8092c
- [-] `Fixed Remote Control sessions not streaming subagent transcripts` — SKIP (Remote Control infra)
- [-] `Fixed Remote Control sessions not being archived when Claude Code exits` — SKIP (Remote Control infra)
- [-] `Fixed thinking.type.enabled is not supported 400 error when using Opus 4.7 via a Bedrock Application Inference Profile ARN` — SKIP (Bedrock-specific)

## 2.1.112

- [-] `Fixed "claude-opus-4-7 is temporarily unavailable" for auto mode` — SKIP (Anthropic model routing, not applicable to our fork)

## 2.1.111

- [-] `Claude Opus 4.7 xhigh is now available! Use /effort to tune speed vs. intelligence` — SKIP (Anthropic model, auto-available via provider)
- [-] `Auto mode is now available for Max subscribers when using Opus 4.7` — SKIP (subscription gating)
- [x] `Added xhigh effort level for Opus 4.7, sitting between high and max. Available via /effort, --effort, and the model picker; other models fall back to high` — DONE in d8bb862
- [x] `/effort now opens an interactive slider when called without arguments, with arrow-key navigation between levels and Enter to confirm` — DONE in d8bb862
- [x] `Added "Auto (match terminal)" theme option that matches your terminal's dark/light mode — select it from /theme` — DONE (already implemented via AUTO_THEME feature flag, enabled in our fork)
- [x] `Added /less-permission-prompts skill — scans transcripts for common read-only Bash and MCP tool calls and proposes a prioritized allowlist for .claude/settings.json` — DONE in 6053180
- [x] `Added /ultrareview for running comprehensive code review in the cloud using parallel multi-agent analysis and critique — invoke with no arguments to review your current branch, or /ultrareview <PR#> to fetch and review a specific GitHub PR` — DONE in 6053180 (adapted to local forked agents)
- [-] `Auto mode no longer requires --enable-auto-mode` — SKIP (already unrestricted in our fork)
- [-] `Windows: PowerShell tool is progressively rolling out. Opt in or out with CLAUDE_CODE_USE_POWERSHELL_TOOL. On Linux and macOS, enable with CLAUDE_CODE_USE_POWERSHELL_TOOL=1 (requires pwsh on PATH)` — SKIP (PowerShell tool already exists in codebase, opt-in via env var)
- [x] `Read-only bash commands with glob patterns (e.g. ls *.ts) and commands starting with cd <project-dir> && no longer trigger a permission prompt` — DONE in 2396509
- [x] `Suggest the closest matching subcommand when claude <word> is invoked with a near-miss typo (e.g. claude udpate → "Did you mean claude update?")` — DONE in 2396509
- [x] `Plan files are now named after your prompt (e.g. fix-auth-race-snug-otter.md) instead of purely random words` — DONE in 2396509
- [x] `Improved /setup-vertex and /setup-bedrock to show the actual settings.json path when CLAUDE_CONFIG_DIR is set, seed model candidates from existing pins on re-run, and offer a "with 1M context" option for supported models` — DONE in 2396509
- [x] `/skills menu now supports sorting by estimated token count — press t to toggle` — DONE in 2396509
- [x] `Ctrl+U now clears the entire input buffer (previously: delete to start of line); press Ctrl+Y to restore` — DONE in 2396509
- [x] `Ctrl+L now forces a full screen redraw in addition to clearing the prompt input` — DONE in 2396509
- [x] `Transcript view footer now shows [ (dump to scrollback) and v (open in editor) shortcuts` — DONE in 2396509
- [x] `The "+N lines" marker for truncated long pastes is now a full-width rule for easier scanning` — DONE in 2396509
- [-] `Headless --output-format stream-json now includes plugin_errors on the init event when plugins are demoted for unsatisfied dependencies` — SKIP (headless plugin infra)
- [x] `Added OTEL_LOG_RAW_API_BODIES environment variable to emit full API request and response bodies as OpenTelemetry log events for debugging` — DONE in 2396509
- [x] `Suppressed spurious decompression, network, and transient error messages that could appear in the TUI during normal operation` — DONE in 2396509
- [x] `Reverted the v2.1.110 cap on non-streaming fallback retries — it traded long waits for more outright failures during API overload` — DONE in 2396509
- [x] `Fixed terminal display tearing (random characters, drifting input) in iTerm2 + tmux setups when terminal notifications are sent` — DONE in 2396509
- [x] `Fixed @ file suggestions re-scanning the entire project on every turn in non-git working directories, and showing only config files in freshly-initialized git repos with no tracked files` — DONE in 2396509
- [x] `Fixed LSP diagnostics from before an edit appearing after it, causing the model to re-read files it just edited` — DONE in 2396509
- [x] `Fixed tab-completing /resume immediately resuming an arbitrary titled session instead of showing the session picker` — DONE in 2396509
- [x] `Fixed /context grid rendering with extra blank lines between rows` — DONE in 2396509
- [x] `Fixed /clear dropping the session name set by /rename, causing statusline output to lose session_name` — DONE in 2396509
- [-] `Improved plugin error handling: dependency errors now distinguish conflicting, invalid, and overly complex version requirements; fixed stale resolved versions after plugin update; plugin install now recovers from interrupted prior installs` — SKIP (marketplace)
- [x] `Fixed Claude calling a non-existent commit skill and showing "Unknown skill: commit" for users without a custom /commit command` — DONE in 2396509
- [x] `Fixed 429 rate-limit errors on Bedrock/Vertex/Foundry referencing status.claude.com (it only covers Anthropic-operated providers)` — DONE in 2396509
- [-] `Fixed feedback surveys appearing back-to-back after dismissing one` — SKIP (feedback disabled)
- [x] `Fixed bare URLs in bash/PowerShell/MCP tool output being unclickable when the terminal wraps them across lines` — DONE in 2396509
- [-] `Windows: CLAUDE_ENV_FILE and SessionStart hook environment files now apply (previously a no-op)` — SKIP (Linux container only)
- [-] `Windows: permission rules with drive-letter paths are now correctly root-anchored, and paths differing only by drive-letter case are recognized as the same path` — SKIP (Linux container only)

## 2.1.110

- [x] `Added /tui command and tui setting — run /tui fullscreen to switch to flicker-free rendering in the same conversation` — DONE in 4c51673
- [-] `Added push notification tool — Claude can send mobile push notifications when Remote Control and "Push when Claude decides" config are enabled` — SKIP (Remote Control infra; we have our own PushNotificationTool)
- [x] `Changed Ctrl+O to toggle between normal and verbose transcript only; focus view is now toggled separately with the new /focus command` — DONE in 2396509
- [x] `Added autoScrollEnabled config to disable conversation auto-scroll in fullscreen mode` — DONE in 386b37a
- [x] `Added option to show Claude's last response as commented context in the Ctrl+G external editor (enable via /config)` — DONE in 2396509
- [-] `Improved /plugin Installed tab — items needing attention and favorites appear at the top, disabled items are hidden behind a fold, and f favorites the selected item` — SKIP (marketplace/plugin UI)
- [x] `Improved /doctor to warn when an MCP server is defined in multiple config scopes with different endpoints` — DONE in 386b37a
- [x] `--resume/--continue now resurrects unexpired scheduled tasks` — DONE in 386b37a (touch cron file to trigger watcher reload)
- [-] `/context, /exit, and /reload-plugins now work from Remote Control (mobile/web) clients` — SKIP (Remote Control infra)
- [x] `Write tool now informs the model when you edit the proposed content in the IDE diff before accepting` — DONE in 2396509
- [x] `Bash tool now enforces the documented maximum timeout instead of accepting arbitrarily large values` — DONE in ebc109a
- [x] `SDK/headless sessions now read TRACEPARENT/TRACESTATE from the environment for distributed trace linking` — DONE in 386b37a
- [x] `Session recap is now enabled for users with telemetry disabled (Bedrock, Vertex, Foundry, DISABLE_TELEMETRY). Opt out via /config or CLAUDE_CODE_ENABLE_AWAY_SUMMARY=0.` — DONE in 386b37a (enabled by default, opt-out via setting or env)
- [x] `Fixed MCP tool calls hanging indefinitely when the server connection drops mid-response on SSE/HTTP transports` — DONE in ebc109a (reduced tool timeout from 27.8h to 10min)
- [x] `Fixed non-streaming fallback retries causing multi-minute hangs when the API is unreachable` — DONE in ebc109a (maxRetries 10→3 for fallback)
- [x] `Fixed session recap, local slash-command output, and other system status lines not appearing in focus mode` — DONE (already handled: filterForFocusView keeps all system subtypes except api_metrics)
- [x] `Fixed high CPU usage in fullscreen when text is selected while a tool is running` — DONE in 386b37a (notifySelectionChange uses scheduleRender instead of onRender)
- [-] `Fixed plugin install not honoring dependencies declared in plugin.json when the marketplace entry omits them; /plugin install now lists auto-installed dependencies` — SKIP (marketplace)
- [x] `Fixed skills with disable-model-invocation: true failing when invoked via /<skill> mid-message` — DONE in ebc109a
- [x] `Fixed --resume sometimes showing the first prompt instead of the /rename name for sessions still running or exited uncleanly` — DONE in ebc109a (customTitle priority over agentName)
- [x] `Fixed queued messages briefly appearing twice during multi-tool-call turns` — DONE in ebc109a
- [x] `Fixed session cleanup not removing the full session directory including subagent transcripts` — DONE in ebc109a
- [x] `Fixed dropped keystrokes after the CLI relaunches (e.g. /tui, provider setup wizards)` — DONE in 386b37a (drainStdin in resumeStdin)
- [x] `Fixed garbled startup rendering in macOS Terminal.app and other terminals that don't support synchronized output` — DONE in 386b37a (skip sync markers on all unsupported terminals)
- [x] `Hardened "Open in editor" actions against command injection from untrusted filenames` — DONE in ebc109a (single-quote escaping in promptEditor)
- [x] `Fixed PermissionRequest hooks returning updatedInput not being re-checked against permissions.deny rules; setMode:bypassPermissions updates now respect disableBypassPermissionsMode` — DONE in ebc109a
- [x] `Fixed PreToolUse hook additionalContext being dropped when the tool call fails` — DONE in ebc109a
- [x] `Fixed stdio MCP servers that print stray non-JSON lines to stdout being disconnected on the first stray line (regression in 2.1.105)` — DONE in ebc109a (10-line tolerance before disconnect)
- [-] `Fixed headless/SDK session auto-title firing an extra Haiku request when CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC or CLAUDE_CODE_DISABLE_TERMINAL_TITLE is set` — SKIP (we set DISABLE_NONESSENTIAL_TRAFFIC=1 globally)
- [x] `Fixed potential excessive memory allocation when piped (non-TTY) Ink output contains a single very wide line` — DONE in ebc109a (10K width cap in resetScreen)
- [x] `Fixed /skills menu not scrolling when the list overflows the modal in fullscreen mode` — DONE in 386b37a (modal inner box flexGrow/flexShrink instead of overflow:hidden)
- [-] `Fixed Remote Control sessions showing a generic error instead of prompting for re-login when the session is too old` — SKIP (Remote Control infra)
- [-] `Fixed Remote Control session renames from claude.ai not persisting the title to the local CLI session` — SKIP (Remote Control infra)

## 2.1.109

- [x] `Improved the extended-thinking indicator with a rotating progress hint` — DONE in ebc109a (6-word cycle: thinking→reasoning→analyzing→considering→evaluating→reflecting)

## 2.1.108

- [x] `Added ENABLE_PROMPT_CACHING_1H env var to opt into 1-hour prompt cache TTL on API key, Bedrock, Vertex, and Foundry; FORCE_PROMPT_CACHING_5M to force 5-minute TTL` — DONE in 19f2d6c
- [x] `Added recap feature to provide context when returning to a session, configurable in /config and manually invocable with /recap; force with CLAUDE_CODE_ENABLE_AWAY_SUMMARY if telemetry disabled` — DONE in 19f2d6c (/recap command + awaySummaryEnabled setting + env var)
- [x] `The model can now discover and invoke built-in slash commands like /init, /review, and /security-review via the Skill tool` — DONE (already in codebase, SkillTool discovers all type:'prompt' commands)
- [-] `/undo is now an alias for /rewind` — SKIP (trivial alias, low priority)
- [x] `Improved /model to warn before switching models mid-conversation, since the next response re-reads the full history uncached` — DONE in 19f2d6c
- [x] `Improved /resume picker to default to sessions from current directory; press Ctrl+A to show all projects` — DONE (already in codebase, showAllProjects toggle with Ctrl+A in LogSelector)
- [x] `Improved error messages: server rate limits distinguished from plan usage limits; 5xx/529 errors show status.claude.com link; unknown slash commands suggest closest match` — DONE in 19f2d6c (levenshtein matching + status link on 529/5xx)
- [x] `Reduced memory footprint for file reads, edits, and syntax highlighting by loading language grammars on demand` — DONE (already in codebase, highlight.js lazy-loaded via getCliHighlightPromise)
- [x] `Added verbose indicator when viewing detailed transcript (Ctrl+O)` — DONE in 19f2d6c (verbose appState toggle)
- [x] `Added warning at startup when prompt caching is disabled via DISABLE_PROMPT_CACHING* environment variables` — DONE in 19f2d6c
- [x] `Fixed paste not working in /login code prompt (regression in 2.1.105)` — DONE in 19f2d6c (onPaste={setPastedCode} on ConsoleOAuthFlow TextInput)
- [x] `Fixed subscribers who set DISABLE_TELEMETRY falling back to 5-minute prompt cache TTL instead of 1 hour` — DONE (USER_TYPE=ant bypasses; ENABLE_PROMPT_CACHING_1H env var added for 3P)
- [x] `Fixed Agent tool prompting for permission in auto mode when safety classifier transcript exceeded context window` — DONE in 19f2d6c (auto-allow in bypassPermissions mode on overflow)
- [x] `Fixed Bash tool producing no output when CLAUDE_ENV_FILE ends with a # comment line` — DONE in 19f2d6c (trimStart + trailing newline guard)
- [x] `Fixed claude --resume <session-id> losing session custom name and color set via /rename` — DONE in 19f2d6c (customTitle ?? agentName in sessionRestore)
- [x] `Fixed session titles showing placeholder example text when first message is a short greeting` — DONE in 19f2d6c (SHORT_GREETINGS set + length check)
- [x] `Fixed terminal escape codes appearing as garbage text in prompt input after --teleport` — DONE in 19f2d6c (stripAnsi on teleported message blocks)
- [-] `Fixed /feedback retry: pressing Enter to resubmit after failure` — SKIP (feedback disabled in our fork)
- [x] `Fixed --teleport and --resume <id> precondition errors exiting silently instead of showing error message` — DONE in 19f2d6c (stderr.write before exit)
- [-] `Fixed Remote Control session titles set in web UI being overwritten by auto-generated titles after third message` — SKIP (Remote Control infra)
- [x] `Fixed --resume truncating sessions when transcript contained self-referencing message` — DONE in 19f2d6c (parentUuid !== uuid guard + visited set cycle detection)
- [x] `Fixed transcript write failures (disk full) being silently dropped instead of logged` — DONE in 19f2d6c (logError on tombstone removal + metadata re-append)
- [x] `Fixed diacritical marks (accents, umlauts, cedillas) being dropped from responses when language setting is configured` — DONE in 19f2d6c (combining marks \p{M} guard in sanitization.ts)
- [-] `Fixed policy-managed plugins never auto-updating when running from different project than first installed` — SKIP (managed plugins infra)

## 2.1.107

- [x] `Show thinking hints sooner during long operations` — DONE in b6c6b0e (thinking min display 2s→1s)

## 2.1.105

- [x] `Added path parameter to EnterWorktree tool to switch into an existing worktree` — DONE in 611f21f
- [x] `Added PreCompact hook support: hooks can block compaction by exiting with code 2 or returning {"decision":"block"}` — DONE in 611f21f
- [x] `Added background monitor support for plugins via top-level monitors manifest key` — DONE in 4e65c5d
- [-] `/proactive is now an alias for /loop` — SKIP (we have our own /proactive implementation)
- [x] `Improved stalled API stream handling: streams abort after 5 minutes of no data and retry non-streaming` — DONE in 611f21f (watchdog enabled by default, 300s timeout)
- [x] `Improved network error messages: connection errors show retry message immediately instead of silent spinner` — DONE in 611f21f
- [x] `Improved file write display: long single-line writes truncated in UI instead of paginating` — DONE in 611f21f (500 char/line cap)
- [x] `Improved /doctor layout with status icons; press f to have Claude fix reported issues` — DONE in 574aa75 (press f to fix implemented; status icons skipped — UI polish)
- [-] `Improved /config labels and descriptions for clarity` — SKIP (UI polish)
- [x] `Improved skill description handling: raised listing cap from 250 to 1,536 characters and startup warning when truncated` — DONE in 611f21f
- [x] `Improved WebFetch to strip <style> and <script> contents from fetched pages` — DONE in 611f21f
- [x] `Improved stale agent worktree cleanup to remove worktrees whose PR was squash-merged` — DONE in 611f21f (diff --quiet against origin/HEAD)
- [x] `Improved MCP large-output truncation prompt to give format-specific recipes` — DONE in 611f21f (jq for JSON, Read chunks for text)
- [x] `Fixed images attached to queued messages being dropped` — DONE in 64c109a (pass pastedContents from all queued commands)
- [x] `Fixed screen going blank when prompt input wraps to second line in long conversations` — DONE in b48f3cf (BaseTextInput textWrap truncate-end→wrap)
- [x] `Fixed leading whitespace getting copied when selecting multi-line assistant responses in fullscreen mode` — DONE in b48f3cf (mark padding columns noSelect)
- [x] `Fixed leading whitespace being trimmed from assistant messages, breaking ASCII art and indented diagrams` — DONE in 611f21f (trimEnd instead of trim in Markdown.tsx)
- [x] `Fixed garbled bash output when commands print clickable file links` — DONE in b48f3cf (OSC 8 pattern added to strip-ansi regex)
- [x] `Fixed alt+enter not inserting a newline in terminals using ESC-prefix alt encoding, and Ctrl+J regression` — DONE in b76ddca (Ctrl+J added to handleCtrl map)
- [x] `Fixed duplicate "Creating worktree" text in EnterWorktree/ExitWorktree tool display` — DONE in 611f21f (renderToolUseMessage returns null)
- [x] `Fixed queued user prompts disappearing from focus mode` — DONE in b48f3cf (preserve queued_command attachments in filterForFocusView)
- [x] `Fixed one-shot scheduled tasks re-firing repeatedly when file watcher missed post-fire cleanup` — DONE in 64c109a (nextFireAt=Infinity during deletion)
- [-] `Fixed inbound channel notifications silently dropped after first message for Team/Enterprise` — SKIP (Team/Enterprise infra)
- [-] `Fixed marketplace plugins with package.json not having dependencies installed after install/update` — SKIP (marketplace)
- [-] `Fixed marketplace auto-update leaving official marketplace broken when plugin process holds files open` — SKIP (marketplace)
- [x] `Fixed "Resume this session with..." hint not printing on exit after /resume, --worktree, or /branch` — DONE in 611f21f (use getSessionProjectDir fallback)
- [-] `Fixed feedback survey shortcut keys firing when typed at end of longer prompt` — SKIP (feedback survey disabled in our fork)
- [x] `Fixed stdio MCP server emitting malformed output hanging session instead of failing fast` — DONE in 611f21f (onerror handler on transport)
- [x] `Fixed MCP tools missing on first turn of headless/remote-trigger sessions when MCP servers connect asynchronously` — DONE in 64c109a (always capture plugin install promise)
- [-] `Fixed /model picker on AWS Bedrock in non-US regions persisting invalid us.* model IDs` — SKIP (Bedrock-specific)
- [x] `Fixed 429 rate-limit errors showing raw JSON dump instead of clean message for API-key, Bedrock, and Vertex users` — DONE in 611f21f
- [x] `Fixed crash on resume when session contains malformed text blocks` — DONE in 611f21f (sanitize text blocks in conversationRecovery)
- [x] `Fixed /help dropping tab bar, Shortcuts heading, and footer at short terminal heights` — DONE in b76ddca (min height 8 rows)
- [x] `Fixed malformed keybinding entry values in keybindings.json being silently loaded instead of rejected` — DONE in 611f21f (skip non-string values)
- [-] `Fixed CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC in one project's settings permanently disabling usage metrics for all projects` — SKIP (we set DISABLE_NONESSENTIAL_TRAFFIC=1 globally at entrypoint)
- [x] `Fixed washed-out 16-color palette when using Ghostty, Kitty, Alacritty, WezTerm, foot, rio, or Contour over SSH/mosh` — DONE in 64c109a (detect truecolor terminals, boost chalk level)
- [x] `Fixed Bash tool suggesting acceptEdits permission mode when exiting plan mode would downgrade from higher level` — DONE in 611f21f (exclude plan mode from suggestion)

## 2.1.101

- [-] `Added /team-onboarding command to generate a teammate ramp-up guide` — SKIP (Anthropic managed infra, requires cloud onboarding flow)
- [x] `Added OS CA certificate store trust by default (CLAUDE_CODE_CERT_STORE=bundled)` — DONE in cb7e5ca
- [-] `/ultraplan auto-create default cloud environment` — SKIP (Anthropic cloud infra)
- [x] `Improved brief mode to retry once when Claude responds with plain text instead of structured message` — a1c7c6e
- [x] `Improved focus mode: Claude writes more self-contained summaries knowing user only sees final message` — DONE in fcb0b30 (BriefTool prompt updated)
- [x] `Improved tool-not-available errors to explain why and how to proceed` — DONE in 167cb90
- [x] `Improved rate-limit retry messages to show which limit was hit and when it resets` — DONE in 98731af
- [x] `Improved refusal error messages to include API-provided explanation` — DONE in 167cb90
- [x] `Improved claude -p --resume <name> to accept session titles from /rename or --name` — DONE in ff9a9b3
- [x] `Improved settings resilience: unrecognized hook event name no longer causes entire settings.json to be ignored` — DONE in fd58648 (z.string() key instead of z.enum)
- [x] `Improved plugin hooks from force-enabled plugins to run when allowManagedHooksOnly is set` — DONE in f7ea957
- [x] `Improved /plugin and claude plugin update to warn when marketplace could not be refreshed` — DONE in f4b49cc
- [-] `Improved plan mode to hide Refine with Ultraplan when org can't reach web` — SKIP (Anthropic cloud)
- [-] `Improved beta tracing to honor OTEL_LOG_USER_PROMPTS/TOOL_DETAILS/TOOL_CONTENT` — SKIP (OTEL infra)
- [-] `Improved SDK query() cleanup on break/await using` — SKIP (SDK internals)
- [x] `Fixed command injection vulnerability in POSIX which fallback for LSP binary detection` — DONE in 2569482 (execFileSync/execa array args instead of shell interpolation)
- [x] `Fixed memory leak where long sessions retained historical copies of message list in virtual scroller` — a0124cf
- [x] `Fixed --resume/--continue losing context on large sessions when loader anchored on dead-end branch` — DONE (already in codebase, gated on tengu_pebble_leaf_prune which we enable)
- [x] `Fixed --resume chain recovery bridging into unrelated subagent conversation` — DONE (already in codebase, findLatestMessage with !m.isSidechain filter at sessionStorage.ts:3949)
- [x] `Fixed crash on --resume when persisted Edit/Write tool result missing file_path` — DONE in 2569482 (optional chaining)
- [x] `Fixed hardcoded 5-minute request timeout ignoring API_TIMEOUT_MS` — DONE in b60045d (300s→600s default for non-streaming fallback)
- [x] `Fixed permissions.deny rules not overriding PreToolUse hook permissionDecision:ask` — DONE in ed80f5a
- [x] `Fixed --setting-sources without user causing cleanup to ignore cleanupPeriodDays` — DONE in 77ff208
- [-] `Fixed Bedrock SigV4 authentication failing with Authorization header` — SKIP (Bedrock-specific)
- [x] `Fixed claude -w <name> failing with "already exists" after stale worktree cleanup` — DONE in 3554670
- [x] `Fixed subagents not inheriting MCP tools from dynamically-injected servers` — DONE (already in codebase, assembleToolPool passes appState.mcp.tools at AgentTool.tsx:577)
- [x] `Fixed sub-agents in worktrees denied Read/Edit access to files inside their own worktree` — DONE in defb5cf (getCwd() added to allWorkingDirectories)
- [-] `Fixed sandboxed Bash commands failing with mktemp after fresh boot` — SKIP (sandbox infra)
- [-] `Fixed claude mcp serve tool calls failing with outputSchema validation` — SKIP (MCP serve)
- [x] `Fixed RemoteTrigger tool run action sending empty body` — DONE in ed80f5a
- [x] `Fixed several /resume picker issues: narrow default view, unreachable preview, incorrect cwd in worktrees, session-not-found stderr, terminal title, resume hint overlap` — 05b0656
- [x] `Fixed Grep tool ENOENT when embedded ripgrep binary path stale; falls back to system rg` — DONE (already in codebase, ripgrep.ts:64-75 existsSync + findExecutable fallback)
- [x] `Fixed /btw writing entire conversation to disk on every use` — DONE in ed80f5a (skipTranscript on side questions)
- [x] `Fixed /context Free space and Messages breakdown disagreeing with header percentage` — DONE in 295ecea (reconcile Free space with API usage)
- [x] `Fixed several plugin issues: duplicate name frontmatter, ENAMETOOLONG, stale version cache, context:fork/agent frontmatter` — 257a60d
- [x] `Fixed /mcp menu offering OAuth actions for headersHelper servers` — DONE in 55059e8 (show Reconnect instead)
- [x] `Fixed ctrl+], ctrl+\, ctrl+^ keybindings not firing in terminals sending raw C0 control bytes` — DONE in ed80f5a
- [x] `Fixed /login OAuth URL rendering with padding preventing clean mouse selection` — DONE in ff9a9b3
- [x] `Fixed rendering issues: flicker in non-fullscreen, scrollback wiped during long sessions, mouse-scroll escapes leaking into prompt` — 04823e8
- [x] `Fixed crash when settings.json env values are numbers instead of strings` — DONE in eeca77b (String() coercion in filterSettingsEnv)
- [x] `Fixed in-app settings writes not refreshing in-memory snapshot` — DONE in 295ecea (clear pluginSettingsBase in resetSettingsCache)
- [-] `Fixed custom keybindings not loading on Bedrock/Vertex/third-party providers` — SKIP (provider-specific)
- [x] `Fixed claude --continue -p not correctly continuing -p/SDK sessions` — DONE in ff9a9b3 (bypass isNonInteractive filter via fetchLogs)
- [-] `Fixed several Remote Control issues` — SKIP (Remote Control infra)
- [-] `Fixed /insights sometimes omitting report file link` — SKIP (insights feature)
- [-] `[VSCode] Fixed file attachment not clearing when last editor tab closed` — SKIP (VSCode extension)

## 2.1.100 (prompt-only release, not in Anthropic changelog)

- [-] `REMOVED: system-prompt-exploratory-questions-analyze-before-implementing.md` — SKIP (runtime-injected prompt, not in our source)
- [-] `REMOVED: system-prompt-output-efficiency.md` — SKIP (runtime-injected prompt, not in our source)
- [-] `REMOVED: system-prompt-user-facing-communication-style.md` — SKIP (runtime-injected prompt, content folded into communication-style.md)
- [-] `EDITED: system-prompt-communication-style.md — end-of-turn summary tightened to "one or two sentences"` — SKIP (runtime-injected prompt)
- [-] `20 new feature flags (tengu_kairos_loop_*, tengu_loops_command, tengu_mcp_directory_*, tengu_sdk_*, tengu_sedge_lantern, tengu_cinder_almanac, tengu_ultraplan_dialog_choice, tengu_vertex_setup_complete)` — SKIP (all pass through feature() polyfill)
- [-] `REMOVED: tengu_flint_harbor flag` — SKIP (not referenced in our code)
- [-] `2 new env vars: CLAUDE_CODE_CERT_STORE, CLAUDE_CODE_SDK_HAS_OAUTH_REFRESH` — SKIP (enterprise/OAuth infra)

## 2.1.98

- [-] `Added interactive Google Vertex AI setup wizard from login screen` — SKIP (Anthropic cloud infra)
- [x] `Added CLAUDE_CODE_PERFORCE_MODE env var: Edit/Write/NotebookEdit fail on read-only files with p4 edit hint` — DONE in 35a791c
- [x] `Added Monitor tool for streaming events from background scripts` — e9f6195
- [x] `Added subprocess sandboxing with PID namespace isolation on Linux (CLAUDE_CODE_SUBPROCESS_ENV_SCRUB, CLAUDE_CODE_SCRIPT_CAPS)` — DONE in cb7e5ca (unshare --pid --fork when CLAUDE_CODE_SCRIPT_CAPS=1 or IS_SANDBOX=1)
- [x] `Added --exclude-dynamic-system-prompt-sections flag to print mode for improved cross-user prompt caching` — DONE in e9b0c9d
- [x] `Added workspace.git_worktree to status line JSON input` — DONE in 4950e3e
- [-] `Added W3C TRACEPARENT env var to Bash tool subprocesses when OTEL tracing enabled` — SKIP (OTEL infra)
- [-] `LSP: Claude Code now identifies itself to language servers via clientInfo in initialize request` — SKIP (LSP internals)
- [x] `Fixed Bash tool permission bypass where backslash-escaped flag could be auto-allowed as read-only` — DONE in 4950e3e
- [x] `Fixed compound Bash commands bypassing forced permission prompts in auto and bypass-permissions modes` — DONE (deny rule check on full compound after operator 'allow')
- [x] `Fixed read-only commands with env-var prefixes not prompting unless the var is known-safe` — DONE (stripSafeWrappers in isCommandReadOnly)
- [x] `Fixed redirects to /dev/tcp/... or /dev/udp/... not prompting instead of auto-allowing` — DONE in defb61c
- [x] `Fixed stalled streaming responses timing out instead of falling back to non-streaming mode` — DONE (already implemented: watchdog + non-streaming fallback in claude.ts)
- [x] `Fixed 429 retries burning all attempts in ~13s when server returns small Retry-After` — DONE in defb61c
- [x] `Fixed MCP OAuth oauth.authServerMetadataUrl config override not honored on token refresh after restart` — DONE in 824cc2e
- [x] `Fixed capital letters being dropped to lowercase on xterm and VS Code with kitty keyboard protocol` — DONE in 824cc2e
- [-] `Fixed macOS text replacements deleting trigger word instead of inserting substitution` — SKIP (macOS-specific)
- [x] `Fixed --dangerously-skip-permissions being silently downgraded to accept-edits after approving write to protected path via Bash` — DONE in 33c3cd1
- [x] `Fixed managed-settings allow rules remaining active after admin removed them until process restart` — DONE in e9b0c9d
- [x] `Fixed permissions.additionalDirectories changes not applying mid-session` — DONE in e9b0c9d
- [x] `Fixed removing directory from additionalDirectories revoking access to same directory passed via --add-dir` — DONE in 33c3cd1
- [x] `Fixed Bash(cmd:*) and Bash(git commit *) wildcard permission rules failing to match commands with extra spaces or tabs` — DONE in 35a791c
- [x] `Fixed Bash(...) deny rules being downgraded to prompt for piped commands mixing cd with other segments` — DONE (reorder deny check before cd+git ask in segmentedCommandPermissionResult)
- [x] `Fixed false Bash permission prompts for cut -d /, paste -d /, column -s /, awk, and filenames containing %` — DONE (cut/paste/column/awk added to COMMAND_ALLOWLIST, % regex fix in hasDangerousExpansion)
- [x] `Fixed permission rules with names matching JavaScript prototype properties (e.g. toString) causing settings.json to be silently ignored` — DONE in 4950e3e
- [x] `Fixed agent team members not inheriting leader's permission mode when using --dangerously-skip-permissions` — DONE in 8a6dd9e
- [x] `Fixed crash in fullscreen mode when hovering over MCP tool results` — DONE in d9432fc
- [x] `Fixed copying wrapped URLs in fullscreen mode inserting spaces at line breaks` — DONE in d9432fc
- [x] `Fixed file-edit diffs disappearing from UI on --resume when edited file was larger than 10KB` — DONE in a6a5ba4 (fall through on safeParse failure)
- [~] `Fixed several /resume picker issues: --resume <name> opening uneditable, filter reload wiping search state, empty list swallowing arrow keys, cross-project staleness, and transient task-status text replacing conversation summaries` — PARTIAL in a6a5ba4 (4 of 5 sub-issues: uneditable, filter wipe, empty list, task-status; cross-project staleness deferred)
- [x] `Fixed /export not honoring absolute paths and ~, and silently rewriting user-supplied extensions to .txt` — DONE in 4950e3e
- [x] `Fixed /effort max being denied for unknown or future model IDs` — DONE in defb61c
- [x] `Fixed slash command picker breaking when plugin frontmatter name is a YAML boolean keyword` — DONE in 4950e3e
- [x] `Fixed rate-limit upsell text being hidden after message remounts` — DONE in 24c7f5b (module-level guard prevents re-opening menu for same resetsAt window)
- [x] `Fixed MCP tools with _meta["anthropic/maxResultSizeChars"] not bypassing token-based persist layer` — DONE in 35a791c
- [x] `Fixed voice mode leaking dozens of space characters into input when re-holding push-to-talk key` — DONE in c573e06
- [-] `Fixed DISABLE_AUTOUPDATER not fully suppressing npm registry version check` — SKIP (we use GitHub Releases)
- [x] `Fixed memory leak where Remote Control permission handler entries were retained for lifetime of session` — DONE in 824cc2e
- [x] `Fixed background subagents that fail with error not reporting partial progress to parent agent` — DONE in 35a791c
- [x] `Fixed prompt-type Stop/SubagentStop hooks failing on long sessions, and hook evaluator API errors showing "JSON validation failed"` — DONE in defb61c (stderr included in error)
- [-] `Fixed feedback survey rendering when dismissed` — SKIP (feedback disabled)
- [x] `Fixed Bash grep -f FILE / rg -f FILE not prompting when reading pattern file outside working directory` — DONE in defb61c
- [x] `Fixed stale subagent worktree cleanup removing worktrees that contain untracked files` — DONE in 35a791c
- [-] `Fixed sandbox.network.allowMachLookup not taking effect on macOS` — SKIP (macOS sandbox)
- [x] `Improved /resume filter hint labels and added project/worktree/branch names in filter indicator` — DONE in 7b8eef4 (worktree directory name instead of generic text)
- [x] `Improved footer indicators (Focus, notifications) to stay on mode-indicator row instead of wrapping` — DONE
- [x] `Improved /agents with tabbed layout: Running tab shows live subagents, Library tab adds Run agent and View running instance actions` — 55de6f2
- [x] `Improved /reload-plugins to pick up plugin-provided skills without requiring restart` — DONE in c573e06
- [x] `Improved Accept Edits mode to auto-approve filesystem commands prefixed with safe env vars or process wrappers` — DONE in e9b0c9d
- [x] `Improved Vim mode: j/k in NORMAL mode now navigate history and select footer pill at input boundary` — DONE in a6a5ba4
- [x] `Improved hook errors in transcript to include first line of stderr for self-diagnosis without --debug` — DONE in defb61c
- [-] `Improved OTEL tracing: interaction spans now correctly wrap full turns under concurrent SDK calls` — SKIP (OTEL infra)
- [x] `Improved transcript entries to carry final token usage instead of streaming placeholders` — DONE (already in codebase, claude.ts:2245-2256 direct property mutation ensures transcript captures final values)
- [x] `Updated /claude-api skill to cover Managed Agents alongside Claude API` — DONE
- [-] `[VSCode] Fixed false-positive "requires git-bash" error on Windows` — SKIP (VSCode extension)
- [x] `Fixed CLAUDE_CODE_MAX_CONTEXT_TOKENS to honor DISABLE_COMPACT when set` — DONE
- [x] `Dropped /compact hints when DISABLE_COMPACT is set` — DONE

## 2.1.97

- [x] `Added focus view toggle (Ctrl+O) in NO_FLICKER mode showing prompt, one-line tool summary with edit diffstats, and final response` — 3b4d08a
- [x] `Added refreshInterval status line setting to re-run status line command every N seconds` — DONE in 4950e3e
- [x] `Added workspace.git_worktree to status line JSON input when inside linked git worktree` — DONE in 4950e3e (also in 2.1.98)
- [x] `Added ● N running indicator in /agents next to agent types with live subagent instances` — DONE in 7b8eef4
- [x] `Added syntax highlighting for Cedar policy files (.cedar, .cedarpolicy)` — DONE in defb61c
- [x] `Fixed --dangerously-skip-permissions being silently downgraded to accept-edits after approving write to protected path` — DONE in 33c3cd1 (also in 2.1.98)
- [x] `Fixed and hardened Bash tool permissions, tightening checks around env-var prefixes and network redirects` — DONE in 69d29ac (pipe-to-interpreter detection) + defb61c (env-var prefix + network redirects)
- [x] `Fixed permission rules with names matching JavaScript prototype properties causing settings.json to be silently ignored` — DONE in 4950e3e (also in 2.1.98)
- [x] `Fixed managed-settings allow rules remaining active after admin removed them until process restart` — DONE in e9b0c9d (also in 2.1.98)
- [x] `Fixed permissions.additionalDirectories changes in settings not applying mid-session` — DONE in e9b0c9d (also in 2.1.98)
- [x] `Fixed removing directory from settings.permissions.additionalDirectories revoking access to same directory passed via --add-dir` — DONE in 33c3cd1 (also in 2.1.98)
- [x] `Fixed MCP HTTP/SSE connections accumulating ~50 MB/hr of unreleased buffers when servers reconnect` — DONE in 824cc2e
- [x] `Fixed MCP OAuth oauth.authServerMetadataUrl not honored on token refresh after restart` — DONE in 824cc2e (also in 2.1.98)
- [x] `Fixed 429 retries burning all attempts in ~13s when server returns small Retry-After` — DONE in defb61c (also in 2.1.98)
- [x] `Fixed rate-limit upgrade options disappearing after context compaction` — DONE in 24c7f5b (module-level guard, also in 2.1.98)
- [~] `Fixed several /resume picker issues` — PARTIAL in a6a5ba4 (4 of 5 sub-issues, also in 2.1.98)
- [x] `Fixed file-edit diffs disappearing on --resume when edited file was larger than 10KB` — DONE in a6a5ba4 (also in 2.1.98)
- [x] `Fixed --resume cache misses and lost mid-turn input from attachment messages not being saved to transcript` — DONE in 9eb1902 (mid-turn input fix; USER_TYPE=ant handles attachment persistence)
- [x] `Fixed messages typed while Claude is working not being persisted to transcript` — DONE in 9eb1902
- [x] `Fixed prompt-type Stop/SubagentStop hooks failing on long sessions` — DONE in defb61c (also in 2.1.98)
- [x] `Fixed subagents with worktree isolation or cwd: override leaking working directory back to parent session's Bash tool` — DONE in 824cc2e
- [x] `Fixed compaction writing duplicate multi-MB subagent transcript files on prompt-too-long retries` — DONE in 35a791c
- [x] `Fixed claude plugin update reporting "already at latest version" for git-based marketplace plugins with newer remote commits` — DONE in be20375
- [x] `Fixed slash command picker breaking when plugin frontmatter name is YAML boolean keyword` — DONE in 4950e3e (also in 2.1.98)
- [x] `Fixed copying wrapped URLs in NO_FLICKER mode inserting spaces at line breaks` — DONE in d9432fc
- [x] `Fixed scroll rendering artifacts in NO_FLICKER mode when running inside zellij` — DONE in be20375
- [x] `Fixed crash in NO_FLICKER mode when hovering over MCP tool results` — DONE in d9432fc
- [x] `Fixed NO_FLICKER mode memory leak where API retries left stale streaming state` — DONE in 07783d8
- [-] `Fixed slow mouse-wheel scrolling in NO_FLICKER mode on Windows Terminal` — SKIP (Windows-specific)
- [x] `Fixed custom status line not displaying in NO_FLICKER mode on terminals shorter than 24 rows` — DONE in d9432fc
- [x] `Fixed Shift+Enter and Alt/Cmd+arrow shortcuts not working in Warp with NO_FLICKER mode` — DONE in be20375
- [-] `Fixed Korean/Japanese/Unicode text becoming garbled when copied in no-flicker mode on Windows` — SKIP (Windows-specific)
- [-] `Fixed Bedrock SigV4 authentication failing when AWS_BEARER_TOKEN_BEDROCK or ANTHROPIC_BEDROCK_BASE_URL are set to empty strings` — SKIP (Bedrock-specific)
- [x] `Improved Accept Edits mode to auto-approve filesystem commands prefixed with safe env vars or process wrappers` — DONE in e9b0c9d (also in 2.1.98)
- [x] `Improved auto mode and bypass-permissions mode to auto-approve sandbox network access prompts` — DONE in 824cc2e
- [-] `Improved sandbox: sandbox.network.allowMachLookup now takes effect on macOS` — SKIP (macOS sandbox)
- [x] `Improved image handling: pasted/attached images compressed to same token budget as images read via Read tool` — DONE (compressImageBufferWithTokenLimit added to imagePaste.ts + attachments.ts)
- [x] `Improved slash command and @-mention completion to trigger after CJK sentence punctuation` — DONE
- [-] `Improved Bridge sessions to show local git repo, branch, and working directory on claude.ai session card` — SKIP (claude.ai Bridge)
- [x] `Improved footer layout: indicators stay on mode-indicator row instead of wrapping below` — DONE (also in 2.1.98)
- [x] `Improved context-low warning to show as transient footer notification instead of persistent row` — DONE
- [x] `Improved markdown blockquotes to show continuous left bar across wrapped lines` — DONE
- [x] `Improved session transcript size by skipping empty hook entries and capping stored pre-edit file copies` — DONE
- [x] `Improved transcript accuracy: per-block entries carry final token usage instead of streaming placeholder` — DONE (already in codebase, claude.ts:2245-2256)
- [-] `Improved Bash tool OTEL tracing: subprocesses inherit W3C TRACEPARENT env var when tracing enabled` — SKIP (OTEL infra)
- [x] `Updated /claude-api skill to cover Managed Agents alongside Claude API` — DONE (also in 2.1.98)

## 2.1.96

- [-] `Fixed Bedrock requests failing with 403 when using AWS_BEARER_TOKEN_BEDROCK or CLAUDE_CODE_SKIP_BEDROCK_AUTH` — SKIP (Bedrock-specific, regression in 2.1.94)

## 2.1.94

- [-] `Added support for Amazon Bedrock powered by Mantle` — SKIP (Anthropic cloud infra)
- [x] `Changed default effort level from medium to high for API-key/Bedrock/Vertex/Foundry/Team/Enterprise users` — DONE (already in codebase, USER_TYPE=ant returns undefined/high at effort.ts:301)
- [-] `Added compact Slacked #channel header with clickable link for Slack MCP send-message` — SKIP (Slack MCP connector, Anthropic infra)
- [x] `Added keep-coding-instructions frontmatter field for plugin output styles` — DONE in 402e025
- [x] `Added hookSpecificOutput.sessionTitle to UserPromptSubmit hooks` — DONE in 402e025
- [x] `Plugin skills use frontmatter name for invocation name instead of directory basename` — DONE in 402e025
- [x] `Fixed agents appearing stuck after 429 rate-limit with long Retry-After` — DONE in 5380f82 (yield error message before sleeping in fast mode path)
- [-] `Fixed Console login on macOS silently failing when login keychain locked` — SKIP (macOS Console login)
- [x] `Fixed plugin skill hooks defined in YAML frontmatter being silently ignored` — DONE (already in codebase, loadSkillsDir.ts:259 parseHooksFromFrontmatter + registerSkillHooks)
- [x] `Fixed plugin hooks failing with No such file or directory when CLAUDE_PLUGIN_ROOT not set` — DONE (already in codebase, pluginOptionsStorage.ts:326 substitutePluginVariables uses plugin.path)
- [x] `Fixed CLAUDE_PLUGIN_ROOT resolving to marketplace source instead of installed cache for local-marketplace plugins` — DONE (already in codebase, pluginLoader.ts:1367 plugin.path = pluginPath)
- [x] `Fixed scrollback showing same diff repeated and blank pages in long-running sessions` — DONE in d08d839 (DECSTBM height shrink guard prevents ghost lines)
- [x] `Fixed multiline user prompts indenting wrapped lines under the caret instead of under the text` — DONE in f96f807 (Box flexDirection=row in HighlightedThinkingText)
- [x] `Fixed Shift+Space inserting literal word space instead of space character in search inputs` — DONE in f96f807 (handle name='space' in keyFromParsed)
- [x] `Fixed hyperlinks opening two browser tabs when clicked inside tmux in xterm.js-based terminals` — DONE in d08d839 (wrapForMultiplexer on OSC 8)
- [x] `Fixed alt-screen rendering bug where content height changes mid-scroll left ghost lines` — DONE in d08d839 (reject DECSTBM when height shrinks)
- [x] `Fixed FORCE_HYPERLINK env var being ignored when set via settings.json env` — DONE in d08d839 (add to SAFE_ENV_VARS)
- [-] `Fixed native terminal cursor not tracking selected tab in dialogs` — SKIP (accessibility/screen reader)
- [-] `Fixed Bedrock invocation of Sonnet 3.5 v2` — SKIP (Bedrock-specific)
- [x] `Fixed SDK/print mode not preserving partial assistant response when interrupted mid-stream` — DONE in c15e26b (flush partial contentBlocks before abort throw in queryModel)
- [x] `Improved --resume to resume sessions from other worktrees directly` — DONE (already in codebase, crossProjectResume.ts gates on USER_TYPE=ant which we set at entrypoint)
- [x] `Fixed CJK and multibyte text corrupted with U+FFFD in stream-json when chunk boundaries split UTF-8` — DONE in c15e26b (decodeUtf8Stream wrapper with TextDecoder stream:true)
- [-] `[VSCode] Reduced cold-open subprocess work` — SKIP (VSCode extension)
- [-] `[VSCode] Fixed dropdown menus selecting wrong item` — SKIP (VSCode extension)
- [-] `[VSCode] Added warning banner when settings.json fails to parse` — SKIP (VSCode extension)

## 2.1.92

- [-] `Added forceRemoteSettingsRefresh policy setting` — SKIP (Anthropic managed infra)
- [-] `Added interactive Bedrock setup wizard` — SKIP (Anthropic cloud infra, needs AWS SDK integration)
- [x] `Added per-model and cache-hit breakdown to /cost` — DONE in bb4fad9
- [x] `/release-notes is now an interactive version picker` — DONE in 64c457b
- [x] `Remote Control session names use hostname prefix` — DONE in 90d72cc (CLAUDE_REMOTE_CONTROL_SESSION_NAME_PREFIX env var)
- [x] `Pro users see footer hint for prompt cache expiry` — DONE in 5a908af
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
- [x] `Fixed collapsed search/read badge duplication in fullscreen` — DONE in 16ec21b (shouldRenderStatically for completed collapsed groups)
- [x] `Fixed auto mode not respecting explicit user boundaries` — DONE in 7b8f28c (populated empty classifier prompt files)
- [x] `Fixed click-to-expand hover text on light themes` — DONE in 850256f
- [x] `Fixed UI crash on malformed tool input in permission dialog` — DONE in 2d14581
- [x] `Fixed headers disappearing in selection screens` — DONE in 850256f
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
- [x] `Added named subagents to @ mention typeahead` — DONE (already in codebase, useTypeahead.tsx:616 reads agentNameRegistry from AppState, shows named agents with status)
- [x] `Added MCP_CONNECTION_NONBLOCKING for -p mode` — DONE (already in codebase, cli.tsx:38)
- [x] `Auto mode denied commands show notification + retry in /permissions` — DONE (already in codebase, useCanUseTool.tsx recordAutoModeDenial + notification, RecentDenialsTab.tsx retry with 'r' key)
- [x] `Fixed Edit/Read allow rules to check symlink targets` — DONE in 24c7f5b
- [-] `Fixed voice push-to-talk modifier bindings` — SKIP (voice not priority)
- [-] `Fixed Edit/Write CRLF doubling on Windows` — SKIP (Windows-specific)
- [x] `Fixed StructuredOutput schema cache 50% failure rate` — DONE (already in codebase, api.ts:142-146 cache key includes inputJSONSchema)
- [x] `Fixed memory leak in LRU cache keys` — DONE in 24c7f5b
- [x] `Fixed crash removing message from 50MB+ sessions` — DONE (already in codebase, sessionStorage.ts MAX_TOMBSTONE_REWRITE_BYTES guard)
- [x] `Fixed LSP server zombie state after crash` — DONE in bb4fad9
- [x] `Fixed prompt history CJK/emoji truncation at 4KB boundary` — DONE (already in codebase, fsOperations.ts:730-733 raw byte carry across chunk boundaries)
- [x] `Fixed /stats undercounting subagent tokens` — DONE in bb4fad9
- [x] `Fixed -p --resume hangs on 64KB+ deferred input` — DONE in 16ec21b (writeToStdoutAsync with drain backpressure)
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
- [x] `Fixed collapsed group badge duplication in parallel tool use` — DONE in 16ec21b (shouldRenderStatically for completed collapsed groups)
- [x] `Fixed notification invalidates not clearing immediately` — DONE (already in codebase, notifications.tsx invalidatesCurrent clears current + filters queue)
- [x] `Fixed prompt disappearing after submit with background messages` — DONE (already in codebase, REPL.tsx userInputBaselineRef bump on background messages)
- [x] `Fixed Devanagari/combining-mark text truncation` — DONE (already in codebase, intl.ts grapheme segmenter + useTypeahead.tsx:36 \p{M} combining marks + fsOperations.ts:731 UTF-8 byte boundary)
- [x] `Fixed rendering artifacts on main-screen terminals` — DONE (already in codebase, ink.tsx displayCursor tracking + didLayoutShift full-damage backstop)
- [-] `Fixed voice mode macOS Apple Silicon permission` — SKIP (voice)
- [-] `Fixed Shift+Enter on Windows Terminal Preview 1.25` — SKIP (Windows-specific)
- [x] `Fixed UI jitter in iTerm2 inside tmux` — DONE (already in codebase, terminal.ts:74 TMUX detection disables DEC 2026, ink.tsx skipSyncMarkers + DECSTBM bypass)
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
- [x] `Preserved task notifications on Ctrl+B background` — DONE (already in codebase, REPL.tsx:2558 handleBackgroundQuery removes task-notification from queue, forwards as attachments to background session)
- [-] `PowerShell argument-splitting hardening` — SKIP (Windows)
- [-] `/env now applies to PowerShell tool` — SKIP (PowerShell-specific)
- [x] `/usage hides redundant Sonnet bar for Pro/Enterprise` — DONE (already in codebase, Usage.tsx:236 showSonnetBar only for max/team/null)
- [x] `Image paste no longer inserts trailing space` — DONE in 1decbda
- [x] `Pasting !command enters bash mode` — DONE (already in codebase, PromptInput.tsx:1206)
- [x] `/buddy April 1st creature` — DONE (already in our fork via BUDDY flag)
