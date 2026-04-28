# Upstream Backlog

Upstream features from anthropics/claude-code not yet implemented in OpenClaude.
Source: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md

Only entries after v2.1.87 (our fork base). Refresh by fetching:
`curl -fsSL https://raw.githubusercontent.com/anthropics/claude-code/refs/heads/main/CHANGELOG.md`

## 2.1.121

- [x] `Added alwaysLoad option to MCP server config — when true, all tools from that server skip tool-search deferral and are always available` — DONE (`services/mcp/types.ts` — added `alwaysLoad: z.boolean().optional()` field via shared `McpAlwaysLoadConfigSchema` to `McpStdioServerConfigSchema`, `McpSSEServerConfigSchema`, `McpHTTPServerConfigSchema`, `McpWebSocketServerConfigSchema`. `services/mcp/client.ts:1822` — `fetchToolsForClient` now sets `alwaysLoad: tool._meta['anthropic/alwaysLoad'] === true || client.config.alwaysLoad === true` on each Tool, so the existing `isDeferredTool()` early-return at `ToolSearchTool/prompt.ts:65` flips off deferral. Per-tool `_meta` and per-server config are OR'd — either way wins. Live-builds clean, no schema regression on existing configs since the new field is optional)
- [-] `Added claude plugin prune to remove orphaned auto-installed plugin dependencies; plugin uninstall --prune cascades` — SKIP (plugin/marketplace infra)
- [x] `Added a type-to-filter search box to /skills so you can find a skill in long lists without scrolling` — DONE in ff91630 (`SkillsMenu.tsx` is 233 LOC, not 1.5K — added controlled `<TextInput>` with `searchMode` toggle on `/`, case-insensitive substring match across name+description, `flatSkills` rebuilt from filtered groups so arrow-key navigation tracks the visible subset, selection clamped when the filtered list shrinks past the cursor. First Esc clears query, second exits search mode)
- [x] `PostToolUse hooks can now replace tool output for all tools via hookSpecificOutput.updatedToolOutput (previously MCP-only)` — DONE (added `updatedToolOutput?: unknown` field alongside the existing legacy `updatedMCPToolOutput` across `types/hooks.ts` (PostToolUse hookSpecificOutput schema, `HookResult`, `AggregatedHookResult`), `entrypoints/sdk/coreSchemas.ts` (`PostToolUseHookSpecificOutputSchema`), and `utils/hooks.ts` (PostToolUse JSON-parse extracts both fields, yields both, threaded through `HookResult`/`AggregatedHookResult` shapes). `services/tools/toolHooks.ts#runPostToolUseHooks` extends the union to `| { updatedToolOutput: Output }` and yields it whenever `result.updatedToolOutput !== undefined`, regardless of `isMcpTool(tool)`. `services/tools/toolExecution.ts:1552` adds a new `'updatedToolOutput' in hookResult` branch that applies to ALL tools (MCP-only branch above retained for backward compat). Documented `updatedMCPToolOutput` as deprecated in favor of `updatedToolOutput` in both schemas)
- [-] `Fullscreen mode: typing into the prompt no longer jumps scroll back to the bottom after you've scrolled up to read earlier output` — SKIP (deep fullscreen scroll-state interaction in `screens/REPL.tsx`'s `composedOnScroll` + the `userInputBaselineRef` follow-on-keystroke logic. The "scroll-back-on-typing" trigger needs a concrete repro to fix safely without regressing the working "follow-when-at-bottom" behavior; the existing `ink.tsx` displayCursor / didLayoutShift backstops handle most cases. Already partially mitigated by the 886d6da prevHeight thread that fixed scrollback duplication on full-resets — typing-induced reflows now don't ERASE_SCREEN)
- [-] `Dialogs that overflow the terminal are now scrollable with arrow keys, PgUp/PgDn, home/end, and mouse wheel in both fullscreen and non-fullscreen modes` — SKIP (general-purpose Modal-content scrolling — adding ScrollBox semantics + new keybinding wiring to every dialog that wraps content. Several of our dialogs (Settings, Permissions, /agents detail) already use the ScrollKeybindingHandler indirectly via `centeredModal` flow; non-fullscreen dialog scrolling would need ScrollKeybindingHandler to mount even without fullscreen, plus per-dialog content-overflow detection. Out of scope — too broad without a specific dialog reproducing the clipping)
- [-] `Clicking any line of a long URL that wraps across rows in fullscreen mode now opens the full URL` — SKIP (fullscreen-only URL hit-test feature — would need to add multi-row click handler resolution in `ink/render-node-to-output.ts` so a click on row N+1 of a wrap-spanning URL still maps to the wrapped URL's full string. OSC 8 hyperlink emission via `utils/hyperlink.ts` already handles the click-to-open case for terminals that support it; clicking a URL span is opt-in via the terminal's mouse handling. Without a concrete repro showing OUR fullscreen layout dropping clicks on wrapped URLs, blind multi-row hit-test changes risk regressing single-row clicks)
- [x] `SDK and claude -p: CLAUDE_CODE_FORK_SUBAGENT=1 now works in non-interactive sessions` — DONE (`tools/AgentTool/forkSubagent.ts#isForkSubagentEnabled` — non-interactive sessions used to hard-return false. Now they return true when `process.env.CLAUDE_CODE_FORK_SUBAGENT === '1'`. Coordinator-mode and `feature('FORK_SUBAGENT')`-disabled paths still short-circuit. Default behavior in `-p` / SDK mode unchanged unless the env var is explicitly set, so we don't surprise existing automation that doesn't expect fork-subagent semantics)
- [x] `--dangerously-skip-permissions no longer prompts for writes to .claude/skills/, .claude/agents/, and .claude/commands/` — DONE (split `isClaudeConfigFilePath` into `isClaudeSettingsPath` (settings.json — still always-ask, including under bypass) and a new `isClaudeContentDirPath` (the three content dirs). `checkPathSafetyForAutoEdit` returns the unsafe result with a new `bypassableUnderDangerousSkip: true` flag when the path is content-only (not settings); `permissions.ts` step 1g consumes the flag — bypass-immune gate skipped for content dirs only, so the existing step 2a `bypassPermissions` mode auto-allows writes. Settings.json and `.git/` / `.vscode/` / `.idea/` paths still require explicit approval. Live-verified in container: `Write` to `.claude/skills/probe/SKILL.md` under `--dangerously-skip-permissions` succeeded without a prompt and the file exists post-call)
- [-] `/terminal-setup now enables iTerm2's "Applications in terminal may access clipboard" setting so /copy works, including from tmux` — SKIP (iTerm2-specific macOS preference write — would require shelling out to `defaults write com.googlecode.iterm2 AllowClipboardAccess -bool true` from our `/terminal-setup`. Cross-platform contract (we run primarily on Linux/WSL) and our `/copy` already uses OSC 52 which works in iTerm2 + tmux + most modern terminals without needing this prefs flip. Worth revisiting only if a macOS user reports `/copy` failing via the OSC 52 path)
- [x] `MCP servers that hit a transient error during startup now auto-retry up to 3 times instead of staying disconnected` — DONE (`services/mcp/client.ts:2370` startup connection sweep — wrapped the initial `connectToServer` call in a 3-attempt retry loop with `isTransientStartupError` predicate that matches `ECONNREFUSED` / `ECONNRESET` / `ETIMEDOUT` / `EHOSTUNREACH` / generic timeout / "Connection terminated" / "socket hang up" in the failed-connection error message. Auth-challenge results (`needs-auth`) and non-transient failures bypass the retry. Each retry deletes the memoize cache entry via `connectToServer.cache.delete(getServerCacheKey(name, config))` so a fresh transport is constructed; fixed 250ms × attempt-index backoff)
- [-] `The terminal tab session title is now generated in your configured language setting` — SKIP (we don't ship the auto-tab-title feature in our fork. Upstream emits an OSC 2/0/L title escape with a Haiku-summarized session description that respects the user's `language` setting; our fork has no tab-title emitter at all (we set internal session titles via `setSessionTitle` for the claude.ai bridge but never write to terminal tabs). Translating-to-user-language only matters once that emitter exists)
- [-] `Claude.ai connectors with the same upstream URL are now deduplicated instead of appearing as duplicates` — SKIP (claude.ai connector-specific; already partially mitigated by our existing `main.tsx:2842` lazy dedup of plugin servers that duplicate claude.ai connectors)
- [-] `Vertex AI: support X.509 certificate-based Workload Identity Federation (mTLS ADC)` — SKIP (Vertex-specific; we don't target Google Vertex)
- [-] `Faster startup after upgrading: removed the Recent Activity panel from the release-notes splash` — SKIP (we don't ship Anthropic's release-notes splash with a Recent Activity panel — our release-notes UI just renders the changelog from `coffeegrind123/changelog` repo; no Recent Activity to remove)
- [-] `LSP diagnostic summaries now expand on click/ctrl+o and show the expand hint` — SKIP (UI polish — fullscreen-mode-only click handler in the diagnostic-summary collapsible. Implementation lives in compiled-React-output region; needs a concrete fullscreen-active repro to wire correctly without regressing the existing ctrl+o behavior. Low impact — diagnostics are already fully visible in non-fullscreen mode and via `/diagnostics` enumeration)
- [-] `SDK: mcp_authenticate now supports redirectUri for custom scheme completion and claude.ai connectors` — SKIP (SDK + claude.ai-connector-specific; not our primary surface)
- [x] `OpenTelemetry: added stop_reason, gen_ai.response.finish_reasons, and user_system_prompt (gated behind OTEL_LOG_USER_PROMPTS) to LLM request spans` — DONE (`services/observe/tracing.ts#recordLLMObservation` extends params with `stopReason`, `finishReasons[]`, `userSystemPrompt`. Span attributes now emit `stop_reason` + `observe.stop_reason` (Anthropic's raw value: `end_turn` / `tool_use` / `max_tokens` / `stop_sequence` / `pause_turn` / `refusal`), `gen_ai.response.finish_reasons` (OpenAI-aligned mapping: `end_turn|stop_sequence` → `['stop']`, `tool_use` → `['tool_calls']`, `max_tokens` → `['length']`, otherwise the raw reason), and `user_system_prompt` only when `OTEL_LOG_USER_PROMPTS=1` is set. `services/api/claude.ts:3019` populates the new params from the `stopReason` already tracked at the streaming layer (line 2346) plus the resolved `system` prompt — supports both the legacy string-system-prompt form and the SystemPromptParam[] array form. Default behavior unchanged when `OTEL_LOG_USER_PROMPTS` is unset)
- [-] `[VSCode] Voice dictation now respects the accessibility.voice.speechLanguage setting when no Claude Code language is configured` — SKIP (VSCode extension)
- [-] `[VSCode] /context now opens a native token usage dialog` — SKIP (VSCode extension)
- [-] `Fixed unbounded memory growth (multi-GB RSS) when processing many images in a session` — SKIP (the upstream regression is in their image-conversion pipeline retaining decoded buffers; our paths through `services/api/imageProcessing.ts` already release intermediate Buffers — and Bun's GC is more aggressive than Node's at returning pages. Without a concrete repro showing our fork leaking on the same workload, blind fixing risks regressions. Our distill compaction also already mitigates by compacting old image-bearing turns out of context)
- [-] `Fixed /usage leaking up to ~2GB of memory on machines with large transcript histories` — SKIP (Anthropic-quota /usage panel reads first-party `/api/quota`-style state. Our `/usage` shows local-session cost and per-provider quota for z.ai/DeepSeek; doesn't enumerate transcript history at /usage time, so the multi-GB regression here can't manifest)
- [-] `Fixed memory leak when long-running tools fail to emit a clear progress event` — SKIP (upstream description doesn't localize the leak — could be an unreleased AbortController, an event-listener that doesn't remove on tool completion, or an output-buffer that doesn't drain. Without a concrete repro, instrumentation-driven blind fixes risk regressing the working long-running-tool path. Our `services/tools/toolExecution.ts` already has `progressInterval = setInterval(...)` cleanup in MCP `callMCPTool` finally blocks, and `TaskOutput.ts` truncates output past a cap — most obvious leak surfaces are already covered)
- [x] `Fixed Bash tool becoming permanently unusable when the directory Claude was started in is deleted or moved mid-session` — DONE (`utils/Shell.ts` — extended the cwd-recovery walk from a single `getOriginalCwd()` fallback to a chain: `getOriginalCwd()` → `$HOME` → `$USERPROFILE` (Win) → `$TMPDIR` → `$TEMP` (Win) → `/tmp` (POSIX). Each candidate gets a `realpath()` probe; first existing one wins. Previously when both the active cwd AND the original cwd were deleted (the literal scenario in upstream's description — user `mv`s the directory the session was started in) the tool returned the dead-end "Please restart Claude" message on every subsequent call. Now we recover to a viable directory and `setCwdState(recoveredTo)` so the rest of the session sees the new cwd. Live-verified: cwd `/tmp/cwd-doomed-test` deleted before Bash invocation → tool reports `/tmp` from `pwd` instead of failing)
- [-] `Fixed --resume crashing on startup in external builds` — SKIP (parenthesised "external builds" — refers to Anthropic's external compiled-binary distribution. Our fork runs from source under Bun where the regression's specific minifier-DCE root cause can't manifest. Local `--resume` paths also already DONE in 64c457b for the older transcript-format crash)
- [x] `Fixed --resume failing on large sessions when a transcript line was corrupted by an unclean shutdown — the corrupt line is now skipped` — DONE (already in codebase, `utils/json.ts#parseJSONL` — all three implementations (`parseJSONLBun` fast path, `parseJSONLBuffer`, `parseJSONLString`) catch JSON.parse errors per-line and continue. The Bun path's `parseChunk` returns the error position, then `parseJSONLBun` skips to the next newline (`indexOf('\n', offset)`) and re-enters `parse(data, offset)` — so a single corrupt line truncates only itself, not the rest of the file. `loadTranscriptFile`'s `parseJSONL<Entry>(buf)` call inherits this behavior unchanged)
- [-] `Fixed thinking.type.enabled is not supported error when using Bedrock application inference profile ARNs` — SKIP (Bedrock-specific; we route through z.ai/DeepSeek/NIM/Anthropic-direct, not AWS Bedrock)
- [-] `Fixed Microsoft 365 MCP OAuth failing with duplicate or unsupported prompt parameter` — SKIP (SDK-level — `@modelcontextprotocol/sdk`'s OAuth dance owns the `prompt=` param emission; auto-fixes on next SDK upgrade. Microsoft 365 MCP is also rare in our user base — primary MCP servers in this fork are zendriver / ghidra / computer-use)
- [x] `Fixed scrollback duplication when pressing Ctrl+L or triggering a redraw in non-fullscreen mode on tmux, GNOME Terminal, Windows Terminal, and Konsole` — DONE in 886d6da (same `ink/log-update.ts` patch that covers the 2.1.120 entry — threading `prev.screen.height` into `fullResetSequence_CAUSES_FLICKER(prevHeight)` at L248 / L272 / L391 means Ctrl+L and other redraw triggers in inline mode emit `eraseLines(prevHeight)` instead of `ERASE_SCREEN + CURSOR_HOME`, so the prior frame doesn't slide into scrollback. Trigger set in upstream's description (Ctrl+L, redraw on tmux/GNOME/Konsole/Windows Terminal) is exactly what the patch covers)
- [x] `Fixed claude.ai MCP connectors silently disappearing when the connector-list fetch hits a transient auth error at startup` — DONE in ff91630 (`services/mcp/claudeai.ts` — added `fetchClaudeAIMcpServersWithRetry()` with 3 attempts and 250ms × attempt linear backoff. `isTransientFetchError()` classifier flags 401/408/429/500–503 + `ECONN*`/`ETIMEDOUT`/`EHOSTUNREACH` as retryable; permanent errors fall through immediately. The outer `catch` block at the memoized fetch logs the final status/code so users diagnosing a missing-connectors session can see what failed instead of getting a silent empty `{}`)
- [-] `Fixed "Always allow" rules for built-in tools in remote sessions not surviving worker restarts` — SKIP (Remote Control Sessions / claude.ai cloud-worker infra; our remote story is `claude ssh` / acp-link / self-hosted CCR runner, none of which use this worker-restart-and-restore flow)
- [-] `Fixed NO_PROXY not being respected for all HTTP clients when set via managed-settings.json under the native build` — SKIP (parenthesised "native build" — bug lives in Anthropic's compiled-binary HTTP client wiring; our fork runs Bun's `fetch` which honours `NO_PROXY` natively via Node's `undici` agent. We also don't process `managed-settings.json` to inject proxy env on first-party Anthropic's enterprise path)
- [-] `Fixed managed settings approval prompt exiting the session even when accepted — now applies settings and continues` — SKIP (requires the first-party `api.anthropic.com` remote-managed-settings sync flow — `services/remoteManagedSettings/` only fires when claude.ai is the auth backend AND the org has dangerous-settings policies pushed remotely. Our primary auth path is `ANTHROPIC_AUTH_TOKEN` → z.ai/DeepSeek/NIM where this code path doesn't run. The approved-branch logic in `securityCheck.tsx#handleSecurityCheckResult` already returns `true` correctly; the upstream regression is presumably a subtle Ink-render lifecycle interaction between the dialog's `<AppStateProvider>` instance and the parent session that we can't reliably reproduce or test without the remote-settings infrastructure)
- [x] `Fixed /usage returning "rate limited" after a stale OAuth token — now refreshes automatically` — DONE in ff91630 (`services/api/usage.ts#fetchUtilization` — pre-flight refresh: if `getClaudeAIOAuthTokens()` reports the token is `isOAuthTokenExpired()`, we call `checkAndRefreshOAuthTokenIfNeeded()` before hitting `/api/oauth/usage` so the server doesn't reject a token it already rotated out. Plus a 429-retry path that force-refreshes (`checkAndRefreshOAuthTokenIfNeeded(0, true)`) and retries once with fresh `getAuthHeaders()` so transient rate-limiter blips and stale-token-treated-as-rate-limit responses both resolve. Other status codes propagate)
- [x] `Fixed invalid legacy enum values in settings.json invalidating the entire settings file` — DONE (`utils/settings/settings.ts` — new `dropLegacyEnumKeysAndRetry` helper extends the existing `filterInvalidPermissionRules` recovery pattern. When `SettingsSchema().safeParse` reports `invalid_enum_value` / `invalid_value` / `invalid_literal` / `invalid_union` issues, the recovery deep-clones the parsed JSON, walks each issue's path to the deepest reachable parent, and removes just the offending leaf (or splices the offending array element when the path's tail is an index). The schema is then re-parsed against the stripped data; success returns the partial settings + a `Dropped <key>: invalid legacy enum value` warning per dropped path. Live-verified in container: `permissions.defaultMode = "totally-fake-value-xyz"` no longer rejects sibling `verbose: true` and `outputStyle: "default"` — assistant reports `verbose **enabled**` from the recovered file)
- [-] `Fixed /usage dialog content being clipped when no-flicker mode is off` — SKIP (UI clipping in our `/usage` Settings dialog only manifests when the centered Modal layout exceeds terminal rows AND fullscreen is off — our wide-layout Usage.tsx already removed the clipping prone progress-bar+labels overlap (BACKLOG #2.1.119 entry). Without a concrete repro showing OUR /usage clipping under specific terminal sizes, blind clipping fixes risk regressing the working layouts)
- [x] `Fixed /focus showing "Unknown command" when the fullscreen renderer is off — now explains how to enable it` — DONE (`commands/focus.ts` — early-return guard via `isFullscreenEnvEnabled()`. When fullscreen is off, the command emits the system message `Focus view requires fullscreen mode. Set CLAUDE_CODE_NO_FLICKER=1 in your environment (or unset it on first-party builds where the default is on) and restart Claude.` instead of silently flipping `isFocusView` state that the non-fullscreen renderer ignores. Live-verified in container with `CLAUDE_CODE_NO_FLICKER=0` — model receives the actionable hint and proceeds correctly)
- [-] `Fixed embedded grep/find/rg shell wrappers failing when the running binary is deleted mid-session — now falls back to installed tools` — SKIP (companion to the parenthesised "macOS/Linux native builds" item below — embedded grep/find/rg are bundled inside Anthropic's compiled native binary; we run from source under Bun and shell out to the host's `/usr/bin/*` tools, which can't get deleted by claude restarting in place)
- [-] `Reduced peak file descriptor usage during find in the Bash tool on large directory trees` — SKIP (paired with the 2.1.120 host-crash fix that's annotated "macOS/Linux native builds"; both target the embedded `find` shell wrapper that ships in Anthropic's compiled native binaries. Our fork runs from source under Bun and shells out to the installed `/usr/bin/find`, where the host kernel's per-process fd limits already bound usage. Not applicable)

## 2.1.120

- [-] `Windows: Git for Windows (Git Bash) is no longer required — when absent, Claude Code uses PowerShell as the shell tool` — SKIP (Windows-specific shell-tool fallback. Our primary runtime is Linux/WSL; Windows users either use Git Bash or run inside WSL where `bash` is always available)
- [-] `Added claude ultrareview [target] subcommand to run /ultrareview non-interactively from CI or scripts — prints findings to stdout (--json for raw output) and exits 0 on completion or 1 on failure` — SKIP (`/ultrareview` is an Anthropic-hosted, billed multi-agent cloud-review feature that's user-triggered only and not present as a slash command in this fork. Our session-specific system prompt explicitly instructs the agent NOT to launch it via Bash or any other path. A non-interactive `claude ultrareview` CLI wrapping it would require the upstream cloud service we don't talk to. Users running ultrareview-style review pipelines should use `/bug-hunter` (4-agent adversarial pipeline shipped in 7d293e9) which serves the same role end-to-end locally on the configured provider)
- [x] `Skills can now reference the current effort level with ${CLAUDE_EFFORT} in their content` — DONE (`skills/loadSkillsDir.ts#getPromptForCommand` + `tools/SkillTool/SkillTool.ts` remote-skill loader — `${CLAUDE_EFFORT}` substitution chained after `${CLAUDE_SESSION_ID}`. Resolves via `getDisplayedEffortLevel(model, appState.effortValue)` so it matches the `/effort` status-bar value (precedence: env `CLAUDE_CODE_EFFORT_LEVEL` → AppState → model default). `includes()` guard skips the AppState read on skills that don't reference the var. Live-verified in container: skill body `**${CLAUDE_EFFORT}**` with `CLAUDE_CODE_EFFORT_LEVEL=high` → `**high**`)
- [x] `Set AI_AGENT environment variable for subprocesses so gh can attribute traffic to Claude Code` — DONE (`utils/subprocessEnv.ts` — new `injectAiAgent` helper sets `AI_AGENT=claude-code` on the subprocess env unless already set; chained after `injectPluginBinPaths` in both the scrub and non-scrub branches of `subprocessEnv()`. Inherits to all five spawn sites — Bash/Shell, MCP stdio, LSP, hooks, ShellSnapshot. Live-verified in container: `Bash: env | grep AI_AGENT` → `AI_AGENT=claude-code`)
- [-] `Spinner tips that recommend installing the desktop app or creating skills/agents are now hidden when you already have them` — SKIP (our `Spinner.tsx` ships only two tips — `/clear` (after 30 min idle) and `/btw` (after 30 s on first usage). The upstream-Anthropic-specific "install the desktop app" / "create your first skill/agent" tips that need state-based filtering aren't present in our fork at all)
- [x] `Show a "use PgUp/PgDn to scroll" hint when the terminal sends arrow keys instead of scroll events` — DONE (`components/ScrollKeybindingHandler.tsx` — new `arrowBurstRef` state in the existing selection-clearing `useInput` handler tracks bare ↑/↓ keypress timestamps (no shift/ctrl/meta/super modifiers). Five within 350ms — faster than any human types, characteristic of a wheel-encoder mapping scroll to arrows on Apple Terminal sans mouse-tracking and a few Windows emulators — fires a one-shot `addNotification({key: 'arrow-scroll-hint', text: 'wheel sent as ↑/↓ keys · use PgUp/PgDn to scroll faster', color: 'suggestion', priority: 'low', timeoutMs: 6000})`. `hinted: true` flag on the ref guards against re-firing in the same session)
- [-] `Faster session start when you have many claude.ai connectors configured but not authorized` — SKIP (claude.ai-connector specific — the session-start latency they're optimizing comes from probing the user's claude.ai-account-attached MCP connectors. Our primary auth path is API tokens (z.ai/DeepSeek/NIM) and the claude.ai connector flow is rarely hit. Already covered by the existing `CLAUDE_AI_MCP_TIMEOUT_MS` lazy-dedup at `main.tsx:2842`)
- [x] `The auto mode denial message now links to the configuration docs` — DONE (`hooks/useCanUseTool.tsx` — auto-mode denial notification now appends `https://docs.claude.com/en/docs/claude-code/iam` after the existing `· /permissions` shortcut. In-CLI navigation preserved; users with terminal hyperlink support get a clickable link to the IAM/auto-mode configuration page)
- [-] `claude plugin validate now accepts $schema, version, and description at the top level of marketplace.json and $schema in plugin.json` — SKIP (plugin/marketplace infra)
- [x] `Auto-compact in auto mode now displays auto (lowercase, no token count) instead of a misleading token value` — DONE (`components/TokenWarning.tsx` — when `isAutoModeActive()` from `utils/permissions/autoModeState.ts` is true, the autocompactLabel renders as the literal string `auto` instead of `${percent}% until auto-compact`. Reactive-only-mode label left alone (different counter, not driven by auto-mode). Rationale: in auto mode the user has no decision to make — compaction fires automatically — so a precise percentage misleadingly implies actionable state)
- [x] `Fixed pressing Esc during a stdio MCP tool call closing the entire server connection (regression in 2.1.105)` — DONE (`services/mcp/client.ts` — defensive `AbortError` guard at the head of the stdio transport's `onerror` handler. AbortError reflected through the transport (the SDK does this in some flows) was either being miscategorised as a parse error (advancing the `MAX_STDIO_PARSE_ERRORS=10` disconnect counter) or surfacing as a generic transport error in the logs that downstream pipe inference treated as a crash. Now: AbortError logs at debug level and returns immediately — the server's child process is unaffected by the user's Esc on a single in-flight request. Parse-error counter, generic transport-error logspew, and `MAX_ERRORS_BEFORE_RECONNECT`-driven reconnects all keep their existing semantics for actual transport failures)
- [ ] `Fixed /rewind and other interactive overlays not responding to keyboard input after launching with claude --resume`
- [x] `Fixed terminal scrollback duplication in non-fullscreen mode (resize, dialog dismiss, long sessions)` — DONE in 886d6da (`ink/log-update.ts` — threaded `prev.screen.height` into the three remaining `fullResetSequence_CAUSES_FLICKER(undefined)` call sites at L248 (scrollback row change branch), L272 (shrinking-overflow branch), L391 (`needsFullReset` post-diff branch). Commit `a725898` patched only the resize branch; the other three offscreen full-reset paths in inline mode kept falling back to `ERASE_SCREEN + CURSOR_HOME`, leaving the prior render in scrollback. Repro lined up with upstream's "resize, dialog dismiss, long sessions" trigger set)
- [-] `Fixed DISABLE_TELEMETRY / CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC not suppressing usage metrics telemetry for API and enterprise users` — SKIP (already neutralized in our fork — `src/services/analytics/` is fully stubbed (preserves API surface, all no-ops), `cli.tsx:37` sets `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` unconditionally at entrypoint. The specific upstream regression where the env var didn't reach the usage-metrics emitter cannot manifest because the emitter itself is a no-op)
- [-] `Fixed false-positive "Dangerous rm operation" permission prompts in auto mode for multi-line bash commands containing both a pipe and a redirect` — SKIP (sits in `tools/BashTool/pathValidation.ts#checkDangerousRemovalPaths` (the source of the literal "Dangerous rm operation detected" message at line 96) which is reached via `bashPermissions.ts` → `createPathChecker` → AST `astCommands` argv-extraction. CLAUDE.md "Don't Touch" list explicitly covers "Bash security checks — 22 validators, AST parsing, injection detection" and "Path validation". Without a concrete repro from upstream, the multi-line pipe+redirect false-positive can't be isolated against our parser's behavior; touching this code blind risks regressing a security-critical path. Worst-case impact for users hitting the false positive is one extra permission prompt — the dangerous-path check `behavior: 'ask'`s, doesn't auto-deny, so the user is still in control)
- [ ] `Fixed long selection menus clipping below the terminal in fullscreen mode — the focused option now stays on screen as you scroll`
- [ ] `Fixed Write tool output collapsing instead of expanding when clicking "+N lines" in fullscreen`
- [ ] `Fixed slash command picker jumping while typing, and improved highlight to only match contiguous substrings in blue`
- [-] `Fixed /plugin marketplace failing to load when one entry uses an unrecognized source format — that entry is shown but installing it prompts you to update` — SKIP (plugin/marketplace infra)
- [-] `[VSCode] /usage now opens the native Account & Usage dialog instead of returning plain-text session cost` — SKIP (VSCode extension)
- [-] `[VSCode] Voice dictation now respects the language setting in ~/.claude/settings.json` — SKIP (VSCode extension)
- [-] `Fixed find in the Bash tool exhausting open file descriptors on large directory trees, causing host-wide crashes (macOS/Linux native builds)` — SKIP (parenthesized "macOS/Linux native builds" — the bug lives in Anthropic's compiled binary's embedded find wrapper; our fork shells to system `find` via Bun)

## 2.1.119

- [-] `/config settings (theme, editor mode, verbose, etc.) now persist to ~/.claude/settings.json and participate in project/local/policy override precedence` — SKIP (our fork already persists theme/verbose/editorMode via `saveGlobalConfig` to `~/.claude/.json` (legacy globalConfig), and newer settings like `fuelgaugeEnabled` go through `updateSettingsForSource('userSettings', …)` into `~/.claude/settings.json`. Migrating the legacy-path settings would rewire ~30 `Config.tsx` onChange handlers + every read site. High churn, low user-visible benefit since persistence DOES already work — it just uses a different file)
- [x] `Added prUrlTemplate setting to point the footer PR badge at a custom code-review URL instead of github.com` — DONE (`utils/ghPrStatus.ts#applyPrUrlTemplate` reads `prUrlTemplate` from settings, substitutes `{owner}`, `{repo}`, `{number}`, `{url}`. Parses owner/repo out of the original github URL via `new URL().pathname.split('/')`. Falls back to the original URL on parse failure or missing setting)
- [x] `Added CLAUDE_CODE_HIDE_CWD environment variable to hide the working directory in the startup logo` — DONE in `logoV2Utils.ts#getLogoDisplayData` — env gate returns empty `cwd` string, both LogoV2 and CondensedLogo renderers degrade gracefully)
- [x] `--from-pr now accepts GitLab merge-request, Bitbucket pull-request, and GitHub Enterprise PR URLs` — DONE (`screens/ResumeConversation.tsx#parsePrIdentifier` tries 4 URL patterns: `/pull/N` (GitHub/GHE), `/merge_requests/N` (GitLab), `/-/merge_requests/N` (GitLab `/-/` prefix), `/pull-requests/N` (Bitbucket). Host is not validated — self-hosted forges work too)
- [x] `--print mode now honors the agent's tools: and disallowedTools: frontmatter, matching interactive-mode behavior` — DONE (`cli/print.ts` — after building `filteredTools`, resolve the active main-thread agent via `getMainThreadAgentType()` + `agents.find(...)`, then pipe `filteredTools` through `resolveAgentTools(agent, tools, isAsync=false, isMainThread=true)`. `resolvedTools` replaces `filteredTools` when the agent's tools/disallowedTools list actually constrains the pool)
- [x] `--agent <name> now honors the agent definition's permissionMode for built-in agents` — DONE (`main.tsx` — after `mainThreadAgentDefinition` resolution, if the agent declares `permissionMode` and the user didn't pass `--permission-mode` or `--dangerously-skip-permissions` on the CLI, override `toolPermissionContext.mode`. Explicit CLI flags still win)
- [-] `PowerShell tool commands can now be auto-approved in permission mode, matching Bash behavior` — SKIP (PowerShell-specific, Linux container only)
- [x] `Hooks: PostToolUse and PostToolUseFailure hook inputs now include duration_ms (tool execution time, excluding permission prompts and PreToolUse hooks)` — DONE (new `durationMs` parameter threaded `toolExecution.ts` → `toolHooks.ts` → `hooks.ts#executePostToolHooks`/`executePostToolUseFailureHooks`, emitted into `PostToolUseHookInput` / `PostToolUseFailureHookInput` as `duration_ms` when defined. Measured from `startTime` set just before `tool.call()` — permission + PreToolUse excluded by construction)
- [x] `Subagent and SDK MCP server reconfiguration now connects servers in parallel instead of serially` — DONE (`cli/print.ts#reconcileMcpServers` — the add-new-servers loop was a serial `for (const name of ...) await connectToServer()`. Now uses `Promise.all` over the servers-to-add list; connect + fetch-tools happen concurrently. Cleanup-old loop kept serial — it touches shared client state and is already fast)
- [-] `Plugins pinned by another plugin's version constraint now auto-update to the highest satisfying git tag` — SKIP (plugin/marketplace infra)
- [x] `Vim mode: Esc in INSERT no longer pulls a queued message back into the input; press Esc again to interrupt` — DONE (`PromptInput.tsx` Esc handler — added `isVimInInsertMode` guard before `popAllCommandsFromQueue`. First Esc in vim INSERT mode switches to NORMAL (handled earlier in the vim hook), second Esc in NORMAL falls through to the normal Esc pipeline)
- [x] `Slash command suggestions now highlight the characters that matched your query` — DONE in f4a2df4 (Fuse `includeMatches: true` + per-char bold rendering in `PromptInputFooterSuggestions.tsx`; match ranges computed from commandName/alias/partKey/descriptionKey hits and merged before rendering via `renderHighlighted`)
- [x] `Slash command picker now wraps long descriptions onto a second line instead of truncating` — DONE (`PromptInputFooterSuggestions.tsx` — when description is wider than the first-line budget, the overflow tail renders as a second indented `<Text>` below, wrapped in a `Box flexDirection="column"`. First line keeps its `wrap="truncate"` budget so it still shows name + tag + leading description chars)
- [x] `owner/repo#N shorthand links in output now use your git remote's host instead of always pointing at github.com` — DONE (`utils/markdown.ts#linkifyIssueReferences` now interpolates a cached host from `getRemoteUrl() + normalizeGitRemoteUrl()`. Cache populated by fire-and-forget on first call; first render falls back to `github.com`, subsequent renders honor the remote host. GHE / GitLab / Bitbucket hosts get correct absolute links)
- [-] `Security: blockedMarketplaces now correctly enforces hostPattern and pathPattern entries` — SKIP (marketplace infra)
- [x] `OpenTelemetry: tool_result and tool_decision events now include tool_use_id; tool_result also includes tool_input_size_bytes` — DONE (`toolExecution.ts` — `logOTelEvent('tool_decision', …)` now carries `use_id`; both success and failure `tool_result` events add `tool_input_size_bytes` alongside the existing `tool_result_size_bytes`. Observers can now correlate decision→result pairs and spot oversized inputs)
- [x] `Status line: stdin JSON now includes effort.level and thinking.enabled` — DONE (`components/StatusLine.tsx#buildStatusLineCommandInput` now threads `effortValue` from AppState and emits `effort.level` (gated on `modelSupportsEffort`) + `thinking.enabled` (gated on `modelSupportsThinking`). Status-line scripts can now check `'effort' in input` reliably)
- [x] `Fixed pasting CRLF content (Windows clipboards, Xcode console) inserting an extra blank line between every line` — DONE (`PromptInput.tsx#onTextPaste` now collapses `\r\n` → `\n` BEFORE the bare-`\r` → `\n` pass. Old code ran `.replace(/\r/g, '\n')` on CRLF content, doubling every newline)
- [-] `Fixed multi-line paste losing newlines in terminals using kitty keyboard protocol sequences inside bracketed paste` — SKIP (complex interaction between kitty keyboard protocol's per-key CSI-u sequences and bracketed-paste mode where the emitted bytes interleave. Fix requires tokenizer state that distinguishes bracketed-paste newlines from individual keypresses within paste. Low-frequency — kitty users can set `TERM=xterm-256color` or disable kitty keyboard protocol via `/terminal-setup` as a workaround)
- [-] `Fixed Glob and Grep tools disappearing on native macOS/Linux builds when the Bash tool is denied via permissions` — SKIP (native builds, we run Bun)
- [x] `Fixed scrolling up in fullscreen mode snapping back to the bottom every time a tool finishes` — DONE in f4a2df4 (tightened positional follow guard in `render-node-to-output.ts` — when `node.stickyScroll === false` the auto-follow only fires if the user is EXACTLY at prev max (click-at-max case, where stickiness was broken by click-select rather than scroll-up). Any scroll-up that lands short of max keeps the viewport where it is, even if the content grew and happens to match the old max by coincidence)
- [-] `Fixed MCP HTTP connections failing with "Invalid OAuth error response" when servers returned non-JSON bodies for OAuth discovery requests` — SKIP (bug lives in `@modelcontextprotocol/sdk`'s `discoverOAuthServerInfo` which throws on non-JSON response bodies — our fork imports the SDK at version 0.x; monkey-patching `node_modules` is fragile. Fix lands naturally on next SDK upgrade)
- [x] `Fixed Rewind overlay showing "(no prompt)" for messages with image attachments` — DONE (`MessageSelector.tsx` — scan entire content array for first text block (not just `lastBlock`); fall back to "(image)" when the message is image-only. Mixed image+text messages now display their caption)
- [x] `Fixed auto mode overriding plan mode with conflicting "Execute immediately" instructions` — DONE (`getAutoModeAttachments` in `utils/attachments.ts` now suppresses the auto-mode attachment when `mode === 'plan'` with auto-active. Plan-mode's own reminder stays authoritative; auto-mode's "execute immediately/prefer action over planning" no longer contradicts it)
- [x] `Fixed async PostToolUse hooks that emit no response payload writing empty entries to the session transcript` — DONE (`getAsyncHookResponseAttachments` in `utils/attachments.ts` now filters out PostToolUse/PostToolUseFailure attachments that have empty response body, empty stdout/stderr, and exit code 0; previously such hooks created noisy `async_hook_response` entries the model had to skip)
- [x] `Fixed spinner staying on when a subagent task notification is orphaned in the queue` — DONE (`messageQueueManager.ts` adds `getCommandQueueActiveLength(isAgentAlive)` + `dropOrphanedNotifications(isAgentAlive)`; REPL spinner gate now uses the active count with `tasks[agentId].status === 'running'` as the live-agent predicate. Task-notifications from exited/killed subagents stop holding the spinner on)
- [-] `Tool search is now disabled by default on Vertex AI to avoid an unsupported beta header error (opt in with ENABLE_TOOL_SEARCH)` — SKIP (Vertex-specific; we don't target Vertex as primary runtime)
- [x] `Fixed @-file Tab completion replacing the entire prompt when used inside a slash command with an absolute path` — DONE (`useTypeahead.tsx` directory branch: checks `extractCompletionToken(input, cursorOffset, true)` for an `@`-prefixed token first; when present, uses the general-path branch's in-place `applyDirectorySuggestion` instead of the "slash-command replace-argument" branch. Previously `/grep @/abs/path` would wipe `/grep ` + anything before the cursor)
- [-] `Fixed a stray p character appearing at the prompt on startup in macOS Terminal.app via Docker or SSH` — SKIP (platform-specific — we can't reproduce without macOS Terminal.app + Docker/SSH. Upstream's fix is presumably filtering a DECRPM "mode report" response (CSI `? … $ p`) that Terminal.app returns even when not queried. Filtering in `src/ink/termio/csi.ts` would be speculative. Primary runtime is Linux/WSL terminals that don't emit this response)
- [-] `Fixed ${ENV_VAR} placeholders in headers for HTTP/SSE/WebSocket MCP servers not being substituted before requests` — SKIP (already ahead: `services/mcp/config.ts:584-598` `expandEnvVars` handles `sse`/`http`/`ws` types and calls `mapValues(remoteConfig.headers, expandString)` so each header value goes through `expandEnvVarsInString` which supports `${VAR}` and `${VAR:-default}`. Called from all 5 validation entry points with `expandVars: true`)
- [-] `Fixed MCP OAuth client secret stored via --client-secret not being sent during token exchange for servers requiring client_secret_post` — SKIP (SDK-level — lives in `@modelcontextprotocol/sdk`'s token-exchange flow; auto-includes on next SDK upgrade)
- [x] `Fixed /skills Enter key closing the dialog instead of pre-filling /<skill-name> in the prompt` — DONE in f4a2df4 (`SkillsMenu.tsx` now tracks a `selectedIndex` across a flat navigation array (projectSettings → userSettings → policySettings → plugin → mcp, matching visible render order); arrow keys move within the grouped display, Enter fires `onExit(undefined, { nextInput: '/<name> ' })`, trailing space positions cursor for args. Token-sort toggle via `t` preserved)
- [x] `Fixed /agents detail view mislabeling built-in tools unavailable to subagents as "Unrecognized"` — DONE (`resolveAgentTools` in `tools/AgentTool/agentToolUtils.ts` now builds a `knownToolNames` superset from pre-filter `availableTools`. Tools that are known built-ins but filtered out by `filterToolsForAgent` for this subagent get routed to `validTools` instead of `invalidTools`)
- [-] `Fixed MCP servers from plugins not spawning on Windows when the plugin cache was incomplete` — SKIP (Windows + plugin)
- [-] `Fixed /export showing the current default model instead of the model the conversation actually used` — SKIP (our `/export` writes only the rendered conversation body via `renderMessagesToPlainText`; no model header line is emitted, so upstream's stale-label bug doesn't apply)
- [-] `Fixed verbose output setting not persisting after restart` — SKIP (our `Config.tsx#onChangeVerbose` already calls `saveGlobalConfig` which persists to `~/.claude/.json`; on restart the setting is re-read via `getGlobalConfig().verbose`. Upstream's bug-fix targets the settings.json migration path we opted out of — see parent item above)
- [-] `Fixed /usage progress bars overlapping with their "Resets …" labels` — SKIP (already ahead: our fork's `Settings/Usage.tsx` wide-layout branch (maxWidth ≥ 62) intentionally removed the progress bar and renders "Resets …" + "N% used" on a single `justifyContent="space-between"` row — no overlap possible. The narrow-layout branch stacks the bar and text in a flex-column. Upstream is fixing an overlap that only exists in their wide-layout-with-bar design we opted out of)
- [-] `Fixed plugin MCP servers failing when ${user_config.*} references an optional field left blank` — SKIP (plugin)
- [-] `Fixed list items containing a sentence-final number wrapping the number onto its own line` — SKIP (upstream description doesn't localize the bug; our markdown renderer goes through marked.js tokens and Ink's Text wrap, no sentence-final number re-parsing. Without a concrete repro the risk of a speculative fix breaking working wraps outweighs the UX gain)
- [-] `Fixed /plan and /plan open not acting on the existing plan when entering plan mode` — SKIP (requires reproducing an "existing plan is on disk but /plan/plan open didn't pick it up on mode-switch" race. Our `/plan` command's persistence flow via `plans.ts` looks correct — `copyPlanForResume`/`persistFileSnapshotIfRemote` wire to plan file on enter. Without a repro we can't confirm the narrow bug; risk of regressing the working path is higher than the reward)
- [-] `Fixed skills invoked before auto-compaction being re-executed against the next user message` — SKIP (the fix lives in the skill-attachment flow post-compact. Our fork already filters out `sentSkillNames` across compact boundaries (see `compact.ts:964` comment: "Intentionally NOT resetting sentSkillNames"). The specific double-execution upstream is fixing would need reproducing against a skill that writes a persistent instruction; not easy to verify without the exact repro)
- [-] `Fixed /reload-plugins and /doctor reporting load errors for disabled plugins` — SKIP (plugin)
- [-] `Fixed Agent tool with isolation: "worktree" reusing stale worktreeS from prior sessions` — SKIP (our `AgentTool.tsx#createAgentWorktree` slug comes from `earlyAgentId.slice(0, 8)` where `earlyAgentId = createAgentId()` is 1 char prefix + 16 random hex = 64 bits entropy. All AgentTool call sites use unlabeled `createAgentId()` so slugs are fully random. `getOrCreateWorktree`'s `existed: true` fast-path can only fire on a 1-in-268M slug collision, not the deterministic reuse upstream's fix targets. `removeAgentWorktree` already cleans up unchanged worktrees on completion, `cleanupStaleAgentWorktrees` sweeps the 30-day cutoff)
- [x] `Fixed disabled MCP servers appearing as "failed" in /status` — DONE (`utils/status.tsx#buildMcpProperties` byState now includes `disabled` bucket; previously fell through to `failed` via `else byState.failed++`, painting intentionally-off servers red in the Status pane)
- [x] `Fixed TaskList returning tasks in arbitrary filesystem order instead of sorted by ID` — DONE in `utils/tasks.ts#listTasks` — numeric sort on task.id (fall back to string compare on non-numeric IDs for safety)
- [x] `Fixed spurious "GitHub API rate limit exceeded" hints when gh output contained PR titles mentioning "rate limit"` — DONE in `BashTool.tsx` — detection now scans lines individually and requires a structural marker (error:/failed:/http 403/http 429/graphql:/gh:/secondary rate limit/api rate limit exceeded) on the SAME line as "rate limit", so a PR title/body mention doesn't match
- [-] `Fixed SDK/bridge read_file not correctly enforcing size cap on growing files` — SKIP (SDK/bridge-specific — the `read_file` endpoint lives in the SDK server path, our fork's primary surface is `FileReadTool` which already has size-cap guards (`FileEditTool.ts MAX_EDIT_FILE_SIZE` pattern). Users mostly don't hit the SDK `read_file` endpoint directly)
- [-] `Fixed PR not linked to session when working in a git worktree` — SKIP (our `ghPrStatus.ts#fetchPrStatus` runs `gh pr view` with the default cwd via `execFileNoThrow` → `getCwd()`. In a worktree, `getCwd()` returns the worktree path where `gh` should resolve the PR correctly. Upstream is fixing a different detection path we may not share. Without a repro I risk regressing our working path)
- [x] `Fixed /doctor warning about MCP server entries overridden by a higher-precedence scope` — DONE in f4a2df4 (`detectMcpScopeShadows()` in `services/mcp/utils.ts` scans user/project/local per-scope server maps (precedence plugin<user<project<local per config.ts:1231); new `McpShadowedServersSection` in `McpParsingWarnings.tsx` renders duplicates with winning scope + `describeMcpConfigFilePath()` paths for each shadowed scope. Appears in both `/doctor` and the `/mcp` panel)
- [-] `Windows: removed false-positive "Windows requires 'cmd /c' wrapper" MCP config warning` — SKIP (Windows-specific)
- [-] `[VSCode] Fixed voice dictation's first recording producing nothing on macOS while the microphone permission prompt is showing` — SKIP (VSCode extension)

## 2.1.118

- [~] `Added vim visual mode (v) and visual-line mode (V) with selection, operators, and visual feedback` — PARTIAL in f4a2df4 (added `VISUAL` and `VISUAL_LINE` VimState variants carrying `startOffset`; v/V from NORMAL idle enters the mode; h/j/k/l/w/b/0/$/arrows extend the selection via the existing motion dispatcher; d/y/c apply to `[min(start,cursor), max(start,cursor))` (VISUAL_LINE snaps to enclosing newlines) and return to NORMAL; Esc exits; v in VISUAL_LINE toggles to VISUAL and vice-versa. Deferred: selection-range highlight rendering in Cursor — operators work correctly without it but the selected range isn't visually distinguished yet)
- [x] `Merged /cost and /stats into /usage — both remain as typing shortcuts that open the relevant tab` — DONE partial (`/stats` converted from Stats component to Settings dialog opened on "Stats" tab, matching /usage dialog shell. `/cost` intentionally kept as `LocalCommandCall` text output so `supportsNonInteractive: true` continues to work in `claude -p "/cost"` pipes — converting to local-jsx would break that headless use case. Interactive `/cost` still prints the total cost as text — acceptable regression vs. upstream to preserve the non-interactive contract)
- [~] `Create and switch between named custom themes from /theme, or hand-edit JSON files in ~/.claude/themes/; plugins can also ship themes via a themes/ directory` — PARTIAL in f4a2df4 (`~/.claude/themes/*.json` loader with 2s in-process cache in `utils/theme.ts` — `getCustomTheme(name)` + `getCustomThemeNames()`. Each JSON file is merged over `darkTheme` so partial palettes inherit missing keys. `getTheme(name: string)` now resolves custom names before the built-in switch, built-ins still win on name collision. `/theme` picker appends "<name> (custom)" rows. Deferred: plugin-manifest `themes/` field — requires extending `PluginManifestSchema` + a dedicated `loadPluginThemes.ts`)
- [x] `Hooks can now invoke MCP tools directly via type: "mcp_tool"` — DONE in f4a2df4 (new `McpToolHookSchema` in `schemas/hooks.ts` with `server`, `tool`, `args`, `if`, `timeout`, `statusMessage`, `once` fields; `utils/hooks/execMcpToolHook.ts` resolves the server from `appState.mcp.clients`, substitutes `$ARGUMENTS` placeholder in string args with the hook-input JSON, calls `callMCPToolWithUrlElicitationRetry`, serializes text/image/resource content blocks into the output string; `utils/hooks.ts` dispatches `hook.type === 'mcp_tool'` alongside the http/prompt/agent branches with aborted/non_blocking_error/success attachments; `if`-condition and SessionStart filter gates updated to include the new type)
- [x] `Added DISABLE_UPDATES env var to completely block all update paths including manual claude update — stricter than DISABLE_AUTOUPDATER` — DONE in `utils/config.ts#getAutoUpdaterDisabledReason` — checked before DISABLE_AUTOUPDATER so the `claude update` CLI honors it too
- [-] `WSL on Windows can now inherit Windows-side managed settings via the wslInheritsWindowsSettings policy key` — SKIP (Windows-WSL bridge)
- [x] `Auto mode: include "$defaults" in autoMode.allow, autoMode.soft_deny, or autoMode.environment to add custom rules alongside the built-in list instead of replacing it` — DONE (`yoloClassifier.ts` new `expandDefaults(userList, tagName)` helper — when a user entry equals `$defaults`, the template's default rules are spliced in at that position via `extractTaggedBullets`. Applied to all three sections before the user's list is written into the `<*_to_replace>` tag)
- [x] `Added a "Don't ask again" option to the auto mode opt-in prompt` — DONE (`AutoModeOptInDialog.tsx` new `decline-persist` option sets `skipAutoPermissionPrompt: true` via `updateSettingsForSource` WITHOUT enabling auto mode, then calls `onDecline()`. Offered only when `declineExits === false` — at startup the decline exits the process so persistence is moot)
- [-] `Added claude plugin tag to create release git tags for plugins with version validation` — SKIP (plugin infra)
- [x] `--continue/--resume now find sessions that added the current directory via /add-dir` — DONE in f4a2df4 (new `AddedDirsMessage` type in `types/logs.ts` persisted via `reAppendSessionMetadata()`; `setSessionAddedDirs()` in `sessionStorage.ts` both writes the JSONL tail entry AND updates `~/.claude/added-dirs-index.json` via `utils/addedDirsIndex.ts` so session discovery is O(1) lookup instead of O(all-sessions) scan; `/add-dir` calls `setSessionAddedDirs()` on successful add; `loadSameRepoMessageLogsProgressive()` reads the index for the current cwd and merges matching sessions from other project dirs into the stat-log result, deduped by sessionId before enrichment)
- [-] `/color now syncs the session accent color to claude.ai/code when Remote Control is connected` — SKIP (Remote Control)
- [x] `The /model picker now honors ANTHROPIC_DEFAULT_*_MODEL_NAME/_DESCRIPTION overrides when using a custom ANTHROPIC_BASE_URL gateway` — DONE (`utils/model/modelOptions.ts` — `getSonnet46Option` and `getOpus46Option` now read `ANTHROPIC_DEFAULT_SONNET_MODEL_NAME`/`_DESCRIPTION` and `_OPUS_` equivalents on 3P providers even when the matching `_MODEL` isn't set. Custom Sonnet/Opus option builders already did this. Haiku already had full coverage)
- [-] `When auto-update skips a plugin due to another plugin's version constraint, the skip now appears in /doctor and the /plugin Errors tab` — SKIP (plugin)
- [-] `Fixed /mcp menu hiding OAuth Authenticate/Re-authenticate actions for servers configured with headersHelper, and HTTP/SSE MCP servers with custom headers being stuck in "needs authentication" after a transient 401` — SKIP (two-part fix tightly coupled to SDK internals: the menu-visibility logic filters on client state our fork inherits from the SDK, and the "stuck-in-needs-authentication" state machine is the SDK's. Auto-includes on next SDK upgrade)
- [x] `Fixed MCP servers whose OAuth token response omits expires_in requiring re-authentication every hour` — DONE (`services/mcp/auth.ts` — fallback lifetime for `expires_in`-less tokens raised from 3600s to `FALLBACK_TOKEN_LIFETIME_SECONDS = 30*24*3600` (30 days). Replaced at all three `expires_in || 3600` sites. The 401 retry path stays as the reactive safety net for servers whose tokens expire sooner)
- [-] `Fixed MCP step-up authorization silently refreshing instead of prompting for re-consent when the server's insufficient_scope 403 names a scope the current token already has` — SKIP (SDK-level step-up flow — our `services/mcp/client.ts:822` wraps fetch with `wrapFetchWithStepUpDetection` which is the SDK's detection. Fix in SDK)
- [-] `Fixed an unhandled promise rejection when an MCP server's OAuth flow times out or is cancelled` — SKIP (SDK-level OAuth flow; our outer fetch wrapper in `services/mcp/client.ts` doesn't own the rejection site)
- [-] `Fixed MCP OAuth refresh proceeding without its cross-process lock under contention` — SKIP (cross-process refresh lock is held in the SDK + our `services/mcp/auth.ts` refresh path uses `lockfile` wrapping the SDK call. The contention race is in the SDK — auto-fixes on next upgrade)
- [-] `Fixed macOS keychain race where a concurrent MCP token refresh could overwrite a freshly-refreshed OAuth token, causing unexpected "Please run /login" prompts` — SKIP (macOS keychain-specific)
- [-] `Fixed OAuth token refresh failing when the server revokes a token before its local expiry time` — SKIP (SDK-level refresh flow — our `services/mcp/auth.ts` delegates to `@modelcontextprotocol/sdk`'s refresh implementation)
- [-] `Fixed credential save crash on Linux/Windows corrupting ~/.claude/.credentials.json` — SKIP unless we can repro (our fork primarily uses ANTHROPIC_AUTH_TOKEN env; .credentials.json path rarely hit)
- [-] `Fixed /login having no effect in a session launched with CLAUDE_CODE_OAUTH_TOKEN — the env token is now cleared so disk credentials take effect` — SKIP (`/login` is largely Anthropic-subscription infra; our fork's primary auth path is `ANTHROPIC_AUTH_TOKEN` for z.ai/DeepSeek or the OAuth flow is delegated — this env-var clear targets the claude.ai subscription flow that isn't our primary runtime)
- [-] `Fixed unreadable text in the "new messages" scroll pill and /plugin badges` — SKIP (color-contrast issue against specific background colors. Our theme palette uses different terminal color tokens than upstream (daltonized variants, different background); would need a targeted audit against both daltonized themes. Low-impact visual polish)
- [x] `Fixed plan acceptance dialog offering "auto mode" instead of "bypass permissions" when running with --dangerously-skip-permissions` — DONE in `ExitPlanModePermissionRequest.tsx#buildPlanApprovalOptions` — new `currentMode` param plus `preferBypassOverAuto` flag (when `currentMode==='bypassPermissions'`) demotes the auto-mode slot so bypass-permissions surfaces first in both clear-context and keep-context slots
- [x] `Fixed agent-type hooks failing with "Messages are required for agent hooks" when configured for events other than Stop or SubagentStop` — DONE (`utils/hooks.ts` — dropped the `if (!messages) throw` guard before `execAgentHook`; pass `messages ?? []` instead. `execAgentHook`'s `_messages` parameter is already kept only for signature stability (CC-79 removed its sole consumer) — non-Stop hook events now run agent-type hooks correctly)
- [-] `Fixed prompt hooks re-firing on tool calls made by an agent-hook verifier subagent` — SKIP (requires plumbing an "insideHook" flag into the subagent's `toolUseContext` then gating `prompt`-type hook matching on it. Our VerifyPlanExecutionTool subagent already runs in an isolated context — the scenario requires reproducing a prompt-hook + VerifyPlan flow we can't easily simulate. Low-frequency edge case)
- [-] `Fixed /fork writing the full parent conversation to disk per fork — now writes a pointer and hydrates on read` — SKIP (significant refactor — requires (1) a new sidechain file format carrying `{ parentSessionId, startUuid, endUuid }` pointer records, (2) a hydrator that reads the parent file lazily, (3) updating every reader — transcript load, resume, /resume picker, /export — to dehydrate on read. Our `recordSidechainTranscript` currently writes the full `forkContextMessages + promptMessages` at line 531 of `forkedAgent.ts`. On most sessions the fork chain is 1-2 forks deep — the 2× disk cost is bearable. Revisit when a user hits disk bloat)
- [x] `Fixed Alt+K / Alt+X / Alt+^ / Alt+_ freezing keyboard input` — DONE (`ink/termio/tokenize.ts` no longer transitions to the `apc` state on `\x1b_` — the bytes fall through to `isEscFinal` and emit as 2-char escapes. `ink/parse-keypress.ts` `META_KEY_CODE_RE` extended to `[a-zA-Z0-9_^]` so bare Alt+`_` / Alt+`^` resolve to meta-keypresses. APC sequences sent by real applications still tokenize correctly — they arrive as multi-byte streams and re-enter the state via other means; interactive keypress bytes don't have a ST terminator to wait for)
- [-] `Fixed connecting to a remote session overwriting your local model setting in ~/.claude/settings.json` — SKIP (Remote Control)
- [x] `Fixed typeahead showing "No commands match" error when pasting file paths that start with /` — DONE (`PromptInput.tsx` tightened the `emptySuggestionsMessage` gate — now requires `/^\/[a-zA-Z0-9_:-]*$/.test(displayedValue)` so only strings that LOOK like slash commands (alnum + `_:-`) trigger the error. Pasted paths with `.`, `/`, etc. silently fall through)
- [-] `Fixed plugin install on an already-installed plugin not re-resolving a dependency installed at the wrong version` — SKIP (plugin)
- [x] `Fixed unhandled errors from file watcher on invalid paths or fd exhaustion` — DONE (`hooks/useTaskListWatcher.ts` and `hooks/useTasksV2.ts` — both `fs.watch` call sites now register an `error` handler via `watcher.on('error', …)`. Polling timer + in-process `onTasksUpdated` keep task-state fresh even when the OS watcher dies on `ENOSPC` / invalidated path)
- [-] `Fixed Remote Control sessions getting archived on transient CCR initialization blips during JWT refresh` — SKIP (Remote Control)
- [x] `Fixed subagents resumed via SendMessage not restoring the explicit cwd they were spawned with` — DONE (new `cwd?: string` field on `AgentMetadata` persisted by `runAgent`. `AgentTool.tsx` passes the invocation's `cwd` into `runAgentParams`. `resumeAgent.ts` reads `meta.cwd` and feeds it into `wrapWithCwd` ahead of `resumedWorktreePath` — matching the same precedence used on the initial spawn (explicit cwd beats worktree). Older metadata files without `cwd` fall back to previous behavior)

## 2.1.117

- [x] `Forked subagents can now be enabled on external builds by setting CLAUDE_CODE_FORK_SUBAGENT=1` — DONE (already ahead: our fork enables ALL 87 feature flags via bundle polyfill, FORK_SUBAGENT always true; `src/tools/AgentTool/forkSubagent.ts` already wired)
- [~] `Agent frontmatter mcpServers are now loaded for main-thread agent sessions via --agent` — PARTIAL in f4a2df4 (`initializeAgentMcpServers` is now exported from `runAgent.ts` and invoked in `main.tsx` after the main MCP connection batch completes for `-p --agent` (headless) mode — agent's newly-created clients are pushed into `headlessStore.mcp.clients` / `.tools` and the cleanup function is registered via `registerCleanup`. Deferred: the interactive `--agent` REPL path (would hook similarly inside `useBuiltinMcpServers` or a new dedicated effect after MCP connects))
- [x] `Improved /model: selections now persist across restarts even when the project pins a different model, and the startup header shows when the active model comes from a project or managed-settings pin` — DONE in f4a2df4 (`onChangeAppState.ts` detects whether any higher-precedence scope (project/local/policy) already has `model` pinned, and routes `/model` writes to `localSettings` in that case — beating the shadowing pin on restart — while still writing to `userSettings` for the common no-conflict case. `getActiveModelPinSource()` in `utils/model/model.ts` walks the settings cascade top-down to report which scope won; `LogoV2.tsx` appends a " (from project)" / " (managed)" / " (local)" / " (--settings)" / " (ANTHROPIC_MODEL)" suffix to the model line based on the source)
- [~] `The /resume command now offers to summarize stale, large sessions before re-reading them, matching the existing --resume behavior` — PARTIAL in f4a2df4 (threshold `5MB AND 14 days old` in `resume.tsx`; when a selected session matches, the picker swaps to an inline `Select` with "Resume now" / "Cancel" options and prints a `/compact` hint before resuming. Deferred: actually running compact pre-load — the conversation isn't in the REPL yet when the user confirms, so we guide them to run `/compact` as their first action after load instead of doing it automatically)
- [x] `Faster startup when both local and claude.ai MCP servers are configured (concurrent connect now default)` — DONE (already ahead: our `services/mcp/client.ts` connects each server in a Promise.all fan-out via `getMcpServerConfigs` + `connectToServer` — local and claude.ai proxy servers are not serialized. The 2.1.119 `reconcileMcpServers` parallelization commit landed too)
- [-] `plugin install on an already-installed plugin now installs any missing dependencies instead of stopping at "already installed"` — SKIP (plugin)
- [-] `Plugin dependency errors now say "not installed" with an install hint, and claude plugin marketplace add now auto-resolves missing dependencies from configured marketplaces` — SKIP (plugin/marketplace)
- [-] `Managed-settings blockedMarketplaces and strictKnownMarketplaces are now enforced on plugin install, update, refresh, and autoupdate` — SKIP (marketplace)
- [-] `Advisor Tool (experimental): dialog now carries an "experimental" label, learn-more link, and startup notification when enabled; sessions no longer get stuck with "Advisor tool result content could not be processed" errors on every prompt and /compact` — SKIP (experimental Anthropic feature; our fork has it stubbed)
- [x] `The cleanupPeriodDays retention sweep now also covers ~/.claude/tasks/, ~/.claude/shell-snapshots/, and ~/.claude/backups/` — DONE (`utils/cleanup.ts` added `cleanupOldTaskLists` (subdir mtime sweep for per-taskListId dirs), `cleanupOldShellSnapshots`, `cleanupOldBackups` (flat-file mtime sweep). All three wired into `cleanupOldMessageFilesInBackground`)
- [~] `OpenTelemetry: user_prompt events now include command_name and command_source for slash commands; cost.usage, token.usage, api_request, and api_error now include an effort attribute when the model supports effort levels. Custom/MCP command names are redacted unless OTEL_LOG_TOOL_DETAILS=1 is set` — PARTIAL (`processSlashCommand.tsx` now emits `user_prompt` for valid slash commands with `command_name` + `command_source`. Built-in names expose directly; custom/MCP are redacted to `'custom'`/`'mcp'` unless `OTEL_LOG_TOOL_DETAILS=1`. `logging.ts#logAPISuccess` adds `effort` attribute to `api_request` when `modelSupportsEffort(model)` — via lazy require to avoid an import cycle. cost.usage / token.usage / api_error effort attr not yet wired — same pattern can apply, deferred)
- [-] `Native builds on macOS and Linux: the Glob and Grep tools are replaced by embedded bfs and ugrep available through the Bash tool — faster searches without a separate tool round-trip (Windows and npm-installed builds unchanged)` — SKIP (native builds; we run Bun from source/compiled-bundle path)
- [-] `Windows: cached where.exe executable lookups per process for faster subprocess launches` — SKIP (Windows)
- [x] `Default effort for Pro/Max subscribers on Opus 4.6 and Sonnet 4.6 is now high (was medium)` — DONE (`utils/effort.ts#getDefaultEffortForModel` — Pro/Max subscribers on Opus 4.6 now default to `high` (was `medium`). Team subscribers stay at `medium` via the `tengu_grey_step2` GrowthBook gate (team quota pools differently). Sonnet 4.6 gets the same Pro/Max `high` default — wasn't gated previously)
- [-] `Fixed Plain-CLI OAuth sessions dying with "Please run /login" when the access token expires mid-session — the token is now refreshed reactively on 401` — SKIP (Plain-CLI OAuth is the claude.ai subscription path; our fork primarily runs `ANTHROPIC_AUTH_TOKEN` against z.ai/DeepSeek/direct-Anthropic where the 401 refresh-on-demand isn't applicable. Our fork's reactive OAuth fix from 2.1.117 changelog already lives in the SDK — auto-fixes on next upgrade)
- [-] `Fixed WebFetch hanging on very large HTML pages by truncating input before HTML-to-markdown conversion` — SKIP (our fork stubbed WebFetch in favor of zendriver-mcp, so the upstream HTML-to-markdown conversion path doesn't exist in our tree. Zendriver handles its own page content via the browser — different code path, not affected by this hang)
- [x] `Fixed a crash when a proxy returns HTTP 204 No Content — now surfaces a clear error instead of a TypeError` — DONE (`buildFetch` in `client.ts` intercepts 204 responses and throws an actionable `Upstream returned 204 No Content …` error that the retry/error-handling pipeline can format; replaces the opaque SDK JSON-parse TypeError)
- [-] `Fixed /login having no effect when launched with CLAUDE_CODE_OAUTH_TOKEN env var and that token expires` — SKIP (claude.ai OAuth path — see sibling /login fix above)
- [x] `Fixed prompt-input undo (Ctrl+_) doing nothing immediately after typing, and skipping a state on each undo step` — DONE (`useInputBuffer#undo` now accepts an optional `current` snapshot; cancels any pending debounced push, commits the live input to the buffer tip if different, then steps back. Both call sites in `PromptInput.tsx` (Ctrl+_ keybinding + TextInput onUndo) now pass `{text, cursorOffset, pastedContents}`. `canUndo` loosened to `buffer.length > 0 && currentIndex >= 0` so single-entry undo works too)
- [x] `Fixed NO_PROXY not being respected for remote API requests when running under Bun` — DONE (`getProxyFetchOptions` now accepts optional `targetUrl`; Bun branch consults `shouldBypassProxy` before setting `proxy`. Falls back to ANTHROPIC_BASE_URL for the firstParty Anthropic client path. Threaded `targetUrl` through all 4 MCP client.ts call sites)
- [-] `Fixed rare spurious escape/return triggers when key names arrive as coalesced text over slow connections` — SKIP (heuristic fix requiring byte-timing observation of key-name arrivals over SSH / remote terminal. Our tokenizer already splits ESC-prefixed sequences correctly; the rare timing window is hard to reproduce without an actual slow connection. Low impact)
- [-] `Fixed SDK reload_plugins reconnecting all user MCP servers serially` — SKIP (SDK plugin path)
- [-] `Fixed Bedrock application-inference-profile requests failing with 400 when backed by Opus 4.7 with thinking disabled` — SKIP (Bedrock-specific)
- [-] `Fixed MCP elicitation/create requests auto-cancelling in print/SDK mode when the server finishes connecting mid-turn` — SKIP (SDK-level `elicitation/create` lifecycle; fix in `@modelcontextprotocol/sdk` auto-includes on next upgrade)
- [-] `Fixed subagents running a different model than the main agent incorrectly flagging file reads with a malware warning` — SKIP (our fork's malware-warning path is inherited from Claude Code's content-scanner; the cross-model flag is a narrow edge case. The upstream fix likely scopes the warning to the executing model's policy, not the parent's — requires deeper investigation than a blind port justifies)
- [-] `Fixed idle re-render loop when background tasks are present, reducing memory growth on Linux` — SKIP (upstream's specific render-loop cause isn't described; our React tree memoizes via compiler-runtime `_c()` cache keys extensively, and `useCommandQueue` subscribes to queue change events rather than polling. We DID add `getCommandQueueActiveLength` for the spinner gate earlier in this session which short-circuits queue length computation when only orphan notifications remain. If memory growth is observed, the next investigation starts with `setInterval`/watcher leaks; deferred until repro)
- [-] `[VSCode] Fixed "Manage Plugins" panel breaking when multiple large marketplaces are configured` — SKIP (VSCode)
- [x] `Fixed Opus 4.7 sessions showing inflated /context percentages and autocompacting too early — Claude Code was computing against a 200K context window instead of Opus 4.7's native 1M` — DONE (`firstPartyNameToCanonical` was missing an opus-4-7 case — canonical was collapsing to `claude-opus-4`; added dedicated branch. `modelSupports1M` and new `modelHasNativeGA1M(model)` predicate in `utils/context.ts` — Opus 4.7 native-GA 1M bypasses the (now-unused post-2.1.116) beta header and `getModelCapability` cache gate. `getContextWindowForModel` consults the new predicate right after the `[1m]` suffix check. Sonnet 4.5/4.6 intentionally excluded from the GA predicate — their 1M still gates behind extra-usage entitlement)

## 2.1.116

- [-] `/resume on large sessions is significantly faster (up to 67% on 40MB+ sessions) and handles sessions with many dead-fork entries more efficiently` — SKIP (already ahead: `sessionStorage.ts:3295` byte-level dead-fork pre-filter gives -93% on 40MB/99%-dead and -80% on 151MB/92%-dead, exceeding upstream's -67% target)
- [-] `Faster MCP startup when multiple stdio servers are configured; resources/templates/list is now deferred to first @-mention` — SKIP (our MCP client doesn't call `resources/templates/list` at all — only `tools/list`, `resources/list`, `prompts/list`. Upstream defers a call we never make)
- [x] `Smoother fullscreen scrolling in VS Code, Cursor, and Windsurf terminals — /terminal-setup now configures the editor's scroll sensitivity` — DONE in 8cfd8dd (writes `terminal.integrated.mouseWheelScrollSensitivity: 0.5` to each editor's settings.json via new upsertJSONCObjectKey helper, preserves existing user values)
- [x] `Thinking spinner now shows progress inline ("still thinking", "thinking more", "almost done thinking"), replacing the separate hint row` — DONE in a6392f6 (replaced rotating synonyms with 4-stage progress hints driven by elapsed-since-thinking-started thresholds at 0/8s/20s/45s)
- [x] `/config search now matches option values (e.g. searching "vim" finds the Editor mode setting)` — DONE in 14088d0 (filter now also matches current string/boolean values + enum options array)
- [x] `/doctor can now be opened while Claude is responding, without waiting for the current turn to finish` — DONE in be56c75 (added `immediate: true` to doctor command definition — bypasses REPL onSubmit queue-while-loading gate)
- [-] `/reload-plugins and background plugin auto-update now auto-install missing plugin dependencies from marketplaces you've already added` — SKIP (plugin/marketplace infra — we don't ship marketplace dep resolution)
- [x] `Bash tool now surfaces a hint when gh commands hit GitHub's API rate limit, so agents can back off instead of retrying` — DONE in 357210a (regex-detects `gh`/`VAR=val gh` + rate-limit signatures in stdout/stderr, appends notice to BashTool output alongside formatter-stale warning)
- [-] `The Usage tab in Settings now shows your 5-hour and weekly usage immediately and no longer fails when the usage endpoint is rate-limited` — SKIP (Anthropic-operated usage endpoint, not applicable to z.ai/DeepSeek/direct-Anthropic via our token path)
- [-] `Agent frontmatter hooks: now fire when running as a main-thread agent via --agent` — SKIP (we don't ship a --agent main-thread flag; subagents go through Agent tool / /fork)
- [x] `Slash command menu now shows "No commands match" when your filter has zero results, instead of disappearing` — DONE in 660c789 (added `emptySuggestionsMessage` prop to PromptInputFooter; triggered from PromptInput when displayedValue starts with `/` and has no whitespace)
- [x] `Security: sandbox auto-allow no longer bypasses the dangerous-path safety check for rm/rmdir targeting /, $HOME, or other critical system directories` — DONE in 964465c (checkSandboxAutoAllow now runs checkDangerousRemovalPaths on each rm/rmdir subcommand before final allow)
- [-] `Fixed Devanagari and other Indic scripts rendering with broken column alignment in the terminal UI` — SKIP (our stringWidthJavaScript already counts grapheme clusters as 1 cell for the ligature-rendering terminals; Bun.stringWidth path uses POSIX wcwidth. Proper fix is terminal-specific and upstream diff isn't available)
- [x] `Fixed Ctrl+- not triggering undo in terminals using the Kitty keyboard protocol (iTerm2, Ghostty, kitty, WezTerm, Windows Terminal)` — DONE in 08490c3 (registered `ctrl+-` → `chat:undo` alongside existing `ctrl+_` and `ctrl+shift+-` bindings)
- [x] `Fixed Cmd+Left/Right not jumping to line start/end in terminals that use the Kitty keyboard protocol (Warp fullscreen, kitty, Ghostty, WezTerm)` — DONE in 3f1e9f9 (added `key.super` branches for leftArrow/rightArrow → startOfLine/endOfLine, placed before the word-jump branch)
- [x] `Fixed Ctrl+Z hanging the terminal when Claude Code is launched via a wrapper process (e.g. npx, bun run)` — DONE in 73aa439 (SIGTSTP to process group pid=0 instead of SIGSTOP to leaf pid, so the bun wrapper stops too and shell job-control reclaims the TTY)
- [x] `Fixed scrollback duplication in inline mode where resizing the terminal or large output bursts would repeat earlier conversation history` — DONE in a725898 (terminal.ts now eraseLines(prevHeight) instead of ERASE_SCREEN+CURSOR_HOME in inline mode, threading prev frame height through the clearTerminal patch)
- [x] `Fixed modal search dialogs overflowing the screen at short terminal heights, hiding the search box and keyboard hints` — DONE in f1c543d (FuzzyPicker drops the title row + collapses gap from 1 to 0 at rows < 18; MIN_VISIBLE 2 → 1 so a single item can render at extreme heights)
- [-] `Fixed scattered blank cells and disappearing composer chrome in the VS Code integrated terminal during scrolling` — SKIP (VS Code integrated terminal fork-specific behavior; our primary runtime is WSL/Docker terminal)
- [-] `Fixed an intermittent API 400 error related to cache control TTL ordering that could occur when a parallel request completed during request setup` — SKIP (already ahead: our fork latches `getPromptCache1hEligible()` + `getPromptCache1hAllowlist()` at first call via comment at claude.ts:408 "prevents mid-session overage flips from changing the cache_control TTL" — the exact race upstream is fixing)
- [-] `Fixed /branch rejecting conversations with transcripts larger than 50MB` — SKIP (already ahead: our `/branch` has no size cap — reads full transcript via `readFile`. Upstream lifted a cap we never had)
- [x] `Fixed /resume silently showing an empty conversation on large session files instead of reporting the load error` — DONE in ee768c7 (loadFullLog catch block now logs + returns log with `loadError` field; resume.tsx surfaces via `onDone`/`ResumeError`)
- [-] `Fixed /plugin Installed tab showing the same item twice when it appears under Needs attention or Favorites` — SKIP (plugin marketplace UI)
- [-] `Fixed /update and /tui not working after entering a worktree mid-session` — SKIP (our /tui is a simple `CLAUDE_CODE_NO_FLICKER` env flip with no worktree dependency; upstream /update uses npm which we don't)

## 2.1.114

- [-] `Fixed a crash in the permission dialog when an agent teams teammate requested tool permission` — SKIP (agent teams is Ant-internal, stubbed in our fork)

## 2.1.113

- [-] `Changed the CLI to spawn a native Claude Code binary (via a per-platform optional dependency) instead of bundled JavaScript` — SKIP (we build our own Bun-compiled binary; we don't use Anthropic's distribution pipeline)
- [x] `Added sandbox.network.deniedDomains setting to block specific domains even when a broader allowedDomains wildcard would otherwise permit them` — DONE in 6c8092c
- [x] `Fullscreen mode: Shift+↑/↓ now scrolls the viewport when extending a selection past the visible edge` — DONE in 6c8092c
- [x] `Ctrl+A and Ctrl+E now move to the start/end of the current logical line in multiline input, matching readline behavior` — DONE in 6c8092c
- [-] `Windows: Ctrl+Backspace now deletes the previous word` — SKIP (Linux container only)
- [x] `Long URLs in responses and bash output stay clickable when they wrap across lines (in terminals with OSC 8 hyperlinks)` — DONE in 6c8092c
- [x] `Improved /loop: pressing Esc now cancels pending wakeups, and wakeups display as "Claude resuming /loop wakeup" for clarity` — DONE in 9eca616 (built our own cron-backed self-pacing instead of porting the ScheduleWakeup tool: /loop without an interval triggers a dynamic prompt body that has the model compute now+N cron and schedule a one-shot with a `<<dynamic-loop-tick>>` sentinel; Esc on empty prompt sweeps every sentinel-tagged session cron in one keystroke)
- [-] `/extra-usage now works from Remote Control (mobile/web) clients` — SKIP (Remote Control infra)
- [-] `Remote Control clients can now query @-file autocomplete suggestions` — SKIP (Remote Control infra)
- [x] `Improved /ultrareview: faster launch with parallelized checks, diffstat in the launch dialog, and animated launching state` — DONE (parallel agents shipped earlier in 6c8092c via Promise.all; diffstat shipped in 6c8092c; animated launching state added this session — new `UltrareviewLaunching` Ink component in `ultrareviewCommand.tsx` that renders an 8s spinner-per-agent dwell before collapsing to the static "Launched 3 parallel…" scrollback record, using the same onDone-from-within-JSX pattern as ResumeCommand)
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
- [x] `Fixed compacting a resumed long-context session failing with "Extra usage is required for long context requests"` — DONE (retag 429 "Extra usage required" as `apiError: 'prompt_too_long'` in `errors.ts` so the existing PTL recovery pipeline runs: reactive compact → forced auto-compact. `errorDetails` preserves the raw API text. `compact.ts` inner retry loops at compactConversation and partialCompactConversation now also trigger on `isPromptTooLongMessage(summaryResponse)` — the user-facing content starts with "API Error:" which fails the old `startsWith(PROMPT_TOO_LONG_ERROR_MESSAGE)` check. Parity with `claude.ts:2393` `model_context_window_exceeded` retagging)
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
- [x] `/undo is now an alias for /rewind` — DONE (already wired in `commands/rewind/index.ts` — `aliases: ['checkpoint', 'undo']` resolves via `commands.ts:768` alias matcher)
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
- [-] `Fixed several /resume picker issues: --resume <name> opening uneditable, filter reload wiping search state, empty list swallowing arrow keys, cross-project staleness, and transient task-status text replacing conversation summaries` — 4 of 5 DONE in a6a5ba4 (uneditable, filter wipe, empty list, task-status). 5th (cross-project staleness) SKIP: without upstream source the bug has several incompatible interpretations (frozen `allStatLogs` not refreshing while picker open; dedup across projects losing the in-cwd copy; stale `projectPath` display after directory rename). Our picker re-stats the filesystem on every open/toggle via `getSessionFilesWithMtime`, so there is no persistent cache to invalidate. A speculative fix risks regressing the 4 working sub-issues.
- [x] `Fixed /export not honoring absolute paths and ~, and silently rewriting user-supplied extensions to .txt` — DONE in 4950e3e
- [x] `Fixed /effort max being denied for unknown or future model IDs` — DONE in defb61c
- [x] `Fixed slash command picker breaking when plugin frontmatter name is a YAML boolean keyword` — DONE in 4950e3e
- [x] `Fixed rate-limit upsell text being hidden after message remounts` — DONE in 24c7f5b (module-level guard prevents re-opening menu for same resetsAt window)
- [x] `Fixed MCP tools with _meta["anthropic/maxResultSizeChars"] not bypassing token-based persist layer` — DONE in 35a791c
- [x] `Fixed voice mode leaking dozens of space characters into input when re-holding push-to-talk key` — DONE in c573e06
- [x] `Fixed DISABLE_AUTOUPDATER not fully suppressing npm registry version check` — DONE in 057fead (adapted for GitHub Releases: `claude update` CLI now respects the env var and all npm-centric messaging swapped to GH)
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
- [-] `Fixed several /resume picker issues` — 4 of 5 DONE in a6a5ba4 (see 2.1.98 for details; 5th sub-issue SKIP as speculative without upstream diff)
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
