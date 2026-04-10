# Upstream Backlog

Upstream features from anthropics/claude-code not yet implemented in OpenClaude.
Source: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md

Only entries after v2.1.87 (our fork base). Refresh by fetching:
`curl -fsSL https://raw.githubusercontent.com/anthropics/claude-code/refs/heads/main/CHANGELOG.md`

## 2.1.101

- [-] `Added /team-onboarding command to generate a teammate ramp-up guide` — SKIP (Anthropic managed infra, requires cloud onboarding flow)
- [-] `Added OS CA certificate store trust by default (CLAUDE_CODE_CERT_STORE=bundled)` — SKIP (enterprise TLS proxy feature)
- [-] `/ultraplan auto-create default cloud environment` — SKIP (Anthropic cloud infra)
- [ ] `Improved brief mode to retry once when Claude responds with plain text instead of structured message` — TODO
- [ ] `Improved focus mode: Claude writes more self-contained summaries knowing user only sees final message` — TODO
- [ ] `Improved tool-not-available errors to explain why and how to proceed` — TODO
- [ ] `Improved rate-limit retry messages to show which limit was hit and when it resets` — TODO
- [ ] `Improved refusal error messages to include API-provided explanation` — TODO
- [ ] `Improved claude -p --resume <name> to accept session titles from /rename or --name` — TODO
- [ ] `Improved settings resilience: unrecognized hook event name no longer causes entire settings.json to be ignored` — TODO
- [ ] `Improved plugin hooks from force-enabled plugins to run when allowManagedHooksOnly is set` — TODO
- [ ] `Improved /plugin and claude plugin update to warn when marketplace could not be refreshed` — TODO
- [-] `Improved plan mode to hide Refine with Ultraplan when org can't reach web` — SKIP (Anthropic cloud)
- [-] `Improved beta tracing to honor OTEL_LOG_USER_PROMPTS/TOOL_DETAILS/TOOL_CONTENT` — SKIP (OTEL infra)
- [-] `Improved SDK query() cleanup on break/await using` — SKIP (SDK internals)
- [ ] `Fixed command injection vulnerability in POSIX which fallback for LSP binary detection` — TODO (security fix)
- [ ] `Fixed memory leak where long sessions retained historical copies of message list in virtual scroller` — TODO
- [ ] `Fixed --resume/--continue losing context on large sessions when loader anchored on dead-end branch` — TODO
- [ ] `Fixed --resume chain recovery bridging into unrelated subagent conversation` — TODO
- [ ] `Fixed crash on --resume when persisted Edit/Write tool result missing file_path` — TODO
- [ ] `Fixed hardcoded 5-minute request timeout ignoring API_TIMEOUT_MS` — TODO
- [ ] `Fixed permissions.deny rules not overriding PreToolUse hook permissionDecision:ask` — TODO
- [ ] `Fixed --setting-sources without user causing cleanup to ignore cleanupPeriodDays` — TODO
- [-] `Fixed Bedrock SigV4 authentication failing with Authorization header` — SKIP (Bedrock-specific)
- [ ] `Fixed claude -w <name> failing with "already exists" after stale worktree cleanup` — TODO
- [ ] `Fixed subagents not inheriting MCP tools from dynamically-injected servers` — TODO
- [ ] `Fixed sub-agents in worktrees denied Read/Edit access to files inside their own worktree` — TODO
- [-] `Fixed sandboxed Bash commands failing with mktemp after fresh boot` — SKIP (sandbox infra)
- [-] `Fixed claude mcp serve tool calls failing with outputSchema validation` — SKIP (MCP serve)
- [ ] `Fixed RemoteTrigger tool run action sending empty body` — TODO
- [ ] `Fixed several /resume picker issues: narrow default view, unreachable preview, incorrect cwd in worktrees, session-not-found stderr, terminal title, resume hint overlap` — TODO
- [ ] `Fixed Grep tool ENOENT when embedded ripgrep binary path stale; falls back to system rg` — TODO
- [ ] `Fixed /btw writing entire conversation to disk on every use` — TODO
- [ ] `Fixed /context Free space and Messages breakdown disagreeing with header percentage` — TODO
- [ ] `Fixed several plugin issues: duplicate name frontmatter, ENAMETOOLONG, stale version cache, context:fork/agent frontmatter` — TODO
- [ ] `Fixed /mcp menu offering OAuth actions for headersHelper servers` — TODO
- [ ] `Fixed ctrl+], ctrl+\, ctrl+^ keybindings not firing in terminals sending raw C0 control bytes` — TODO
- [ ] `Fixed /login OAuth URL rendering with padding preventing clean mouse selection` — TODO
- [ ] `Fixed rendering issues: flicker in non-fullscreen, scrollback wiped during long sessions, mouse-scroll escapes leaking into prompt` — TODO
- [ ] `Fixed crash when settings.json env values are numbers instead of strings` — TODO
- [ ] `Fixed in-app settings writes not refreshing in-memory snapshot` — TODO
- [-] `Fixed custom keybindings not loading on Bedrock/Vertex/third-party providers` — SKIP (provider-specific)
- [ ] `Fixed claude --continue -p not correctly continuing -p/SDK sessions` — TODO
- [-] `Fixed several Remote Control issues` — SKIP (Remote Control infra)
- [-] `Fixed /insights sometimes omitting report file link` — SKIP (insights feature)
- [-] `[VSCode] Fixed file attachment not clearing when last editor tab closed` — SKIP (VSCode extension)

## 2.1.98

- [-] `Added interactive Google Vertex AI setup wizard from login screen` — SKIP (Anthropic cloud infra)
- [x] `Added CLAUDE_CODE_PERFORCE_MODE env var: Edit/Write/NotebookEdit fail on read-only files with p4 edit hint` — DONE in 35a791c
- [ ] `Added Monitor tool for streaming events from background scripts` — TODO (MONITOR_TOOL flag stub exists)
- [-] `Added subprocess sandboxing with PID namespace isolation on Linux (CLAUDE_CODE_SUBPROCESS_ENV_SCRUB, CLAUDE_CODE_SCRIPT_CAPS)` — SKIP (sandbox infra)
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
- [ ] `Improved /agents with tabbed layout: Running tab shows live subagents, Library tab adds Run agent and View running instance actions` — TODO
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

- [ ] `Added focus view toggle (Ctrl+O) in NO_FLICKER mode showing prompt, one-line tool summary with edit diffstats, and final response` — TODO
- [x] `Added refreshInterval status line setting to re-run status line command every N seconds` — DONE in 4950e3e
- [x] `Added workspace.git_worktree to status line JSON input when inside linked git worktree` — DONE in 4950e3e (also in 2.1.98)
- [x] `Added ● N running indicator in /agents next to agent types with live subagent instances` — DONE in 7b8eef4
- [x] `Added syntax highlighting for Cedar policy files (.cedar, .cedarpolicy)` — DONE in defb61c
- [x] `Fixed --dangerously-skip-permissions being silently downgraded to accept-edits after approving write to protected path` — DONE in 33c3cd1 (also in 2.1.98)
- [~] `Fixed and hardened Bash tool permissions, tightening checks around env-var prefixes and network redirects` — PARTIAL (env-var prefix fix done, network redirects already in defb61c)
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
