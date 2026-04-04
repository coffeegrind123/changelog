# Changelog

## 04.04.2026

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
