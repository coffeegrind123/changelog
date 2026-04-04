# Changelog

## 04.04.2026 9371826

- Added auto-updater rewritten to use GitHub Releases instead of npm/GCS — no Node.js needed on target machine, downloads compiled binary directly
- Added `bootstrap.sh` installer — detects platform, downloads latest release from GitHub, installs to `/usr/local/bin` or `~/.local/bin`
- Added GitHub Actions build workflow — compiles binaries for linux-x64, linux-arm64, darwin-x64, darwin-arm64 on tag push
- Added startup notification when MCP server dependencies are missing (Chrome for browser, maven for Ghidra)
- Added full auto-install chain for Ghidra MCP — downloads JDK 21, Ghidra 12.0.3, builds GhidraMCP jar, installs bridge scripts (~800MB first run, idempotent)
- Added smart dependency detection for browser and Ghidra MCP — checks for Chrome/JDK/Ghidra before attempting install, skips gracefully on systems without deps
- Added Ghidra MCP as built-in server + bundled `/ghidra-re` skill — auto-installs from coffeegrind123/ghidra-in-claude-code, auto-connects on startup, pre-approves all 193 tools
- Added zendriver-mcp browser as built-in MCP + bundled `/browser-automation` skill — auto-installs from coffeegrind123/Zendriver-MCP-fork, auto-connects, pre-approves all 48 tools
- Added auto-install and auto-update for zendriver-mcp — git clone on first run, background git pull on subsequent runs
- Disabled all built-in browser/web tools (WebFetchTool, WebSearchTool, WebBrowserTool, Claude in Chrome, Computer Use) — replaced by external MCP server as sole browser automation provider
- Added `--super` CLI flag and `/super` slash command for fully autonomous mode — activates proactive tick loop, bypasses all permissions, sets high effort, force-enables all GrowthBook-gated features (verification agent, memory extraction, computer use, auto-approve, swarms, ultrathink)
- Added `/proactive [on|off]` slash command — toggle autonomous proactive mode mid-session
- Added `/assistant [on|off]` slash command — toggle persistent KAIROS assistant mode
- Added `/coordinator [on|off]` slash command — toggle multi-agent coordinator mode (alias: `/agent-teams`)
- Added `/dump-prompt` slash command — display full system prompt mid-session (alias: `/system-prompt`)
- Added `MODIFICATIONS.md` documenting all fork changes with three-tier feature markers (public/hidden/fork-only)

## 04.04.2026 394f06f

- Removed `CYBER_RISK_INSTRUCTION` system prompt injection — Claude no longer refuses security-related requests
- Disabled domain blocklist check (`api.anthropic.com/api/web/domain_info`) — WebFetch works on any URL
- Disabled metrics opt-out status check (`api.anthropic.com/api/claude_code/organizations/metrics_enabled`)
- Disabled MCP registry prefetch (`api.anthropic.com/mcp-registry/v0/servers`)
- Disabled SSRF guard — HTTP hooks can reach any IP including private networks
- Set `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` at entrypoint by default
- Set `USER_TYPE=ant` at entrypoint — unlocks all ant-only tools, skills, commands, models, and debug features
- Replaced `bun:bundle` imports across 194 files with runtime feature module — all 87 feature flags enabled via Set lookup
- Enabled all feature flags: KAIROS, PROACTIVE, TRANSCRIPT_CLASSIFIER, COORDINATOR_MODE, VOICE_MODE, WEB_BROWSER_TOOL, CHICAGO_MCP, AGENT_TRIGGERS, FORK_SUBAGENT, ULTRAPLAN, TOKEN_BUDGET, and 76 more

## 03.04.2026 7357ffb

- Neutralized all product telemetry — 10 files replaced with no-op stubs preserving 1,019 call sites
- Disabled 1st-party event logging, Datadog, BigQuery metrics, OpenTelemetry, session tracing, analytics sinks
- Disabled GrowthBook feature flag service (cascading: all remote gates return defaults, no network calls)
- Disabled remote killswitches for bypass mode and auto mode
- Disabled version enforcement and auto-update caps

## 03.04.2026 ce7532e

- Eliminated 12 npm dependencies with inline vendor modules in `src/vendor/`
- Added `DEPENDENCY-AUDIT.md` with security analysis of all 55 remaining dependencies
- Identified and documented unmaintained packages and past CVEs

## 31.03.2026 15fb6a5

- Initial buildable research fork of Claude Code source
- TypeScript project setup with bun runtime
- All source files reconstructed and compilable
