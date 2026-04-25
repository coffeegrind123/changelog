---
name: Three-way fork parity audit (CCB / Gitlawb / openclaude)
description: Feature-level comparison of three reverse-engineered Claude Code forks, with prioritized backport backlog
type: audit
---

# Three-Way Fork Parity Audit

> Date: 2026-04-24
> Sources:
> - **CCB** — `https://github.com/claude-code-best/claude-code` docs cloned to `/tmp/ccb-docs` (76 `.md`/`.mdx`, source private)
> - **Gitlawb** — `https://github.com/Gitlawb/openclaude` v0.6.0 cloned to `/tmp/gitlawb-oc` (2161 TS files, source-based)
> - **openclaude (ours)** — `/home/claudeuser/openclaude/src` (2356 TS files)
> Method: see `coffeegrind123/openclaude:context/fork-parity-audit-protocol.md`

Supersedes `ccb-parity-audit.md`, `ccb-audit-protocol.md`, `gitlawb-parity-audit.md` (deleted).

## Philosophy contrast

- **CCB** — docs-first reverse-engineering fork. Publishes a whitepaper-style catalogue of 44 shipped features + internal planning docs. Source private. Emphasizes agentic depth (KAIROS, Bridge Mode, Coordinator/Teammate, Computer Use) with Anthropic-first auth.
- **Gitlawb** — multi-provider open-source fork (`@gitlawb/openclaude` on npm, Node ≥20, Android/Termux support). Marquee focus: any LLM (OpenAI/Gemini/GitHub Models/Codex/Ollama/Atomic Chat/DashScope/MiniMax/NIM/Bedrock/Vertex/Foundry), `.openclaude-profile.json` saved profiles, `/provider` wizard, gRPC headless server, bundled VS Code extension, DuckDuckGo + Firecrawl WebSearch.
- **openclaude (ours)** — developer-agent depth fork, Bun-compiled binary via GitHub Releases. Marquee focus: distill + code knowledge graph + ACP (Zed/Cursor) + SSH Remote + LAN/UDS pipes + fuelgauge + OTel observe + Ghidra MCP + zendriver + Emacs integration + z.ai RPM throttling + NVIDIA NIM auto-catalog + reactive compact/PTL recovery.

All three ship: Buddy companion, Bridge/remote control, Coordinator Mode, Swarm/Teammate, Auto-Dream, LSP, NVIDIA NIM (different impls), Context Collapse, MicroCompact, Voice Mode, Workflows, Tree-sitter Bash AST, Token Budget, MCP Skills, Ultra Plan, Fork Subagent, extract-memories.

## Methodology note

Two `Explore` subagents produced exhaustive feature inventories in parallel (CCB = 44 features + 8 design docs from 76 `.md`/`.mdx`; Gitlawb = 96 commands + 45 tools + 24 services + 31 util subdirs from 2161 TS files). Every MISSING/PARTIAL claim below was cross-verified by `ls` / `command find` against `/tmp/<fork>/src` or `docs/`. The first pass had ~20 false negatives in the slash-command area (we ship `teleport`/`rewind`/`thinkback`/`passes`/`insights`/`issue`/`pr_comments`/`sandbox-toggle`/`rate-limit-options`/`reload-plugins`/`mobile`/`privacy-settings`/`perf-issue`/`remote-env`/`remote-setup`/`rename`/`reset-limits`/`share`/`summary`/`stats`); those got corrected by enumerating our actual `src/commands/` directory.

Status key: **✅ HAVE** · **⚠️ PARTIAL** (stub, thin, or materially different) · **❌ MISSING** · **— N/A** (intentionally out of scope).

---

## 1. Provider / Auth / Model routing

| Feature | CCB | Gitlawb | openclaude | Location / Notes |
|---|---|---|---|---|
| Env-var provider setup (`ANTHROPIC_BASE_URL`) | ✅ | ✅ | ✅ | Universal baseline. |
| `/provider` wizard (in-session) | ⚠️ | ✅ | ❌ | CCB: `commands/provider.ts` is a thin env-var toggler (`CLAUDE_CODE_USE_<BEDROCK|VERTEX|FOUNDRY|GEMINI|GROK>`). Gitlawb: `commands/provider/provider.tsx` full wizard + saved profiles. Ours: startup picker only. |
| `.openclaude-profile.json` saved profiles | ❌ | ✅ | ❌ | `utils/providerProfile.ts` + `providerStartupOverrides.ts`. |
| Provider auto-detect (zero-config) | ❌ | ✅ | ❌ | `utils/providerAutoDetect.ts` (#784). |
| Provider benchmark-backed recommendation | ❌ | ✅ | ❌ | `utils/providerRecommendation.ts` — goal-based (`--goal coding/balanced/latency`). |
| Provider discovery | ❌ | ✅ | ❌ | `utils/providerDiscovery.ts`. |
| Provider fail-fast validation at startup | ❌ | ✅ | ⚠️ | Ours errors at API-call time. |
| Provider secrets in settings.json | ❌ | ✅ | ❌ | `utils/providerSecrets.ts`. |
| API-key masking in UI | ❌ | ✅ | ❌ | #772. |
| Per-agent model routing (`agentRouting` / `agentModels`) | ⚠️ | ✅ | ⚠️ | `services/api/agentRouting.ts` (Gitlawb). CCB has sub-agent model hints. Ours has `model: small` flag, no settings router. |
| OpenAI-compatible endpoint | ✅ | ✅ | ✅ | All three via various paths. |
| Anthropic direct | ✅ | ✅ | ✅ | — |
| AWS Bedrock | ✅ | ✅ | ✅ | All three ship `@anthropic-ai/bedrock-sdk`. |
| Google Vertex | ✅ | ✅ | ✅ | `vertex-sdk`. |
| Azure Foundry | ✅ | ✅ | ✅ | `foundry-sdk`. |
| z.ai proxy | ❌ | ⚠️ | ✅ | We have zero-config RPM throttling + subscription-list auto-discovery. Gitlawb supports as generic OpenAI endpoint. |
| z.ai RPM sliding-window rate limiter | ❌ | ❌ | ✅ | `services/api/zaiRpmConfig.ts` + `zaiRateLimiter.ts` (our unique). |
| DeepSeek | ⚠️ | ✅ | ✅ | All support via OpenAI endpoint; we have auto low-context mode; Gitlawb has `thought_signature` fix. |
| Gemini native | ✅ | ✅ | ❌ | CCB: `src/services/api/gemini/` (client + index). Gitlawb: `utils/geminiAuth.ts` + `geminiCredentials.ts` with `thought_signature` fix (#404). |
| Grok (xAI) native | ✅ | ❌ | ❌ | CCB only: `src/services/api/grok/` (client + index + tests). |
| Foundry (Azure) native | ✅ | ✅ | ✅ | CCB: `CLAUDE_CODE_USE_FOUNDRY` provider toggle. Gitlawb + ours: `@anthropic-ai/foundry-sdk`. |
| GitHub Models onboarding | ❌ | ✅ | ❌ | `/onboard-github` + `utils/githubModelsCredentials.ts` (#351, #579). |
| GitHub Copilot native Anthropic mode | ❌ | ✅ | ❌ | Claude models via Copilot subscription (#579). |
| Codex OAuth (ChatGPT sign-in) | ❌ | ✅ | ❌ | `services/api/codexOAuth.ts` + `codexShim.ts` + `utils/codexCredentials.ts`. |
| Codex CLI credential reuse | ❌ | ✅ | ❌ | Reads `~/.codex/auth.json`. |
| Ollama `ollama launch openclaude` shim | ❌ | ✅ | ❌ | Zero-config local Ollama boot. |
| Ollama via env vars | ⚠️ | ✅ | ✅ | Ours via `OPENAI_BASE_URL`. |
| Atomic Chat provider | ❌ | ✅ | ❌ | `/provider` picker + autodetect (#810). |
| Alibaba DashScope | ❌ | ✅ | ❌ | #509. |
| MiniMax | ❌ | ✅ | ❌ | `utils/model/minimaxModels.ts` (#552). |
| NVIDIA NIM | ❌ | ✅ | ✅ (++) | Both. Ours has auto-generated 130-entry catalog (`openaiBridge/providers/nimModelCatalog.ts`); Gitlawb's `utils/model/nvidiaNimModels.ts` is handcrafted. |
| 1M context access check | ❌ | ✅ | ⚠️ | `utils/model/check1mAccess.ts` (Gitlawb). Ours does per-model lookup but no entitlement probe. |
| Model cache + benchmarking | ❌ | ✅ | ❌ | `utils/model/modelCache.ts` + `benchmark.ts` (#671). |
| Smart model routing (cheap/hard) | ❌ | ✅ | ❌ | `services/api/smartModelRouting.ts` (#785). |
| Model allowlist | ⚠️ | ✅ | ✅ | — |
| Model-capabilities deprecation layer | ⚠️ | ✅ | ⚠️ | `utils/model/deprecation.ts` (Gitlawb). |
| Multi-provider secure storage | ⚠️ | ✅ | ⚠️ | `utils/secureStorage/` (Gitlawb, 8 files). Ours uses OS keychains ad-hoc. |
| OAuth via Claude.ai (bridge/KAIROS) | ✅ | ⚠️ | ✅ | CCB for Bridge/KAIROS; ours preserved from upstream; Gitlawb has `oauth/` but not first-class. |
| Referral tracking | — | ✅ | ✅ | — |

---

## 2. Agents / Coordinator / Swarm / Teammate

| Feature | CCB | Gitlawb | openclaude | Location / Notes |
|---|---|---|---|---|
| Sub-agent (`Agent` tool) | ✅ | ✅ | ✅ | Stock. |
| Fork Subagent (context inheritance + shared cache) | ✅ | ✅ | ✅ | `src/tools/AgentTool/forkSubagent.ts` + `/fork` (ours). |
| Coordinator Mode (star topology) | ✅ | ✅ | ✅ | `src/coordinator/coordinatorMode.ts` 369-line parity. Our `workerAgent.ts` was a 1-line stub that threw at runtime on first worker spawn; fixed 2026-04-24 with a hybrid shape — reuse `GENERAL_PURPOSE_AGENT` (Gitlawb-style base) + filter `INTERNAL_ORCHESTRATION_TOOLS` (`TEAM_CREATE`/`TEAM_DELETE`/`SEND_MESSAGE`/`SYNTHETIC_OUTPUT`) out of `ASYNC_AGENT_ALLOWED_TOOLS` (CCB-style curation). Returns `[WORKER, GENERAL, EXPLORE, PLAN]`. See `coffeegrind123/openclaude:context/agents-coordinator-swarm-deepdive.md` §3 P0. |
| Swarm / Agent Teams (mesh + mailbox) | ✅ | ✅ | ✅ | **Corrected.** All three ship the full 14-file swarm dir (~4571 lines, byte-identical on most files). CCB-specific: `leaderPermissionMode` inherit in `spawnInProcess.ts` (+41 lines). Gitlawb-specific: 27 lines of deprecation JSDoc on file-based permission funcs (our callers already on mailbox). See deep-dive §4. |
| Teammate mailbox | ✅ | ✅ | ✅ | **Corrected.** `utils/teammateMailbox.ts` byte-identical (1183–1187 lines; 4-line trivial diff on CCB). `teammate.ts` / `teammateContext.ts` / `collapseTeammateShutdowns.ts` / `inProcessTeammateHelpers.ts` identical. |
| Worktree isolation (git worktree per agent) | ✅ | ✅ | ✅ (++) | `utils/worktree.ts` (CCB 1516, Gitlawb 1563, ours 1573 after 2026-04-24 adapts). Ported from Gitlawb: `withGitWorktreeMutationLock(repoRoot, fn)` per-repo promise-chained mutex (prevents `git worktree add` races when `/super` / `/coordinator` fans out), wrapped with double-checked locking inside `getOrCreateWorktree` + extracted inner body into `doCreateWorktreeLocked`. Also wrapped `removeAgentWorktree` in the same lock. Graceful non-git fallback added to `AgentTool.tsx:592` — try/catch re-throws only on explicit `isolation: 'worktree'`, otherwise logs + falls back to cwd. See deep-dive §6 + Tier 1 adapts 2–3. |
| VerifyPlanExecution | ⚠️ | ❌ | ✅ | **Corrected.** CCB ships a 93-line **self-report** tool (agent claims `{plan_summary, verification_notes, all_steps_completed}`, tool echoes back — no actual diff inspection). Gitlawb ships a 3-line stub (`export default null`). Ours ships a 223-line **active** verifier that `runForkedAgent()`-spawns a background agent to read the plan, run `git diff`, check each item, emit PASS/PARTIAL/FAIL/EXTRA. See deep-dive §7. |
| Forked agent helper | — | ✅ | ✅ | `utils/forkedAgent.ts`. |
| Standalone agent | — | ✅ | ✅ | `utils/standaloneAgent.ts`. |
| `/super` orchestrator with swarmNudge | ❌ | ❌ | ✅ | Our unique. `commands/super.ts` + `proactive/swarmNudge.ts`. |
| `/coordinator on/off` | ✅ | ✅ | ✅ | — |

---

## 3. Assistant / Proactive / KAIROS

| Feature | CCB | Gitlawb | openclaude | Location / Notes |
|---|---|---|---|---|
| Assistant mode (persistent) | ✅ | ⚠️ | ✅ | CCB: KAIROS (autonomy/CCR/swarm-team-bound — `initializeAssistantTeam` real impl, `discoverAssistantSessions`, JSX panel, `NewInstallWizard` for daemon setup). Gitlawb: `src/assistant/AssistantSessionChooser.tsx` (10-line session-chooser stub). Ours: local-only KAIROS by design — `/assistant on` persists `assistantMode` setting + activates proactive + autoDream + daily logs. CCB-only sub-features deliberately excluded per kickoff (autonomy/RCS infrastructure we don't run). See `coffeegrind123/openclaude:context/assistant-proactive-kairos-deepdive.md`. |
| Proactive tick loop | ✅ | ⚠️ | ✅ (++) | CCB: wall-clock 30s timer + autonomy-module prompt builder + activation primer (`<system-reminder>` "do useful work or Sleep — don't say 'still waiting'"). Gitlawb: partial (`utils/agent*.ts` agent helpers, no `proactive/` directory). Ours: event-driven (turn-complete + Sleep-controlled cadence) + `swarmNudge.ts` (149-line `/super`-mode parallel-fanout enforcer, no equivalent in CCB) + coordinator-conflict guard in `/proactive on` + activation primer ported from CCB (after 2026-04-25 commit `7f3ff65`, with double-prime guards against `/super` overlap). See deep-dive. |
| Sleep tool | ✅ | ✅ | ✅ | All three: `SleepTool`. CCB: `packages/builtin-tools/src/tools/SleepTool/SleepTool.ts` (212L) + `prompt.ts` (17L). Ours: simpler 77-line impl gated on `CLAUDE_CODE_PROACTIVE=1`. |
| Push notifications | ✅ | ❌ | ✅ (++) | CCB: bridge-bound (axios POST to `/v1/sessions/{id}/events`, returns `sent: false` without a connected RCS bridge — functionally inert without Anthropic-hosted infrastructure). Ours: local terminal-escape delivery (iTerm2 `OSC 9` / Kitty `OSC 99` / Ghostty `OSC 777` / `\x07` bell fallback) + `executeNotificationHooks()` for user-defined hooks — independently functional with no infrastructure dependency. Different scope by design. |
| Daily dream logs | ✅ | ❌ | ✅ | KAIROS feature. CCB + ours both instruct model to append timestamped entries to today's `memdir/` log via the system-prompt addendum. Gitlawb skips (no KAIROS subsystem). |
| Auto-Dream consolidation | ✅ | ✅ | ✅ (++) | All three: `src/services/autoDream/` essentially byte-identical (autoDream.ts 323–326 lines, consolidationLock.ts 140 lines all three, consolidationPrompt.ts 65 lines all three). Ours' (++): autoDream **runs in KAIROS mode** (CCB + Gitlawb both `return false` if `getKairosActive()`) + **default-on** (ours short-circuits the `tengu_onyx_plover` GrowthBook check to `return true`). |
| `/dream` manual command | ✅ | ✅ | ✅ (skill, ++) | CCB: skill with `DREAM_PROMPT_PREFIX` preamble framing manual run. Gitlawb: command listing sessions touched since `lastConsolidatedAt` + "last run: Xh ago" timing context. Ours (after 2026-04-25 commit `7f3ff65`): skill with **both** — preamble *and* session-list (filters out current session). Superset of CCB and Gitlawb. |
| Away summary | ✅ | ✅ | ✅ (++) | All three: `services/awaySummary.ts` + `hooks/useAwaySummary.ts`. 5-min blur triggers 1–3 sentence recap via small-fast model. Ours = CCB's shape (idle fallback for `'unknown'` focus state — makes it work in Docker/CMD/PowerShell) + Gitlawb's simpler service (no Langfuse, no i18n) + our additions: `settings.awaySummaryEnabled`, `CLAUDE_CODE_ENABLE_AWAY_SUMMARY` env, `hasPendingInput` guard to skip mid-composition. |
| `/mobile` slash command (Anthropic-app QR code) | ✅ | ✅ | ✅ | All three forks ship `src/commands/mobile/mobile.tsx` showing a QR code linking to the Anthropic Claude mobile app on iOS App Store / Google Play. Aliases `/ios`, `/android`. **Not a push feature** — pure marketing surface for Anthropic's 1st-party app. Audit row was previously mislabelled "Mobile push (KAIROS feature set)" — corrected 2026-04-25. |
| SubscribePR tool | ✅ (stub) | ❌ | ✅ | CCB ships an 88-line stub at `packages/builtin-tools/src/tools/SubscribePRTool/SubscribePRTool.ts` whose `call()` returns `{ subscribed: false, error: 'requires the KAIROS GitHub webhook subsystem' }` unconditionally — tied to ant-internal webhook plumbing not in their public source. Gitlawb has no SubscribePR tool. Ours: 193-line working implementation (`gh` CLI polling + cron task creation + per-PR state file in `~/.claude/pr-subscriptions/`). Only fork with a working version. Cross-ref §8 row. |
| Session-resume across CLI restarts | ✅ | ✅ | ✅ | `src/assistant/sessionHistory.ts` byte-identical (87 lines) across all three forks. `tengu_session_resumed` logged at 8+ sites in our `main.tsx`. |

---

## 4. Remote Control / SSH / Bridge

| Feature | CCB | Gitlawb | openclaude | Location / Notes |
|---|---|---|---|---|
| Bridge Mode (WebSocket remote control) | ✅ | ✅ | ✅ | All three. CCB: v1+v2 with workSecret + trusted devices. Gitlawb: `src/bridge/` 25+ files. Ours: `src/bridge/` + `src/ccr-server/`. |
| Self-hosted RCS (React UI + JWT) | ✅ | ⚠️ | ⚠️ | CCB: full stack. `packages/remote-control-server/` = Hono backend + React 19 + Vite + Radix UI + Tailwind + Shiki + QR code auth. Ours: local CCR server, no UI. |
| BYOC environment runner | ⚠️ | ⚠️ | ✅ | CCB: `src/environment-runner/main.ts` is a 3-line `Promise.resolve()` stub (file-exists-but-inert). Gitlawb: directory deleted, routing in cli.tsx would crash. Ours: 342-line real impl. See `coffeegrind123/openclaude:context/remote-control-ssh-bridge-deepdive.md`. |
| Self-hosted runner (CCR v2) | ⚠️ | ⚠️ | ✅ | CCB: `src/self-hosted-runner/main.ts` is a 3-line `Promise.resolve()` stub. Gitlawb: directory deleted. Ours: 252-line real impl (CCR v2 worker). See deep-dive. |
| Direct-connect session manager | ✅ | ✅ | ✅ | All three ship the 3 real client files (`createDirectConnectSession.ts` + `directConnectManager.ts` + `types.ts`) byte-identical (~358 lines). CCB and ours also carry 7 placeholder server stubs that are inert. See deep-dive. |
| RemoteSessionManager + SessionsWebSocket | ✅ | ✅ | ✅ | All three ship `src/remote/` 4-file. Ours byte-identical to Gitlawb; CCB has minor drift on 2 files. Wired through `useRemoteSession` → REPL. See deep-dive. |
| Trusted-device tokens | ✅ | ✅ | ✅ | `bridge/trustedDevice.ts` byte-identical to CCB (210 lines), 5 non-test callers in bridge core + login/logout. See deep-dive. |
| Capacity-wake signal | ✅ | ✅ | ✅ | `bridge/capacityWake.ts` byte-identical (56 lines) across all three forks; wired in bridgeMain + replBridge. See deep-dive. |
| Long-poll task assignment | ✅ | ✅ | ✅ | `pollConfig.ts` (110) + `pollConfigDefaults.ts` (82) byte-identical; `bridgeMain.ts` has 20+ runtime references; `bridgeApi.ts#pollForWork` matches Gitlawb. See deep-dive. |
| SSE / WebSocket streaming session | ✅ | ✅ | ✅ | — |
| **SSH Remote (ssh user@host)** | ✅ | ⚠️ | ✅ | CCB: `src/ssh/` (5 files: `SSHAuthProxy.ts`, `SSHDeploy.ts`, `SSHProbe.ts`, `SSHSessionManager.ts`, `createSSHSession.ts`) — full impl confirmed at source. Gitlawb: `src/hooks/useSSHSession.ts` wiring only, no backend. Ours: 5-file backend ported from CCB. |
| `claude daemon start/stop/status/restart` (tmux) | ✅ | ⚠️ | ✅ | CCB shipped (incl. extra `state.ts` for CCR ack-replay); ours shipped (without state.ts). Gitlawb has routing only. |
| `--bg` daemon mode | ✅ | ⚠️ | ✅ | Gitlawb has routing + feature-flag references but no daemon module. |
| Debug mode (`-d, --debug` filter flag) | ✅ | ⚠️ | ⚠️ | CCB-only top-level commander option (`-d, --debug [filter]`) at `main.tsx:1361`. Both forks already detect `--inspect`/`--inspect-brk` for Bun-inspect mode (runtime introspection, not a feature). Ours has `--debug-to-stderr`/`--debug-file` + `process.argv.includes('--debug')` runtime check at `utils/debug.ts:49`. Gap is one commander-option registration. See deep-dive. |
| `/remote-env`, `/remote-setup` | ✅ | ✅ | ✅ | All three ship both. CCB: `commands/remote-env/{index.ts,remote-env.tsx}` + `commands/remote-setup/{api.ts,index.ts,remote-setup.tsx}`. |
| `/bridge-kick` | ✅ | ✅ | ✅ | Byte-identical 200-line file across all three forks (Ant-only debug command for injecting bridge failure states). |

---

## 5. Multi-instance / Pipes / LAN

| Feature | CCB | Gitlawb | openclaude | Location / Notes |
|---|---|---|---|---|
| Pipes (UDS / Named Pipe local IPC) | ✅ | ❌ | ✅ | CCB: UDS_INBOX. Ours: `utils/pipeTransport.ts` + `udsClient.ts` + `udsMessaging.ts`. Gitlawb: none. |
| LAN Pipes (TCP cross-machine) | ✅ | ❌ | ✅ | CCB: shipped. Ours: `utils/lanBeacon.ts` + UDP multicast 224.0.71.67:7101. |
| Main/sub role election | ✅ | ❌ | ✅ | — |
| Broadcast + unicast messaging | ✅ | ❌ | ✅ | — |
| `/pipes`, `/attach`, `/detach`, `/send`, `/claim-main`, `/pipe-status`, `/peers` | ✅ | ❌ | ✅ | Command set only in CCB + ours. |
| Shift+Down pipe selector toggle | ✅ | ❌ | ✅ | — |
| Pipe permission relay | ❌ | ❌ | ✅ | `utils/pipePermissionRelay.ts` — our unique. |
| UDS Inbox registry | ✅ | ❌ | ✅ | `utils/pipeRegistry.ts`. |
| Remote-control server (bridge) | ✅ | ⚠️ | ✅ | `commands/remoteControlServer/`. |

---

## 6. Integration / Headless / IDE

| Feature | CCB | Gitlawb | openclaude | Location / Notes |
|---|---|---|---|---|
| Stock Claude Code IDE integration | ✅ | ✅ | ✅ | Via MCP port + `~/.claude/ide/<port>.lock`. |
| VS Code extension (bundled) | ❌ | ✅ | ❌ | `vscode-extension/openclaude-vscode/` — 10 commands, control center, chat UI (#608). |
| Emacs integration (transient menu) | ❌ | ❌ | ✅ | `contrib/emacs/openclaude.el` (our unique). |
| ACP (Zed/Cursor stdio NDJSON) | ✅ | ❌ | ✅ | CCB shipped; we ported. `services/acp/` (7 files). |
| acp-link (WebSocket → stdio bridge) | ✅ | ❌ | ✅ | CCB shipped; we ported. `services/acpLink/`. |
| Headless gRPC server (bidir streaming) | ❌ | ✅ | ❌ | `src/grpc/server.ts` + `src/proto/openclaude.proto`. |
| gRPC test CLI client | ❌ | ✅ | ❌ | `scripts/grpc-cli.ts`. |
| Local CCR server (Anthropic CCR v1+v2) | ❌ | ⚠️ | ✅ | Ours: `src/ccr-server/` (~20 endpoints). |
| `claude submit` / `claude ccr-server` | ❌ | ❌ | ✅ | Our unique. |
| `claude environment-runner` (BYOC) | ⚠️ | ⚠️ | ✅ | CCB: 3-line `Promise.resolve()` stub. Gitlawb: directory deleted, routing in cli.tsx would crash. Ours: 342-line real impl. Mirrors §4 deep-dive verdict (commit `03e63e8`). |
| `claude self-hosted-runner` | ⚠️ | ⚠️ | ✅ | CCB: 3-line stub. Gitlawb: directory deleted. Ours: 252-line real impl (CCR v2 worker). Mirrors §4 deep-dive. |
| `claude acp-link` subcommand | ✅ | ❌ | ✅ | — |
| `claude ssh user@host` subcommand | ✅ | ❌ | ✅ | — |
| Deep linking (URL protocol handler) | ✅ | ✅ | ✅ (++) | All three forks ship the full 6-file `deepLink/{registerProtocol,terminalPreference,protocolHandler,terminalLauncher,banner,parseDeepLink}` shape (~1390 LOC) + 236-line `desktopDeepLink.ts`; ours/Gitlawb byte-identical on 4 of 6 files. Ours `parseDeepLink.ts` is a **superset** with the 2.1.91 multi-line-prompts backport. See `coffeegrind123/openclaude:context/integration-headless-ide-deepdive.md`. |

---

## 7. MCP servers + tool infrastructure

| Feature | CCB | Gitlawb | openclaude | Location / Notes |
|---|---|---|---|---|
| Stock MCP client + manager | ✅ | ✅ | ✅ | — |
| MCP auth + OAuth | ✅ | ✅ | ✅ | `services/mcp/auth.ts` + `oauth/`. |
| MCP skill URI (skill://) discovery | ✅ | ✅ | ✅ | All three. |
| MCP schema normalization (strict tools) | ⚠️ | ✅ | ✅ | Different architectures. Gitlawb: `OPENCLAUDE_DISABLE_STRICT_TOOLS` env opt-out at `openaiShim.ts:774`. Ours: `services/api/openaiBridge/` per-provider registry, `supportsStrictTools: false` default — env gate structurally unnecessary. CCB: `services/api/openai/` shim with no strict-tools handling. |
| MCP official registry | ✅ | ✅ | ✅ (stub) | `services/mcp/officialRegistry.ts`. Ours is an 11-LOC deliberate stub (telemetry no-op'd); CCB 72 / Gitlawb 78 LOC. |
| MCP doctor | ❌ | ✅ | ✅ | `services/mcp/doctor.ts` (695 LOC) ported from Gitlawb on 2026-04-25. CLI subcommand `claude mcp doctor [name] [--scope] [--config-only] [--json]`. CCB still has no doctor.ts. |
| MCP channel notifications (Slack/Discord/WeChat/Telegram/Feishu) | ✅ (+native WeChat) | ✅ | ✅ | All three: `channelNotification.ts` + `channelAllowlist.ts` + `channelPermissions.ts`. CCB additionally has dedicated `packages/weixin/` native package. |
| MCP elicitation handler | ✅ | ✅ | ✅ | `services/mcp/elicitationHandler.ts` — byte-identical 313 LOC across all three forks. |
| MCP `maxResultSizeChars` 500K override | ❌ | ❌ | ✅ | Backported from upstream 2.1.91 — **ours-only.** `MAX_RESULT_SIZE_CHARS_CEILING = 500_000` + `resolveMaxMcpOutputChars()` + `_meta['anthropic/maxResultSizeChars']` wiring at `services/mcp/client.ts:1888-1891`. CCB+Gitlawb have neither the constant nor the wiring. |
| MCP tool error: all content blocks | ❌ | ❌ | ✅ | Backported from upstream 2.1.89 — **ours-only.** `services/mcp/client.ts:3160-3190` joins text from all content blocks. CCB+Gitlawb both still use `result.content[0]` (pre-fix). |
| XAA IDP login | ✅ | ✅ | ✅ | `services/mcp/xaaIdpLogin.ts` — byte-identical 487 LOC across all three forks. |
| VS Code SDK MCP | ✅ | ✅ | ✅ | `services/mcp/vscodeSdkMcp.ts` — byte-identical 112 LOC across all three forks. SDK-side helper for IDE extension hosts running MCP servers (distinct from §5's bundled vscode-extension). |
| **Bundled MCP servers** | — | — | — | — |
| Chrome MCP (claude-in-chrome) | ✅ | ✅ | ⚠️ | CCB: `packages/@ant/claude-for-chrome-mcp/`. Gitlawb: `utils/claudeInChrome/`. Ours: 2337 LOC files present + tool-rendering wired, MCP server registration deliberately disabled (`zendriver-mcp` replaces it per CLAUDE.md). |
| Chrome extension (Claude Pro+) | ✅ | ❌ | ❌ | CCB-unique. |
| Zendriver browser MCP (auto-install) | ❌ | ❌ | ✅ | `utils/browserMcp/setup.ts` — our fork. |
| Computer Use (cross-platform) | ✅ | ✅ | ✅ (npx) | CCB: `packages/@ant/computer-use-mcp/` + `@ant/computer-use-input/` (per-OS NAPI dispatcher) + `@ant/computer-use-swift/` (screenshots). Gitlawb: full `utils/computerUse/` (15 files / 2161 LOC). Ours: same 15-file shim shape (2131 LOC); `setup.ts` runs `npx -y computer-use-mcp` to deliver domdomegg's upstream. |
| Computer Use Windows enhancements | ✅ | ⚠️ | ❌ | CCB: `PrintWindow`, UIA tree, Windows.Media.Ocr via `@ant/computer-use-swift/`. Tier-3 / NAPI-heavy port. |
| WeChat/Weixin channel | ✅ (+native package) | ✅ | ✅ | All three cover WeChat. CCB additionally ships dedicated `packages/weixin/` native transport. Gitlawb+ours route via generic `channelNotification.ts` (316 LOC, byte-identical). |
| Ghidra MCP (JDK + Ghidra + bridge auto-install) | ❌ | ❌ | ✅ | `utils/ghidraMcp/setup.ts` — our unique. |
| Computer Use MCP (domdomegg npx) | ❌ | ❌ | ✅ | `utils/computerUse/setup.ts` auto-install. |

---

## 8. Tools (model-facing)

> Source-level deep-dive at `coffeegrind123/openclaude:context/tools-model-facing-deepdive.md` (2026-04-25). 26 column flips + 5 row additions = 31 row-level changes — largest single-section correction count to date. Root cause: CCB ships its model-facing tools in `packages/builtin-tools/src/tools/`, not `src/tools/`; the audit was originally `ls`'ing only `src/tools/` so 18 CCB cells were false-negatives.

| Feature | CCB | Gitlawb | openclaude | Location / Notes |
|---|---|---|---|---|
| Stock tools (Bash/Read/Write/Edit/Glob/Grep/WebFetch/WebSearch/NotebookEdit) | ✅ | ✅ | ✅ | — |
| AgentTool + sub-agents | ✅ | ✅ | ✅ | — |
| Task tools (Create/Get/List/Output/Stop/Update) | ✅ | ✅ | ✅ | — |
| Todo tools + TodoWrite | ✅ | ✅ | ✅ | — |
| AskUserQuestion | ✅ | ✅ | ✅ | — |
| EnterPlanMode / ExitPlanMode | ✅ | ✅ | ✅ | — |
| EnterWorktree / ExitWorktree | ✅ | ✅ | ✅ | — |
| LSPTool | ✅ | ✅ | ✅ | — |
| SkillTool | ✅ | ✅ | ✅ | — |
| MCPTool + McpAuthTool | ✅ | ✅ | ✅ | — |
| ListMcpResourcesTool / ReadMcpResourceTool | ✅ | ✅ | ✅ | CCB at `packages/builtin-tools/src/tools/` (178+218 LOC). |
| MonitorTool (streaming shell output) | ✅ | ✅ | ✅ | — |
| SleepTool | ✅ | ✅ | ✅ | — |
| SendMessageTool | ✅ | ✅ | ✅ | CCB at `packages/builtin-tools/src/tools/SendMessageTool/` (1060 LOC). |
| RemoteTriggerTool | ✅ | ✅ | ✅ | CCB at `packages/builtin-tools/src/tools/RemoteTriggerTool/` (308 LOC). |
| ScheduleCronTool (Create/Delete/List) | ✅ | ✅ | ✅ | Identical 5-file `CronCreate/Delete/List + UI + prompt` layout across all three forks. CCB 552 LOC. |
| PowerShellTool | ✅ | ✅ | ✅ | CCB heavyweight (10124 LOC); Gitlawb 8972; ours 8954. |
| REPLTool | ✅ | ✅ | ✅ | CCB 174 LOC; ours 563 LOC (heavily extended; needs both `description()` AND `prompt()`). |
| BriefTool | ✅ | ✅ | ✅ | All three ~614 LOC, near-identical. |
| ConfigTool | ✅ | ✅ | ✅ | CCB 820 LOC; ours 854 LOC (gated on `USER_TYPE === 'ant'` which our entrypoint sets). |
| NotebookEditTool | ✅ | ✅ | ✅ | (Redundant entry — already covered by stock-tools row.) |
| SuggestBackgroundPRTool | ⚠️ | ⚠️ | ⚠️ | Ant-only Anthropic-internal feature. CCB packages 84-LOC real impl; Gitlawb + ours both 3-LOC/2-LOC null-export stubs. **Gitlawb demoted ✅→⚠️** on 2026-04-25 — file exists as null-export stub. |
| VerifyPlanExecutionTool | ⚠️ | ⚠️ | ✅ | See §2 — CCB is self-report, Gitlawb is 3-LOC null-export stub (refinement ❌→⚠️ on 2026-04-25 — file exists), ours is 224-LOC active forked-agent verifier. |
| WorkflowTool | ✅ | ✅ | ✅ | — |
| ToolSearchTool (tool deferral) | ✅ | ✅ | ✅ | CCB at `packages/builtin-tools/src/tools/ToolSearchTool/` (593 LOC). Native deferral on all providers (ours unique: non-Anthropic supported via text `<discovered-tools>` markers). |
| SyntheticOutputTool | ✅ | ✅ | ✅ | CCB 163 LOC at `packages/builtin-tools/src/tools/`; ours 163 LOC at `src/tools/SyntheticOutputTool/SyntheticOutputTool.ts` — **dynamic-injected** at `main.tsx:1855` + `cli/print.ts:1544` for `--output-format=json` flow (added AFTER `getTools()` filtering, so registry-grep alone misses it). Audit's prior `❌` was a wiring blind spot, not absence. |
| TeamCreateTool / TeamDeleteTool | ✅ | ✅ | ✅ | CCB 360+265 LOC at packages; ours 359+175 LOC, gated on `USER_TYPE === 'ant'`. |
| TungstenTool | ⚠️ | ⚠️ | ⚠️ | Ant-only; all three forks ship null-export stubs. CCB 8-LOC auto-generated stub (`(() => {}) as unknown as Tool`), Gitlawb 4-LOC `export const TungstenTool = null`, ours 4-LOC same shape. **CCB flip — → ⚠️ + Gitlawb demoted ✅→⚠️** on 2026-04-25. |
| CtxInspectTool | ✅ | ❌ | ✅ | Internal dev tool. CCB packages 324 LOC real impl; Gitlawb truly missing; **ours 122 LOC ported from CCB on 2026-04-25** at `src/tools/CtxInspectTool/CtxInspectTool.ts` — reports total tokens via `tokenCountWithEstimation()` + message count + caching/session-memory/collapse status. Required adding `getStats()` no-op to `services/contextCollapse/index.ts` (stub returns 0/0/0). Wired via direct-import + dual-fallback spread (`CtxInspectTool ?? CtxInspectToolDirect`) at `tools.ts`. |
| SnipTool + `/force-snip` | ✅ | ❌ | ✅ | CCB has `commands/force-snip.ts` + `packages/builtin-tools/src/tools/SnipTool/` (93 LOC); Gitlawb missing; ours `services/compact/snipCompact.ts` + 45-LOC tool. |
| PushNotificationTool | ✅ | ❌ | ✅ (++) | CCB packages 133 LOC: bridge-bound (RCS-dependent — `sent: false` without hosted infra). Ours: local terminal escapes (iTerm2/Kitty/Ghostty/bell) + notification hooks — independently functional. See §3. |
| SubscribePRTool + `/subscribe-pr` | ✅ (stub) | ❌ | ✅ | CCB packages 88-LOC stub returning `error: 'requires KAIROS GitHub webhook subsystem'` unconditionally. Gitlawb omits. Ours: 193-line working `gh` CLI polling + cron implementation. Only fork that actually subscribes to PRs. See §3. |
| OverflowTestTool | ⚠️ | ❌ | ⚠️ | Internal dev tool. CCB 3-LOC auto-generated stub (`export {}; export const OVERFLOW_TEST_TOOL_NAME: string = '';`), Gitlawb truly missing, ours 2-LOC null-export. **CCB flip — → ⚠️** on 2026-04-25 (kickoff predicted ✅ but content read shows stub-shape). |
| TerminalCaptureTool | ✅ | ❌ | ✅ (++) | CCB packages 83-LOC stub that returns empty content (TERMINAL_PANEL infra never shipped in CCB). Gitlawb truly missing. **Ours ~120 LOC implemented on 2026-04-25** at `src/tools/TerminalCaptureTool/TerminalCaptureTool.ts` — taps MonitorTool's task buffer via `getTaskOutputPath(panel_id)` + `tail`-style line slice; without `panel_id`, lists running monitor sessions via `getRunningTasks(state).filter(isMonitorMcpTask)`. `(++)` because ours is functionally working where CCB's only ever returns empty data. |
| CodeGraph tool (28 operations) | ❌ | ❌ | ✅ | **Ours-unique.** 1511 LOC at `src/tools/CodeGraphTool/` — full tree-sitter knowledge-graph dispatcher (build/query/impact/refactor/flows/communities/cross-repo/wiki). |
| ListPeersTool | ✅ | ❌ | ✅ | CCB packages 107-LOC real `buildTool()` impl (`name: 'ListPeers'`, full inputSchema/prompt/mapToolResultToToolResultBlockParam — same surface as ours' 66-LOC impl). Gitlawb truly missing. **CCB flip ❌→✅** on 2026-04-25. |
| DiscoverSkillsTool | ✅ | ❌ | ✅ | **NEW row 2026-04-25, ported same day.** CCB packages 107-LOC tool + 13-LOC prompt + tests dir. Gitlawb missing. **Ours implemented on 2026-04-25** at `src/tools/DiscoverSkillsTool/DiscoverSkillsTool.ts` (107 LOC tool + 16 LOC prompt + 444 LOC `services/skillSearch/localSearch.ts` TF-IDF index + 161 LOC adapted `prefetch.ts` + 10 LOC `signals.ts` + updated `featureCheck.ts`) — TF-IDF skill search lets the model find skills by description (e.g. `description="reverse engineering binary"` → returns `ghidra-re` ranked by score). CJK / `intentNormalize.ts` infra explicitly NOT ported per user request — ASCII-only TF-IDF, no Haiku-driven Chinese-to-English query normalization. Live-verified end-to-end via `-p` mode. |
| NativeAdvisorTool | ❌ | ❌ | ✅ | **NEW row 2026-04-25. Ours-unique.** 210 LOC at `src/tools/NativeAdvisorTool/NativeAdvisorTool.ts`. Tool name `'advisor'`. Wires `sideQuery()` to a strategic-guidance system prompt; gated on `getInitialAdvisorModeSetting() === 'native'`. The model-facing surface for our advisor-executor pattern. |
| ReviewArtifactTool | ✅ | ❌ | ✅ | **NEW row 2026-04-25, ported same day.** CCB packages 142 LOC real impl with annotation/severity inputSchema. Gitlawb missing. **Ours 142 LOC ported verbatim from CCB on 2026-04-25** at `src/tools/ReviewArtifactTool/ReviewArtifactTool.ts` — stateless emit of artifact + per-line annotations (line/message/severity) + summary; output flows inline to transcript. Wired via direct-import + dual-fallback spread at `tools.ts`. |
| SendUserFileTool | ✅ | ❌ | ⚠️ (stub, KAIROS-future) | **NEW row 2026-04-25.** CCB packages 122 LOC (`SendUserFileTool.ts` + `prompt.ts`); Gitlawb missing; ours 3-LOC null-export stub gated on `feature('KAIROS')` (we have KAIROS but no file-delivery transport — CCB's relies on Anthropic's RCS bridge for mobile push). Stay stub. |
| WebBrowserTool | ✅ | ❌ | ⚠️ (stub, deliberately disabled — replaced by zendriver-mcp) | **NEW row 2026-04-25.** CCB packages 266 LOC across `WebBrowserPanel.ts` + `WebBrowserTool.ts` + tests. Gitlawb missing. Ours 4-LOC stub; `tools.ts:121` hardcodes `const WebBrowserTool = null` with the require **explicitly commented out** (not feature-gated) per CLAUDE.md ("Built-in browser tools commented out — zendriver-mcp is sole browser provider"). |

---

## 9. Slash commands (by category)

Large and messy to compare — lots of "commands that are commands" overlap. Commands that are truly present only in one fork are flagged; the vast majority are present in at least two.

### 9a. Core UX / session

| Command | CCB | Gitlawb | ours | Notes |
|---|---|---|---|---|
| `/help` | ✅ | ✅ | ✅ | — |
| `/clear` | ✅ | ✅ | ✅ | — |
| `/exit` / `/logout` / `/login` | ✅ | ✅ | ✅ | — |
| `/resume` | ✅ | ✅ | ✅ | — |
| `/compact` | ✅ | ✅ | ✅ | — |
| `/config` | ✅ | ✅ | ✅ | — |
| `/model` | ✅ | ✅ | ✅ | — |
| `/theme` | ✅ | ✅ | ✅ | — |
| `/status` / `/stats` / `/usage` / `/cost` | ✅ | ✅ | ✅ | All four. |
| `/memory` | ✅ | ✅ | ✅ | — |
| `/tasks` | ✅ | ✅ | ✅ | — |
| `/release-notes` | ⚠️ | ✅ | ✅ | Ours fetches `coffeegrind123/changelog`. |
| `/upgrade` | ⚠️ | ✅ | ⚠️ | We use GitHub Releases auto-updater. |
| `/version` | ✅ | ✅ | ✅ | — |
| `/context` | — | ✅ | ✅ | — |
| `/session`, `/share`, `/summary` | — | ✅ | ⚠️ | ours: no `/session`; `/share` + `/summary` present. |
| `/mobile` | — | ✅ | ✅ | — |
| `/rename` | — | ✅ | ✅ | — |
| `/export` | — | ✅ | ✅ | — |
| `/copy` | — | ✅ | ✅ | — |
| `/files` | — | ✅ | ✅ | — |
| `/diff` | — | ✅ | ✅ | — |
| `/branch` | — | ✅ | ✅ | — |
| `/tag` | — | ✅ | ✅ | — |
| `/color` | — | ✅ | ✅ | — |
| `/rewind` (session rollback) | ❌ | ✅ | ✅ | `src/commands/rewind/`. |
| `/teleport` (cross-project resume) | ❌ | ✅ | ✅ | `src/commands/teleport/`. |
| `/thinkback`, `/thinkback-play` | ❌ | ✅ | ✅ | — |
| `/passes` | ❌ | ✅ | ✅ | — |
| `/insights` | ❌ | ✅ | ✅ | — |
| `/effort` | ❌ | ✅ | ✅ | — |
| `/fast` | ⚠️ | ✅ | ✅ | Ours = fast mode (Opus 4.6). Different concept. |
| `/stickers` | — | ✅ | ✅ | — |
| `/good-claude` | — | ✅ | ✅ | — |
| `/btw` | — | ✅ | ✅ | — |
| `/recap` | ❌ | ❌ | ✅ | Our unique. |
| `/statusline` | — | ✅ | ✅ | Ours replaced by Fuelgauge by default. |

### 9b. Provider / Auth / Setup

| Command | CCB | Gitlawb | ours | Notes |
|---|---|---|---|---|
| `/provider` | ❌ | ✅ | ❌ | Gitlawb flagship. |
| `/onboard-github` | ❌ | ✅ | ❌ | — |
| `/oauth-refresh` | ❌ | ✅ | ✅ | — |
| `/terminalSetup` | ✅ | ✅ | ✅ | — |
| `/install`, `/install-github-app`, `/install-slack-app` | — | ✅ | ✅ | — |
| `/plugin`, `/reload-plugins` | — | ✅ | ✅ | — |
| `/setup-bedrock`, `/setup-vertex` | ❌ | ❌ | ✅ | Our unique. |
| `/add-dir` | ✅ | ✅ | ✅ | — |
| `/agents` | ✅ | ✅ | ✅ | — |
| `/onboarding` | ✅ | ✅ | ✅ | — |

### 9c. Diagnostics

| Command | CCB | Gitlawb | ours | Notes |
|---|---|---|---|---|
| `/doctor` | ⚠️ | ✅ | ✅ | All three have `/doctor` screen; only Gitlawb ships structured `doctor:runtime` CLI. |
| `/cache-probe` | ❌ | ✅ | ❌ | `src/commands/cache-probe/` (#580). |
| `/debug-tool-call` | — | ✅ | ✅ | — |
| `/heapdump` | — | ✅ | ✅ | — |
| `/ctx_viz` | — | ✅ | ✅ | — |
| `/perf-issue` | — | ✅ | ✅ | — |
| `/env` | — | ✅ | ✅ | — |
| `/feedback`, `/issue`, `/pr_comments` | — | ✅ | ✅ | — |
| `/dump-prompt` | ❌ | ❌ | ✅ | Our unique. |
| `/ant-trace` | — | ✅ | ✅ | — |
| `/mock-limits`, `/rate-limit-options`, `/reset-limits` | — | ✅ | ✅ | — |
| `/privacy-settings` | — | ✅ | ✅ | — |
| `/sandbox-toggle` | — | ✅ | ✅ | — |
| `/benchmark` | — | ✅ | ❌ | — |
| `/break-cache` | — | ✅ | ✅ | — |

### 9d. Automation / Workflow

| Command | CCB | Gitlawb | ours | Notes |
|---|---|---|---|---|
| `/auto-fix` (lint+test after edits) | ❌ | ✅ | ❌ | `services/autoFix/`. |
| `/autofix-pr` | — | ✅ | ✅ | — |
| `/bughunter` | — | ✅ | ✅ | — |
| `/commit`, `/commit-push-pr` | — | ✅ | ✅ | — |
| `/review`, `/security-review` | ✅ | ✅ | ✅ | Bundled skills. |
| `/init` | ✅ | ✅ | ✅ | — |
| `/init-verifiers` | — | ❌ | ✅ | Our unique. |
| `/plan` | ✅ | ✅ | ✅ | — |
| `/ultraplan` | ✅ | ✅ | ✅ | All three. Ours refactored to local forked agent. |
| `/loop` (fixed + dynamic scheduling) | ⚠️ | ✅ | ✅ | Gitlawb: `src/commands/loop/` (#621). Ours: `loop` skill + `cron*.ts` scaffolding. |
| `/workflows`, `/schedule` | ✅ | ✅ | ✅ | — |
| `/torch` | — | ❌ | ✅ | Our unique. |
| `/fork` | ✅ | ❌ | ✅ | — |
| `/super` | ❌ | ❌ | ✅ | Our unique. |
| `/proactive` | ✅ | ✅ | ✅ | — |
| `/assistant` | ✅ | ✅ | ✅ | — |
| `/coordinator` | ✅ | ✅ | ✅ | — |
| `/agents-platform` | ✅ | ✅ | ⚠️ | Stub (Ant-only). |
| `/buddy` | ✅ | ✅ | ✅ | — |
| `/dream` | ✅ | ✅ | ✅ (skill) | — |
| `/wiki` | ⚠️ | ✅ | ⚠️ | CCB: Teach-Me + background sessions partially cover. Gitlawb: `src/commands/wiki/` + `services/wiki/` (8 files: index builder, ingestion, status) (#532). Ours: only CodeGraph's `generate_wiki` for community pages. |
| `/voice` | ✅ | ✅ | ✅ | Same UX, three different backends. |
| `/vim` | ❌ | ✅ | ✅ | `src/vim/` (Gitlawb: motions/operators/textObjects/transitions/types; ours too). |
| `/keybindings` | ⚠️ | ✅ | ✅ | — |
| `/chrome` | ✅ | ✅ | ✅ | — |
| `/desktop` | — | ✅ | ✅ | — |
| `/ide` | — | ✅ | ✅ | — |
| `/edit-system-prompt` | ❌ | ❌ | ✅ | Our unique. |
| `/backfill-sessions` | — | ✅ | ✅ | — |
| `/permissions` | ✅ | ✅ | ✅ | — |
| `/hooks` | ✅ | ✅ | ✅ | — |
| `/skills` | ✅ | ✅ | ✅ | — |
| `/security-review` | ✅ | ✅ | ✅ | Bundled skill. |

### 9e. Multi-instance / Remote (CCB + ours heavy)

| Command | CCB | Gitlawb | ours | Notes |
|---|---|---|---|---|
| `/pipes`, `/attach`, `/detach`, `/send`, `/claim-main`, `/pipe-status`, `/peers` | ✅ | ❌ | ✅ | CCB source: `commands/{attach,claim-main,detach,peers,pipe-status,pipes,send}/`. Confirmed. |
| `/bridge`, `/bridge-kick` | ✅ | ✅ | ✅ | — |
| `/remote-env`, `/remote-setup` | ✅ | ✅ | ✅ | All three ship both. CCB: `commands/remote-env/` (2 files) + `commands/remote-setup/` (3 files). |
| `/submit`, `/ccr-server` | ❌ | ❌ | ✅ | Our unique (CCR). |
| `/remoteControlServer` | ✅ | ⚠️ | ✅ | CCB: `commands/remoteControlServer/` dir. |
| `/daemon` | ✅ | ⚠️ | ✅ | CCB: `commands/daemon/daemon.tsx` + `index.ts`. Ours: `claude daemon start/stop/status/restart`. |
| `/fork` (sub-agent spawn) | ✅ | ❌ | ✅ | — |
| `/force-snip` | ✅ | ❌ | ✅ | — |
| `/init-verifiers` | ✅ | ❌ | ✅ | Confirmed at source. |
| `/subscribe-pr` | ✅ | ❌ | ✅ | Confirmed at source. |
| `/monitor` | ✅ | ❌ | ❌ | `commands/monitor.ts` — CCB-unique. |
| `/focus`, `/tui` | — | — | ✅ | Our unique. |
| `/initMode` | — | ✅ | ❌ | — |
| `/memory-import`, `/memory-export`, `/memory-cli` | ❌ | ❌ | ✅ | Our unique. |

### 9f. Distinctive CCB commands (source-verified)

| Command | CCB | Gitlawb | ours | Notes |
|---|---|---|---|---|
| `/autonomy` + `autonomyPanel` | ✅ | ❌ | ❌ | CCB-unique. `commands/autonomy.ts` + `autonomyPanel.tsx` — inspects autonomy runs for proactive ticks + scheduled tasks; sub-args: `status/runs/flows/flow/flow cancel/flow resume`. Paired with `utils/autonomy{Authority,CommandSpec,Flows,Persistence,Runs,Status}.ts` (6-file subsystem). |
| `/lang` | ✅ | ❌ | ❌ | `commands/lang/lang.ts` — language/locale switcher. |
| `/poor` + poorMode | ✅ | ❌ | ❌ | `commands/poor/poor.ts` + `poorMode.ts` — reduced-resource mode (unclear semantics; likely low-context / Ollama-mode toggle). |
| `/skill-search`, `/skill-learning` | ✅ | ❌ | ❌ | CCB-unique. Paired with real `services/skillSearch/` (~970 lines) + `services/skillLearning/`. |
| `/history`, `/job` | ✅ | ❌ | ❌ | — |
| Teach-Me skill | ✅ | ❌ | ❌ | Socratic Q&A for project modules; docs-documented. |
| `/kairos` (superset of assistant) | ✅ | ⚠️ | ⚠️ | CCB-unique naming. Our `/assistant` covers functional scope. |
| `/templates` job/template bootstrap | ✅ | ⚠️ | ✅ | Ours: `~/.claude/templates/*.md` + job classifier. |
| `/debug` (Bun inspect attach) | ✅ | ❌ | ❌ | CCB-unique. |
| `/advisor` | ✅ | ✅ | ✅ | — |

---

## 10. Memory / Compaction / Session

| Feature | CCB | Gitlawb | openclaude | Location / Notes |
|---|---|---|---|---|
| File-based project memory (`MEMORY.md` + sidecars) | ✅ | ✅ | ✅ | CCB: per-project under `~/.claude/projects/<slug>/memory/`. Gitlawb: `src/memdir/` (`findRelevantMemories`, `memoryAge`, `memoryScan`, `teamMemPaths`, `teamMemPrompts`). Ours: similar path. |
| Sonnet-driven memory recall injection | ✅ | ✅ | ✅ | — |
| Extract memories service | ✅ | ✅ | ✅ | All three: `services/extractMemories/`. |
| Session memory | ✅ | ✅ | ✅ | `services/SessionMemory/`. |
| Team memory (Anthropic backend) | ✅ | ✅ | ✅ | — |
| Team memory GitHub backend | ❌ | ❌ | ✅ | Our unique. `services/teamMemorySync/githubBackend.ts`. |
| Team memory secret scanner | ✅ | ✅ | ✅ | — |
| MicroCompact (single tool) | ✅ | ✅ | ✅ (++) | `services/compact/microCompact.ts`. Ours + Gitlawb: `isCompactableTool(name)` helper compacts `mcp__*` tools in addition to the built-in 8 — matters because Ghidra decompile / zendriver screenshot / Computer Use MCP outputs are routinely huge. CCB compacts built-ins only. |
| Cached MicroCompact | ✅ | ❌ | ✅ | Ported CCB's 112-line implementation 2026-04-24 (commit `1e1983f`). `CLAUDE_CACHED_MICROCOMPACT=1` env gate + Claude 4.x regex; emits `{type: 'cache_edits', edits: [{type: 'delete_tool_result', tool_use_id}]}` block when >10 tool results accumulate, keeps last 5. Aligned `CachedMCEditsBlock` type in `services/api/claude.ts` with CCB's tool_use_id shape (prior `cache_reference` shape was dead — we never name cache breakpoints). Added `markToolsDeleted` helper over CCB for eager state mutation at microCompact call site. See `coffeegrind123/openclaude:context/memory-compaction-session-deepdive.md` §9 + Tier 2 #5. |
| Session Memory Compact | ✅ | ✅ | ✅ | — |
| Full message compaction | ✅ | ✅ | ✅ | — |
| Context Collapse (3-tier overflow recovery) | ⚠️ | ⚠️ | ⚠️ | **Corrected.** All three ship STUBS under `services/contextCollapse/` (CCB 75-line, Gitlawb 7-line, ours 24-line). Overflow recovery in our fork is delivered via `reactiveCompact` + forced auto-compact fallback (next two rows), not contextCollapse. See `coffeegrind123/openclaude:context/memory-compaction-session-deepdive.md` §12. |
| Reactive Compact (pivot-based partial compact on PTL) | ❌ | ❌ | ✅ | Our unique. `services/compact/reactiveCompact.ts`. |
| Forced auto-compact fallback | ❌ | ⚠️ | ✅ | Our unique. `force` parameter on `autoCompactIfNeeded()` bypasses estimated-token threshold; trusts API overflow reports. Also: universal effective-context floor in `getEffectiveContextWindowSize()` clamps to `summaryReservation + AUTOCOMPACT_BUFFER_TOKENS` for any small-context 3P provider (not just DeepSeek via `lowContextMode`). Ported from Gitlawb 2026-04-24. |
| Snip output compaction | ❌ | ❌ | ✅ | Our unique. `services/compact/snipCompact.ts`. |
| Session transcript (JSONL) | ✅ | ✅ | ✅ | Via `utils/sessionStorage.ts` on all three. `services/sessionTranscript/` file specifically is a stub on all three (CCB 6-line, Gitlawb none, ours 1-line) — upstream likely moved the boundary-writer into a dedicated service that no fork ported. |
| Session restore / resume | ✅ | ✅ | ✅ | — |
| Session title / URL | ✅ | ✅ | ✅ | — |
| Session ingress auth | ✅ | ✅ | ✅ | **Corrected.** `utils/sessionIngressAuth.ts` identical 140 lines across all three. |
| Conversation recovery (mid-stream failure) | ✅ | ✅ (++) | ✅ (++) | **Corrected.** All three ship `utils/conversationRecovery.ts` (CCB 600, Gitlawb 663, ours 663). Ported Gitlawb's `ResumeTranscriptTooLargeError` + `assertResumeMessageSize()` 8 MiB hard cap 2026-04-24 (prevents multi-GB resume bombs; wired at two call sites — post-deserialize and post-hook-append). Still open: `stripThinkingBlocks` for 3P-provider resume (Tier 2). Ours also retains malformed-text-block sanitization Gitlawb lacks. See deep-dive §20. |
| Crossproject-resume | — | ✅ | ✅ | — |

---

## 11. Context / Token management

| Feature | CCB | Gitlawb | openclaude | Location / Notes |
|---|---|---|---|---|
| Token Budget (`+500k`, `spend 1B`) | ✅ | ✅ | ✅ | All three: `query/tokenBudget.ts`. |
| Tree-sitter Bash AST | ✅ | ✅ | ✅ | Line-for-line equivalent; live in all. |
| Token analytics | ⚠️ | ⚠️ | ⚠️ | Gitlawb's `utils/tokenAnalytics.ts` (210 lines, `TokenUsageTracker` class with historical accumulation + `estimateCost`/`export`/`import`) exists but is **unwired dead library code** — `grep` for the class in Gitlawb returns only its own test file. Ours + CCB lack the class entirely. Demoted Gitlawb from `✅` to `⚠️` on 2026-04-24 to reflect the file-exists-but-inert state. Structural note: this is an in-memory tracker, not a translator, so unlike other §11 items it has no natural openaiBridge-scoping — lives independently in a hypothetical cost-dashboard / `/tokens` command. See `coffeegrind123/openclaude:context/context-token-deepdive.md`. |
| Thinking token extraction (3P `<think>` tags) | ❌ | ⚠️ | ❌ | Gitlawb's `utils/thinkingTokenExtractor.ts` (191 lines, `ThinkingTokenAnalyzer` class) is only referenced by its own `.test.ts` — unwired in runtime. Demoted from `✅` to `⚠️` on 2026-04-24 (same reasoning as Token analytics row above). Ours + CCB: absent. Name is misleading — this file counts tokens in *already-parsed* Anthropic `thinking` blocks; the tag-stripping feature lives in the separate Thinking-tag sanitizer row below. See `coffeegrind123/openclaude:context/context-token-deepdive.md`. |
| Thinking-tag sanitizer (tag-based filter) | ❌ | ✅ | ✅ | Ported 2026-04-24 in openclaude. `services/api/thinkTagSanitizer.ts` (162 lines verbatim) + 42 unit tests. 3-layer: `stripThinkTags` whole-text + `createThinkTagFilter` streaming state machine (handles partial tags split across SSE frames) + `flush` partial-tag discard. **openaiBridge-scoped only**, mirroring compressToolHistory — wired per-stream in `openaiBridge/streamTranslator.ts` (text-delta feed + finalize flush) + `openaiBridge/responseTranslator.ts` (whole-text cleanup). Anthropic-native path (z.ai / DeepSeek-via-Anthropic-endpoint / first-party) bypasses entirely. |
| Small-context tool_result compression | ❌ | ✅ | ✅ | Ported 2026-04-24 (commit `1e1983f`). `services/api/compressToolHistory.ts` adapted for our `openaiBridge` shape. Tiered recent/mid/old compression with `MID_MAX_CHARS=2000` truncate + old-tier `[tool args=… → N chars omitted]` stubs; tiers scale via `getEffectiveContextWindowSize()`. Wired as pre-translate pass in `translateAnthropicRequestToOpenAI()`. Default-off via `toolHistoryCompressionEnabled` setting. Reuses our `isCompactableTool` + `TOOL_RESULT_CLEARED_MESSAGE`. Complements (doesn't replace) microCompact. |
| Prompt cache break detection | ✅ | ✅ | ✅ | `services/api/promptCacheBreakDetection.ts` byte-identical between Gitlawb + ours (727 lines, zero diff); CCB differs by 1 type-cast character. Wired identically in all three via `claude.ts` + `compact.ts` + `microCompact.ts` + `autoCompact.ts` + `AgentTool/runAgent.ts`. Audit was wrong `— ✅ ⚠️` → corrected to `✅ ✅ ✅` on 2026-04-24. See `coffeegrind123/openclaude:context/context-token-deepdive.md`. |
| 1M context entitlement check | ✅ | ✅ | ✅ | `utils/model/check1mAccess.ts` byte-identical across all three forks (72 lines, zero diff). Same 3-call-site wiring in all (`commands/model/model.tsx` + `utils/model/modelOptions.ts` + `utils/model/contextWindowUpgradeCheck.ts`). Audit was wrong `— ✅ ⚠️` → corrected to `✅ ✅ ✅` on 2026-04-24. See `coffeegrind123/openclaude:context/context-token-deepdive.md`. |
| Tool argument normalization (bash/OpenAI) | — | ✅ | ✅ | Ported 2026-04-24 in openclaude. `services/api/toolArgumentNormalization.ts` (69 lines verbatim) + 20 unit tests. Maps plain-string tool arguments (`"ls -la"` → `{command: "ls -la"}` for Bash; `"src/foo.ts"` → `{file_path: "src/foo.ts"}` for Read/Write/Edit; `"*.ts"` → `{pattern: "*.ts"}` for Glob/Grep) that OpenAI-compat providers emit. **openaiBridge-scoped only** — wired per-stream in `openaiBridge/streamTranslator.ts` (per-tool `jsonBuffer`, emit normalized JSON once at `content_block_stop` to avoid partial-string leakage through `input_json_delta`; raw buffer preserved on `finish_reason='length'` to avoid coercing truncated output into a confidently-malformed command) + `openaiBridge/responseTranslator.ts` (non-streaming — direct replacement for prior `_raw_arguments` fallback). Non-mapped tools (MCP/custom) pass fragments through as before. Anthropic-native path needs nothing. |
| OpenAI strict schema sanitizer | — | ✅ | ✅ | Ported 2026-04-25 in openclaude. `utils/schemaSanitizer.ts` (258 lines verbatim) + 3 unit tests. Strips OpenAI-incompatible JSON-schema keywords ($comment, $schema, default, else, examples, format, if, maxLength, maximum, minLength, minimum, multipleOf, pattern, patternProperties, propertyNames, then, unevaluatedProperties); recurses into anyOf/oneOf/allOf; filters `required[]` against actual properties; validates enum/const against the remaining type constraint; normalizes type:"null" and array-typed type fields. **openaiBridge-scoped only** — wired into `openaiBridge/requestTranslator.ts:sanitizeToolParameters()` (replaces prior no-op pass-through stub). The Anthropic-native path bypasses since first-party Anthropic accepts the full JSON Schema spec. End-to-end verified via `translateTools()` smoke test against an MCP-style schema with `pattern`/`examples`/`maximum`/`default`. |
| 3P auto-compact infinite loop fix | — | ✅ | ✅ | All now have. |
| Low-context mode (DeepSeek auto) | ❌ | ❌ | ✅ | Our unique. `utils/lowContextMode.ts`. |
| Unknown 3P model context fallback | — | ✅ | ✅ | — |

---

## 12. Web / Search / Fetch

| Feature | CCB | Gitlawb | openclaude | Location / Notes |
|---|---|---|---|---|
| WebSearch tool (Anthropic built-in) | ✅ | ✅ | ❌ | Ours commented out. |
| WebFetch tool (Anthropic built-in) | ✅ | ✅ | ❌ | — |
| DuckDuckGo fallback (no key) | ❌ | ✅ | ❌ | `duck-duck-scrape` dep. Default on non-Anthropic. |
| Firecrawl search + fetch | ❌ | ✅ | ❌ | `@mendable/firecrawl-js` dep + `FIRECRAWL_API_KEY`. |
| Bing HTML scrape adapter | ✅ | ✅ | ❌ | CCB + Gitlawb (#593, #537). |
| Brave HTML scrape adapter | ✅ | ✅ | ❌ | — |
| `WEB_URL_TEMPLATE` custom search | ❌ | ✅ | ❌ | (#537). |
| SSRF bypass guard in custom provider | — | ✅ | — | (#610). |
| Multi-adapter fallback chain | ✅ | ✅ | ❌ | CCB: API → Bing → Brave. |
| Browser automation via MCP | ✅ (claude-in-chrome) | ✅ (claude-in-chrome) | ✅ (zendriver) | Three different implementations. |
| Terminal in-browser interaction (WebView) | ✅ (WebBrowserTool) | ✅ | ⚠️ | CCB has Bun WebView tool; Gitlawb has `WebBrowserTool`; we have stub. |

---

## 13. Voice

| Feature | CCB | Gitlawb | openclaude | Location / Notes |
|---|---|---|---|---|
| Voice Mode (push-to-talk) | ✅ | ✅ | ✅ | — |
| Anthropic Nova 3 STT backend | ✅ | ✅ | ⚠️ | CCB: requires Anthropic OAuth. Gitlawb: same. Ours: preserved behind `VOICE_STREAM_BASE_URL`. |
| Local faster-whisper STT | ❌ | ❌ | ✅ | Our unique. `utils/voiceLocal/`. |
| Voice key-terms | — | ✅ | ⚠️ | — |

---

## 14. Observability / Diagnostics / Telemetry

| Feature | CCB | Gitlawb | openclaude | Location / Notes |
|---|---|---|---|---|
| Telemetry neutralized (analytics stubs) | ❌ | ⚠️ | ✅ | Our unique: all analytics return no-op. |
| OpenTelemetry stack | ⚠️ | ✅ | ✅ | All three have some. |
| Datadog exporter | — | ✅ | ❌ | — |
| BigQuery 1P event logging | ✅ | ✅ | ❌ | — |
| Langfuse monitoring | ✅ | ❌ | ❌ | CCB-unique. `src/services/langfuse/` (real service) + `packages/langfuse-dashboard/` + `@langfuse/otel` + `@langfuse/tracing` deps. |
| Custom observability dashboard | ❌ | ❌ | ✅ | `openclaude-observe` repo — our unique. |
| OTLP collector support (generic) | ⚠️ | ✅ | ✅ | Ours via env `OTEL_EXPORTER_OTLP_ENDPOINT`. |
| Session tracing | ⚠️ | ✅ | ✅ | — |
| Perfetto profiling | — | ✅ | ❌ | — |
| Doctor runtime check (script) | ❌ | ✅ | ❌ | `scripts/system-check.ts`. |
| Doctor JSON report | ❌ | ✅ | ❌ | `--out reports/doctor-runtime.json`. |
| Doctor context warnings | — | ✅ | ✅ | `utils/doctorContextWarnings.ts`. |
| Request logging | ✅ | ✅ | ✅ | — |
| OpenAI error classification | — | ✅ | ⚠️ | `services/api/openaiErrorClassification.ts`. |
| Sentry integration | ⚠️ | ❌ | ❌ | CCB optional. We stub. |
| GrowthBook A/B testing | ⚠️ | ⚠️ | ⚠️ | CCB uses w/ local defaults; Gitlawb + us force-default. |
| Local feature-flag override (`~/.claude/feature-flags.json`) | — | ✅ | ❌ | (#639). |
| Fuelgauge status line | ❌ | ❌ | ✅ | Our unique (port of adityaarakeri/fuelgauge). |
| Session title | ✅ | ✅ | ✅ | — |
| Privacy level | ⚠️ | ✅ | ⚠️ | `utils/privacyLevel.ts`. |
| Distill tool-output compaction | ❌ | ❌ | ✅ | Our unique: 59 filters + arg injection + sidecar analytics. |
| Shot stats (API call telemetry panel) | ✅ | ⚠️ | ⚠️ | CCB-specific UI. |

---

## 15. Hooks / Self-Healing / Automation

| Feature | CCB | Gitlawb | openclaude | Location / Notes |
|---|---|---|---|---|
| Pre/PostToolUse hooks | ✅ | ✅ | ✅ | — |
| Project `.claude/hooks/` markdown | ✅ | ✅ | ✅ | — |
| `defer` permission in PreToolUse | ⚠️ | ❌ | ✅ | 2.1.89 backport — only ours ships it. CCB + Gitlawb `permissionDecision` enum is `"allow"\|"deny"\|"ask"`, no `defer` value. See §15 deep-dive. |
| Hook output >50K → disk | ⚠️ | ❌ | ✅ | 2.1.89 backport — only ours ships it. Zero hits for `HOOK_OUTPUT_DISK_THRESHOLD` or any size-based output-spillover pattern in CCB or Gitlawb. See §15 deep-dive. |
| **Hook Chains** (event → action DSL) | ❌ | ✅ | ✅ | `utils/hookChains.ts` (1518 LOC) + `docs/hook-chains.md` (333 LOC). `spawn_fallback_agent`, `notify_team`, `warm_remote_capacity`. Depth guard + cooldown + dedup. Ours: ported 2026-04-25 (commit `9c4cb7e`); env-gated via `CLAUDE_CODE_ENABLE_HOOK_CHAINS=1` + `feature('HOOK_CHAINS')`. See `coffeegrind123/openclaude:context/hooks-self-healing-deepdive.md`. |
| AutoFix service (auto-lint/test after edits) | ❌ | ✅ | ✅ | `services/autoFix/` (#508; 263 LOC source). Ours: ported 2026-04-25 (commit `7ff1396`); opt-in via `settings.autoFix.enabled: true` + at least one of `lint`/`test`. `/auto-fix` command for config help. See §15 deep-dive. |
| Auto-fix hook integration | ❌ | ✅ | ✅ | `autoFixHook.ts`. Sub-feature — ported alongside AutoFix in commit `7ff1396`. |
| PostToolUseFailure dispatch | ❌ | ✅ | ✅ | Hook Chains trigger source. Sub-feature — ported alongside Hook Chains in commit `9c4cb7e`. |
| TaskCompleted hook | ✅ | ✅ | ✅ | `executeTaskCompletedHooks` + `getTaskCompletedHookMessage` are full async-generator implementations in all three forks; identically wired into `stopHooks.ts`. The "Hook Chains hook into this" annotation is true for Gitlawb only and belongs on the Hook Chains row, not gating the TaskCompleted row. |
| Provider self-healing (local readiness) | ❌ | ❌ | ❌ | **Phantom citation** — zero hits for `selfHeal`/`providerHealth`/`isProviderReady`/`readinessCheck` in any Gitlawb `provider*.ts`. #738 doesn't exist as runtime source. Drop row in next pass. See §15 deep-dive. |
| Conversation recovery | ✅ | ✅ | ✅ | See §10 — Tier 1 8 MiB cap ported 2026-04-24. Still open: 3P-provider thinking-block strip (Tier 2). |
| Away summary | ✅ | ✅ | ✅ | See §3 — full three-way parity after 2026-04-24 idle-fallback port. |
| Cleanup registry | ✅ | ✅ | ✅ | Byte-identical 25 LOC across all three forks (`diff` shows zero bytes). |

---

## 16. Skills

| Feature | CCB | Gitlawb | openclaude | Location / Notes |
|---|---|---|---|---|
| Bundled skills (generic) | ✅ | ✅ | ✅ | — |
| Skills frontmatter (whenToUse, allowedTools, tags) | ✅ | ✅ | ✅ | — |
| Two-part execution (inline / fork) | ✅ | ✅ | ✅ | — |
| Remote skill discovery | ⚠️ | ⚠️ | ⚠️ | §16 deep-dive: CCB's `remoteSkillLoader.ts` (17 LOC) + `remoteSkillState.ts` (3 LOC) + `telemetry.ts` (11 LOC) are explicitly labeled `// Auto-generated stub — replace with real implementation` and return no-ops. Three-way stub-shaped — actual fetch+parse+cache logic does not exist in any source tree. CCB previously ✅ overstated. See `coffeegrind123/openclaude:context/skills-deepdive.md`. |
| **Experimental Skill Search** (TF-IDF) | ✅ | ❌ | ✅ | §16 deep-dive: post-§9 parity confirmed. Ours `services/skillSearch/` = 602 LOC across 7 files (`localSearch.ts` 416 + `prefetch.ts` 165 + `featureCheck.ts` 10 + `signals.ts` 8 + 3 stubs); CCB = 970 LOC. 368-LOC delta is `intentNormalize.ts` (149 LOC CJK, **user-rejected per §8**) + thinned localSearch/prefetch (-191 LOC, no CJK tokenizer hooks, no skill-gap recording) + 3 CCB stub files (also stubs). Functional parity on TF-IDF index + prefetch surface. **Row title renamed from "(semantic)" to "(TF-IDF)"** — neither CCB nor we use embeddings; both are TF-IDF + Porter-style stemmer + IDF + cosine. See `coffeegrind123/openclaude:context/skills-deepdive.md`. |
| Skill Learning service | ✅ | ❌ | ✅ | §16 deep-dive: ported §9 commit `0e37443`. Ours `services/skillLearning/` = 4643 LOC across 21 files; CCB = 4637. **20 of 21 files are byte-identical** (`diff -r --brief`). Only `featureCheck.ts` differs (+6 LOC, default-on adapt mirroring `isCodeGraphEnabled()` / `isKairosEnabled()` — necessary because `bun:bundle` DCE strips `feature('SKILL_LEARNING')` to false in source-mode). CCB also ships a `__tests__/` directory we don't (per fork convention "port source, leave tests"). |
| Bundled browser-automation skill | ✅ | ✅ | ✅ | §16 deep-dive: Gitlawb's `bundled/claudeInChrome.ts` is **byte-identical to CCB's** (34 LOC, `diff` returns zero bytes). Three-way functionally equivalent; ours uses zendriver-mcp (registered via `browserAutomation.ts`), CCB+Gitlawb use Anthropic's `@ant/claude-for-chrome-mcp`. Architecturally divergent but row-level parity. |
| Bundled ghidra-re skill | ❌ | ❌ | ✅ | Our unique. |
| Bundled `/dream` skill | ✅ | ✅ | ✅ | — |
| Bundled `/hunter` skill | ❌ | ❌ | ⚠️ | §16 deep-dive: no `.ts` source in CCB or Gitlawb trees — only the feature-gated `require('./hunter.js')` line in `bundled/index.ts`. Ours has 1-LOC stub `.ts` so the require resolves to a no-op handler. CCB previously ⚠️ overstated. |
| Bundled `/runSkillGenerator` | ❌ | ❌ | ⚠️ | §16 deep-dive: same shape as `/hunter` — paired feature-gated companion. No source in CCB or Gitlawb; ours has 1-LOC stub. |
| Bundled `/code-graph` skills (7 docs) | ❌ | ❌ | ✅ | Our unique: build-graph, review-pr, review-delta, review-changes, debug-issue, explore-codebase, refactor-safely. |
| Teach-Me skill | ✅ | ❌ | ✅ | §16 deep-dive: NOT a phantom (initial recon was wrong). Markdown skill at `.claude/skills/teach-me/SKILL.md` (368 LOC) + `references/pedagogy.md` (235 LOC) — Socratic-tutor pedagogy with diagnose/question/mastery-gate protocol. Ported as drop-in mini-port commit `64fbb97` — 603 LOC of pure markdown, byte-identical to CCB's. Uses our existing `AskUserQuestion` tool. |
| MCP Skills (skill:// URIs) | ✅ | ✅ | ✅ | — |

---

## 17. Infrastructure / Distribution / Platform

| Feature | CCB | Gitlawb | openclaude | Location / Notes |
|---|---|---|---|---|
| Runtime: Node | — | ✅ | — | Node ≥20. |
| Runtime: Bun | ✅ | ⚠️ | ✅ | CCB + ours Bun-compiled. Gitlawb Bun for source builds. |
| npm install (`@<scope>/openclaude`) | — | ✅ | — | — |
| GitHub Releases binary | ✅ | ❌ | ✅ | — |
| `curl bootstrap.sh | bash` install | ⚠️ | ❌ | ✅ | Our unique per convention. |
| Docker compose dev | — | ⚠️ | ✅ | Ours: `docker-compose.interactive.yml` |
| Docker image (GHCR public) | ✅ | ✅ | ❌ | (#656). |
| Android install (Termux + proot) | ❌ | ✅ | ❌ | `ANDROID_INSTALL.md`. |
| Homebrew / apt / etc. | ⚠️ | ⚠️ | ❌ | Auto-updater detects. |
| Release Please automation | ❌ | ✅ | ❌ | `.release-please-manifest.json`. |
| Auto-updater (multi-strategy) | ✅ | ✅ | ✅ | CCB: GCS native + npm + pkg mgr. Gitlawb: npm. Ours: GitHub Releases. |
| Keepmarketplace-on-failure env | ⚠️ | ✅ | ✅ | Backported 2.1.90. |
| `bun:bundle` shim / feature() override | ⚠️ | ✅ | ✅ | Gitlawb replaced shim with source pre-processing (#657). We force-enable all 87 via `node_modules/bundle/`. |
| 15+ additional feature flags open | ⚠️ | ✅ | ✅ | — |
| All 87 feature flags open | ❌ | ⚠️ | ✅ | Our unique. |
| `USER_TYPE=ant` always set | — | ❌ | ✅ | Our unique. |
| `CLAUDE_AUTO_TRUST=1` | — | ❌ | ✅ | Our unique. |
| Source pre-processing (no bun:bundle) | ❌ | ✅ | ❌ | Gitlawb-unique build strategy. |
| Fingerprinting (CCH body signing) | ⚠️ | ⚠️ | ✅ | Our xxHash64-based body signing `services/api/cchSigning.ts`. |
| CLIProxyAPI-mirrored constants | — | — | ✅ | Our unique. `config/claudeFingerprint.ts`. |
| Privacy verification (`verify:privacy`) | ❌ | ✅ | ⚠️ | `scripts/verify-no-phone-home.ts`. Our analytics stubs serve same goal. |
| PR intent scanner | — | ✅ | ❌ | `scripts/pr-intent-scan.ts`. |
| Smoke test | — | ✅ | ⚠️ | `bun run smoke`. |
| Coverage heatmap UI | — | ✅ | ❌ | `scripts/render-coverage-heatmap.ts`. |

---

## 17a. Native NAPI modules (platform-specific bindings)

CCB is the **only** fork shipping Node-native modules. All are in `packages/*-napi/`. These power features that would otherwise require a sidecar process (MCP) or be impossible in pure JS.

| Module | CCB | Gitlawb | ours | Purpose |
|---|---|---|---|---|
| `audio-capture-napi` | ✅ | ❌ | ❌ | Platform audio capture (system audio + mic) — Voice Mode foundation. Restored & operational. |
| `color-diff-napi` | ✅ | ❌ | ❌ | CIEDE2000 color distance — visual/pixel diff for image comparison. Complete + 11 tests. |
| `image-processor-napi` | ✅ | ❌ | ❌ | Image manipulation (resize, compress, filter) — backs screenshot / clipboard paste flows. Restored. |
| `modifiers-napi` | ⚠️ | ❌ | ❌ | Keyboard modifier state (Shift/Ctrl/Alt/Cmd detection). Stub per source audit. |
| `url-handler-napi` | ⚠️ | ❌ | ❌ | OS-level URL scheme registration (deep linking). Stub per source audit. |

Gitlawb's `src/native-ts/` directory (color-diff, file-index, yoga-layout) is **TypeScript re-implementations**, not native modules — a Node-no-native-build environment convenience. Ours uses stock Ink (with stock Yoga) and relies on `sharp` for image work.

## 17b. CCB-forked Anthropic `@ant/` packages

CCB ships a `packages/@ant/` namespace of forked / reimplemented Anthropic internals:

| Package | Purpose |
|---|---|
| `@ant/ink` | Forked Ink framework (components, hooks, keybindings, theme). Explains why their CLAUDE.md says "Ink is at packages/@ant/ink/, not src/ink/". |
| `@ant/computer-use-mcp` | Computer Use MCP server (cross-platform). |
| `@ant/computer-use-input` | Keyboard/mouse dispatcher + per-OS backends. |
| `@ant/computer-use-swift` | Screenshots + app management (macOS/Windows/Linux). |
| `@ant/claude-for-chrome-mcp` | Chrome browser control MCP (official extension integration). |
| `@ant/model-provider` | Model provider abstraction. |

Gitlawb and we rely on upstream Ink + external MCP servers for these. CCB's forked `@ant/` layer is a larger engineering investment but also a larger upstream-divergence debt.

## 17c. CCB auxiliary (non-workspace) packages

| Package | Purpose | Status in ours / Gitlawb |
|---|---|---|
| `packages/cc-knowledge/` | Claude Code knowledge base (likely doc/snippet store) | ❌ / ❌ |
| `packages/langfuse-dashboard/` | Langfuse observability panel | ❌ / ❌ |
| `packages/mcp-server/` | MCP server library (non-workspace) | ❌ / ❌ (we depend on @modelcontextprotocol/sdk) |
| `packages/shell/` | Shell abstraction (non-workspace) | — / — |
| `packages/swarm/` | Agent swarm logic (non-workspace) | — / — |
| `packages/weixin/` | WeChat integration | ❌ / ❌ |
| `packages/acp-link/` | ACP WebSocket → stdio bridge (Hono + Pino) | — (we ported, native Bun.serve) / ❌ |
| `packages/agent-tools/` | Agent tool Zod schemas | — / — |
| `packages/mcp-client/` | MCP client library | — / — |
| `packages/remote-control-server/` | RCS Web UI (React 19 + Vite + Radix + Tailwind + Shiki + QR code auth) | ❌ / ❌ |
| `packages/builtin-tools/` | 59 built-in tool implementations | — / — |

---

## 18. Feature notices (startup UX)

| Notice | CCB | Gitlawb | openclaude | Location / Notes |
|---|---|---|---|---|
| Component-based startup notices (N sessions) | ⚠️ | ⚠️ | ✅ | Our convention: each major feature ships `src/components/LogoV2/XxxNotice.tsx`. |
| Opus 1M merge notice | ⚠️ | ✅ | ⚠️ | Upstream. |
| Ghidra MCP notice | — | — | ✅ | Our unique. |
| Browser MCP notice | — | — | ✅ | Our unique. |
| `/super` mode notice | — | — | ✅ | Our unique. |
| Multi-provider API notice | — | ✅ | ✅ | — |
| NVIDIA NIM native notice | — | — | ✅ | Our unique. |
| Computer Use MCP notice | — | — | ✅ | Our unique. |
| Upstream backports notice | — | — | ✅ | Our unique. |
| Proactive notice | ⚠️ | ⚠️ | ✅ | — |
| KAIROS notice | ⚠️ | ⚠️ | ✅ | — |
| Voice local notice | — | — | ✅ | Our unique. |
| LAN pipes notice | ⚠️ | — | ✅ | — |
| Observe tracing notice | — | — | ✅ | — |
| `/buddy` command notice | ⚠️ | ⚠️ | ✅ | — |
| Distill notice | — | — | ✅ | — |
| Emacs integration notice | — | — | ✅ | — |
| Fuelgauge status line notice | — | — | ✅ | — |
| SSH Remote notice | ⚠️ | — | ✅ | — |
| ACP (Zed/Cursor) notice | ⚠️ | — | ✅ | — |
| acp-link notice | ⚠️ | — | ✅ | — |
| Away summary notice | — | — | ✅ | `AwaySummaryNotice.tsx`, 4 sessions. |
| CodeGraph notice | — | — | ✅ | — |

---

## 19. Unique-to-openclaude (our fork only)

Mirror / symmetry section — features shipped only by us. **Note:** after the CCB source re-inventory, several items previously listed here were moved out because CCB also ships them (ACP, acp-link, SSH, LAN/UDS pipes, environment-runner, self-hosted runner, `/force-snip`, `/subscribe-pr`, `/init-verifiers`, `/fork`, daemon command hierarchy). What remains is genuinely ours-only:

- **Code knowledge graph** (`src/services/codeGraph/` + `CodeGraphTool` + `/graph`) — 28 operations, 23+ languages, SQLite + FTS5 + Louvain communities, auto-update on file edits, cross-repo registry, wiki generation
- **Distill output compaction** (`src/services/distill/`) — 59 embedded filters + arg injection + sidecar JSONL analytics
- **ACP (Zed/Cursor)** — ported from CCB as pure-TS reimplementation (CCB also ships ACP at `src/acp/` — we're at parity)
- **acp-link WebSocket bridge** — ported from CCB with Bun.serve native WebSocket (drops CCB's hono+ws+pino stack that lives at `packages/acp-link/`)
- **SSH Remote** backend — ported with two CCB bug fixes (`ANTHROPIC_AUTH_SOCKET`→`ANTHROPIC_UNIX_SOCKET`, `waitForInit` deadlock). CCB has parity at `src/ssh/`.
- **LAN Pipes + UDS pipes** (both CCB and ours; different wiring). CCB has `utils/{pipeTransport,lanBeacon,pipeRegistry,pipePermissionRelay,pipeMuteState,pipeStatus}.ts` — parity.
- **Fuelgauge native status line** — port of adityaarakeri/fuelgauge, Ink-native; 5h/7d bars only on first-party Anthropic
- **Observe tracing** — OTel + custom dashboard at `coffeegrind123/openclaude-observe` (SQLite + React, port 4981)
- **Emacs integration** — transient menu shim over `claude-code-ide.el`, bound to `C-c o o`; podman-friendly boundary (host port forwarding + lockfile bind mount)
- **Ghidra MCP** — full JDK + Ghidra + GhidraMCP + bridge auto-install stack
- **Zendriver browser MCP** — auto-installed from our fork repo
- **Computer Use MCP (domdomegg npx)** — sidesteps upstream Swift-loader stub mess
- **NVIDIA NIM auto-catalog** — 130-entry, auto-regenerated, `max_input_tokens` + `max_output_tokens` from litellm pricing DB
- **z.ai RPM throttling** — zero-config sliding-window limiter, `customerId` auto-discovery via `/api/biz/subscription/list`, plan-inferred `modelCode` routing
- **Reactive Compact + PTL recovery** — pivot-based partial compact on `prompt_too_long`, forced-fallback path
- **CCH body signing** — xxHash64 integrity hash
- **KAIROS full wiring** — CCB's KAIROS concept, our implementation with autoDream 3-gate trigger + `/dream` skill
- **Low-context mode** (`utils/lowContextMode.ts`) — DeepSeek auto-optimization, trims system prompt ~60% (10K→4K tokens)
- **Native tool deferral on non-Anthropic providers** — MCP ToolSearchTool works on z.ai/DeepSeek/etc. via text markers instead of `tool_reference` blocks
- **Team memory GitHub backend** — `TEAMMEM_GITHUB_REPO=owner/repo`; provider-agnostic (z.ai/DeepSeek/NIM all work, not just Claude.ai OAuth)
- **Daemon (tmux) mode + templates/jobs** — `claude daemon start/stop/status/restart`, `claude new <template>`
- **Local CCR server** — full ~20-endpoint Anthropic CCR API (v1 + v2) in Bun
- **Environment runner + Self-hosted runner** — BYOC workers
- **Snip output compaction** (`services/compact/snipCompact.ts`) — fast truncation of old messages, no LLM
- **`/super` orchestrator** — phase tokens + swarmNudge fan-out detection
- **`/memory-import`, `/memory-export`, `/memory-cli`** — memory tooling
- **`/setup-bedrock`, `/setup-vertex`, `/edit-system-prompt`, `/recap`, `/focus`, `/tui`, `/torch`, `/init-verifiers`, `/submit`, `/ccr-server`** — niche commands
- **`/dump-prompt`** — full system prompt dumper (Gitlawb has similar `services/api/dumpPrompts.ts` internal; we expose as command)
- **Upstream backports table** — tracked in CLAUDE.md, dated, commit-linked
- **Fingerprinting constants** mirrored from CLIProxyAPI

---

## 20. Unique-to-Gitlawb (their fork only)

- **`/provider` wizard + `.openclaude-profile.json` saved profiles** — multi-provider session-level switching
- **Provider auto-detect / recommendation / benchmarking / validation** — `utils/provider*.ts` (10+ files)
- **gRPC headless server** + bidirectional-streaming protocol + test CLI client
- **Bundled VS Code extension** (`vscode-extension/openclaude-vscode/`) — 10 commands, control center, chat UI
- **Gemini native** with `thought_signature` fix
- **GitHub Models onboarding** — `/onboard-github`
- **Codex OAuth (ChatGPT sign-in)** + Codex CLI credential reuse
- **GitHub Copilot native Anthropic mode** — Claude via Copilot subscription
- **Ollama `ollama launch openclaude` shim** — zero-config local Ollama boot
- **Atomic Chat, Alibaba DashScope, MiniMax providers** — three extra OpenAI-compatible endpoints with discovery
- **Smart model routing** (`services/api/smartModelRouting.ts`) — cheap-for-simple, strong-for-hard auto-route
- **Thinking token extraction** for 3P `<think>` tags
- **Thinking-tag sanitizer**
- **Small-context tool_result compression** (`services/api/compressToolHistory.ts`)
- **Model caching + benchmarking** (`utils/model/modelCache.ts` + `benchmark.ts`)
- **Agent routing** (per-agent model via settings.json `agentRouting`/`agentModels`)
- **DuckDuckGo + Firecrawl WebSearch** (no key fallback + optional API key)
- **Bing + Brave HTML scrape adapters** + `WEB_URL_TEMPLATE` custom search
- **AutoFix service** — auto-lint+test after AI edits, hook-based
- **Hook Chains** — event-driven recovery DSL (spawn_fallback_agent / notify_team / warm_remote_capacity) with depth guard + cooldown + dedup
- **`doctor:runtime` + `doctor:runtime:json` + `doctor:report`** — structured runtime diagnostics
- **`/cache-probe`** diagnostic
- **Wiki service** (`services/wiki/` 8 files: index builder, ingestion, status) + `/wiki` command
- **Vim keybindings engine** (`src/vim/` motions/operators/textObjects/transitions/types) — note: ours has this too per audit verification; CCB doesn't
- **Local feature-flag overrides** (`~/.claude/feature-flags.json`)
- **`allowBypassPermissionsMode` setting**
- **15 additional feature flags enabled in open build**
- **`bun:bundle` source pre-processing** (alternative to our shim)
- **Strict MCP tool schema normalization with opt-out** (`OPENCLAUDE_DISABLE_STRICT_TOOLS`)
- **Android/Termux install path**
- **Release Please automation**
- **Coverage heatmap UI** (`scripts/render-coverage-heatmap.ts`)
- **`security:pr-scan` + `verify:privacy` scripts**
- **Datadog + Perfetto exporters**
- **Native TS modules** (`src/native-ts/` color-diff, file-index, yoga-layout subdirs) — strips native deps for Node-no-native-build environments

---

## 21. Unique-to-CCB (their fork only — source-verified)

### Native / foundational capabilities
- **5 native NAPI modules** — `audio-capture-napi` (operational, Voice foundation), `color-diff-napi` (CIEDE2000 complete + tests), `image-processor-napi` (operational), `modifiers-napi` (stub), `url-handler-napi` (stub). Neither Gitlawb nor we ship any NAPI modules.
- **`@ant/ink` forked Ink framework** — custom components, hooks, keybindings, theme system; explains CCB's own CLAUDE.md note that "Ink is at packages/@ant/ink/". We + Gitlawb use upstream Ink.
- **`@ant/computer-use-*` package trio** — MCP server + input dispatcher + Swift/Win/Linux screenshot backend, as separate workspace packages rather than a single MCP install script.
- **`@ant/claude-for-chrome-mcp`** — forked Chrome browser control MCP with official-extension integration.
- **`@ant/model-provider`** — model provider abstraction as a workspace package.

### Services / subsystems only in CCB
- **Real Skill Search** (`src/services/skillSearch/`, ~970 lines) — `localSearch.ts` (444), `prefetch.ts` (328), `intentNormalize.ts` (149). We + Gitlawb do not ship real skill search.
- **Skill Learning service** (`src/services/skillLearning/`).
- **Langfuse observability** (`src/services/langfuse/` + `packages/langfuse-dashboard/` + `@langfuse/otel` + `@langfuse/tracing`).
- **Autonomy subsystem** — `utils/autonomy{Authority,CommandSpec,Flows,Persistence,Runs,Status}.ts` (6 files) + `commands/autonomy.ts` + `autonomyPanel.tsx`. Tracks automatic autonomy runs for proactive ticks + scheduled tasks; sub-args `status/runs/flows/flow/flow cancel/flow resume`.
- **VCR (record/replay)** — `src/services/vcr.ts`.
- **Teach-Me skill** — Socratic Q&A learning system (atom-sized concept trees, diagnostic profiling, error tracking, session resumption).
- **Session transcript** (`src/services/sessionTranscript/`) — dedicated service we fold into compact.

### Commands only in CCB
- **`/autonomy`** — inspect autonomy runs (proactive + scheduled).
- **`/lang`** — language/locale switcher.
- **`/poor` + poorMode** — reduced-resource mode.
- **`/skill-search`, `/skill-learning`** — paired with real services above.
- **`/history`**, **`/job`**, **`/monitor`** — additional command surfaces we/Gitlawb lack.
- **`/debug`** — Bun inspect attach.

### Distribution / Infrastructure
- **Self-hosted RCS with React 19 Web UI** — `packages/remote-control-server/` = Hono backend + React 19 + Vite + Radix UI + Tailwind + Shiki + QR code auth. Our `src/ccr-server/` is the API surface only; no UI.
- **Three-tier feature gating** (compile-time + GrowthBook + env) — conceptual vs our all-forced.
- **Bridge Mode v1+v2** with workSecret + trusted devices.
- **Chrome extension** (official Claude Pro+) — separate from chrome-use-mcp.
- **Cross-platform Computer Use Windows-specific extras** — PrintWindow, UIA, Windows.Media.Ocr, PostMessage/SendMessage background input.
- **Lodestone deep linking** (URL protocol handler registration at OS level).
- **Sentry integration** (optional).
- **`cc-knowledge` package** — Claude Code knowledge base.
- **WeChat/Weixin native package** (`packages/weixin/`) — integration beyond the generic channel notification layer.

### Provider support
- **Grok (xAI) native** — `src/services/api/grok/` (client + index + tests). Not in Gitlawb or ours.
- **Gemini native** — `src/services/api/gemini/` (Gitlawb also has via utils; we have neither).

### Parity with ours (previously misclassified)
- **SSH Remote backend**, **BYOC environment-runner**, **Self-hosted runner**, **Multi-instance pipe commands** (`/attach`/`/detach`/`/claim-main`/`/peers`/`/pipe-status`/`/pipes`/`/send`), **`/force-snip`**, **`/subscribe-pr`**, **`/init-verifiers`**, **`/fork`**, **`/daemon` command hierarchy** — all shipped in both CCB source and ours. Prior audit wrongly called several of these "ours unique" based on docs-only CCB coverage.

---

## 22. Prioritized backport backlog

Ranked by user-visible value × effort ratio. Source repo cited per item.

### Tier 1 — high value, real gap, feasible

1. **DuckDuckGo WebSearch fallback** — Gitlawb. Biggest functional hole in our non-Anthropic UX (z.ai/DeepSeek/NIM users have no web search today). `duck-duck-scrape` dep + minimal adapter. **Effort: 1 day.**
2. **Firecrawl WebFetch + WebSearch** — Gitlawb. Drop-in upgrade path for users with a Firecrawl key; JS-rendered sites work. `@mendable/firecrawl-js`. **Effort: 1 day.**
3. **`/provider` wizard + `.openclaude-profile.json`** — Gitlawb (`src/commands/provider/provider.tsx` + `utils/providerProfile.ts` + `providerStartupOverrides.ts`). Flip providers mid-session. **Effort: 2–3 days.**
4. **AutoFix service** — Gitlawb (`services/autoFix/autoFixHook.ts` + `autoFixRunner.ts` #508). Closes the agent edit→validate loop. **Effort: 3–4 days.**
5. **Hook Chains (self-healing DSL)** — Gitlawb (`utils/hookChains.ts`, `docs/hook-chains.md`). Spawns fallback agents / notifies team / warms remote capacity on PostToolUseFailure / TaskCompleted. Slots into our existing hook infrastructure. **Effort: 4–5 days.**
6. **Gemini native** (with `thought_signature` fix) — Gitlawb. Unblocks a whole provider family. `utils/geminiAuth.ts` + `geminiCredentials.ts`. **Effort: 2–3 days.**

### Tier 2 — polish / parity

7. **`/cache-probe` diagnostic** — Gitlawb. Easy cache hit/miss inspector. **Effort: 0.5 day.**
8. **`doctor:runtime` structured diagnostics script + `doctor:report` JSON output** — Gitlawb. Support-triage win. **Effort: 1 day.**
9. **Smart model routing (cheap/hard)** — Gitlawb. Good for DeepSeek-V4-Flash ↔ DeepSeek-V4-Pro. **Effort: 2 days.**
10. **Thinking-tag sanitizer + 3P thinking token extraction** — Gitlawb. Cleans DeepSeek/Qwen-reasoner noise. **Effort: 1 day.**
11. **Codex OAuth (ChatGPT sign-in)** — Gitlawb. Opens Codex to our users. **Effort: 2–3 days.**
12. **GitHub Models onboarding (`/onboard-github`)** — Gitlawb. **Effort: 1–2 days.**
13. **Ollama `ollama launch openclaude` shim** — Gitlawb. Zero-config local inference. **Effort: 1 day.**
14. **Agent routing** (per-agent model via settings.json) — Gitlawb. Long-standing ask. **Effort: 1–2 days.**
15. **Local feature-flag override file** (`~/.claude/feature-flags.json`) — Gitlawb. Lets users disable individual flags without rebuild. **Effort: 0.5 day.**
16. **Windows Computer Use enhancements** — CCB. `PrintWindow`, UIA tree, `Windows.Media.Ocr`, `PostMessage`/`SendMessage` background input. Real value for Windows automation users. **Effort: 1–2 weeks (Win32 companion native module).**
17. **Langfuse OTLP exporter** — CCB. Add `@langfuse/otel` as alternate OTel target. CCB ships `packages/langfuse-dashboard/` as the UI. **Effort: 1–2 days (exporter only, no UI).**
18. **Teach-Me skill** — CCB. Socratic Q&A learning for project modules; diagnostic profiling, atom-sized concept trees. **Effort: 4–5 days.**
19. **Real Skill Search** — CCB (`services/skillSearch/` ~970 lines: `localSearch.ts` + `prefetch.ts` + `intentNormalize.ts`). Our current 20-line stubs are already wired but do nothing. Porting would activate the existing call sites (`commands.ts:118`, `AttachmentMessage.tsx:44/108`, `prompts.ts:110/352/924`, `query.ts:70`, `compact.ts:215`). **Effort: 3–4 days.**
20. **Autonomy subsystem** — CCB (`utils/autonomy{Authority,CommandSpec,Flows,Persistence,Runs,Status}.ts` + `commands/autonomy.ts` + `autonomyPanel.tsx`). Persists + inspects proactive + cron autonomy runs — `status/runs/flows/flow/flow cancel/flow resume`. Pairs with our `/super` / proactive tick loop; would give users a visibility surface we currently lack. **Effort: 3–4 days.**
21. ~~**Small-context tool_result compression**~~ — **DONE 2026-04-24.** Ported as `src/services/api/compressToolHistory.ts`; wired into `openaiBridge` translator. Gated on new `toolHistoryCompressionEnabled` setting (default-off). See deep-dive Tier 3 #6.
22. **Bing + Brave HTML scrape adapters** (tier after DuckDuckGo/Firecrawl) — Gitlawb. **Effort: 2–3 days.**
23. **RCS React Web UI** — CCB. `packages/remote-control-server/` = Hono backend + React 19 + Vite + Radix UI + Tailwind + Shiki + QR code auth. Turns our headless CCR server into a real self-hosted control panel. **Effort: 2–3 weeks.**
24. **Grok (xAI) native** — CCB (`services/api/grok/`). Low-effort, drops into our NIM bridge provider framework. **Effort: 1 day.**
25. **Native NAPI audio-capture** — CCB. Replace our Python faster-whisper sidecar with native audio capture + local whisper. Bigger lift but removes a dependency. **Effort: 2 weeks.**

### Tier 3 — skip or defer

- **gRPC server** — we have ACP + local CCR + daemon; gRPC would be a 4th headless transport.
- **VS Code extension** — big commitment, stock Claude Code IDE integration works.
- **Android install** — out of scope for our in-container / binary-first model.
- **Alibaba DashScope, Atomic Chat, MiniMax providers** — one-file additions in `services/api/openaiBridge/providers/` on demand.
- **GitHub Copilot native Anthropic mode** — requires Copilot subscription probe; edge case.
- **VCR replay / rate-limit mocking** — Gitlawb-internal test infra.
- **Sentry** — conflicts with our telemetry-neutralization fork mission.
- **RCS React UI** — substantial UI work; we ship CCR server without UI.
- **Bundled VS Code control center** — part of extension work above.
- **Debug mode (Bun inspect attach)** — niche; CCB-only.
- **Native TS modules (yoga-layout etc.)** — only matters if we move off Bun-compiled binary.
- **Experimental Skill Search** — symmetric stub on all three forks; skip.
- **Bash classifier** — symmetric stub (we all have functional `yoloClassifier.ts`; only the Anthropic-internal `bashClassifier.ts` is stub everywhere).

---

## 23. Key takeaway

**Three real functional gaps in ours, all in one area: web access for non-Anthropic users.** DuckDuckGo + Firecrawl + (later) Bing/Brave close this in 2–3 days of work. Currently z.ai/DeepSeek/NIM users have no WebSearch at all (we commented out upstream and only have zendriver for navigation).

**Next-biggest UX win: `/provider` wizard + saved profiles** (2–3 days). Our env-var-only setup is more brittle than Gitlawb's saved-profile flow for users who toggle between z.ai / DeepSeek / Anthropic.

**Medium-term: AutoFix service + Hook Chains** — these two close the "agent writes code → something breaks → nothing happens" loop. Both slot cleanly into existing hook infrastructure.

**CCB-side (after source re-inventory):** the real backport candidates are **Real Skill Search** (they have 970 lines; we have 20 line stubs on existing call sites — activate the wiring), **Autonomy subsystem** (pairs with our `/super` + proactive tick loop), **Langfuse exporter**, **Windows Computer Use enhancements**, and **Grok native**. Skip the `@ant/*` forked package layer (ink, computer-use, chrome) — too much upstream-divergence debt — and skip the RCS React UI unless there's user demand.

**Recommended starting point:** DuckDuckGo WebSearch fallback (Tier 1 #1). Smallest effort, largest unblock.

---

## 24. Audit changelog

- **2026-04-25 (§16 Skills deep-dive + Teach-Me mini-port shipped — 7 cell flips across 6 rows + 1 row rename)** — Source-level pass on §16 Skills. Re-verified `services/skillSearch/`, `services/skillLearning/`, `skills/bundled/index.ts`, `skills/bundledSkills.ts`, `skills/loadSkillsDir.ts`, and `.claude/skills/` across all three forks. **§16 is dominated by post-§9 audit hygiene** — most "ours-is-behind" cells were stale because §9 commit `0e37443` shipped the two largest CCB Skills services at near-byte parity. Six audit-correction flips landed plus one user-greenlit Tier-3 mini-port (Teach-Me skill, commit `64fbb97`). (1) **Experimental Skill Search ours `⚠️ → ✅` + row rename "(semantic) → (TF-IDF)"** — post-§9 parity confirmed: ours `services/skillSearch/` = 602 LOC across 7 files vs CCB's 970 LOC across 8. 368-LOC delta breakdown: `intentNormalize.ts` (149 LOC CJK, **user-rejected per §8**, don't reopen) + thinned `localSearch.ts` (-28 LOC, CJK-aware tokenizer hooks dropped) + thinned `prefetch.ts` (-163 LOC, no skill-gap recording / no auto-load enrichment per CLAUDE.md) + 3 CCB stub files (`remoteSkillLoader.ts` 17 / `remoteSkillState.ts` 3 / `telemetry.ts` 11 — all explicitly labeled `// Auto-generated stub — replace with real implementation`, ours has at 1-LOC each). Functional parity on the actual TF-IDF index + prefetch surface. Row title "(semantic)" was misleading — neither CCB nor we use embeddings; both are TF-IDF + Porter-style stemmer + IDF + cosine. Renamed to "(TF-IDF)" to match the actual algorithm. (2) **Skill Learning service ours `❌ → ✅`** — ported §9 commit `0e37443`. Ours `services/skillLearning/` = 4643 LOC across 21 files; CCB = 4637. **20 of 21 files are byte-identical** (`diff -r --brief`). Only `featureCheck.ts` differs (CCB 12 LOC → ours 18 LOC = +6 LOC default-on adapt mirroring `isCodeGraphEnabled()`/`isKairosEnabled()` — necessary because `bun:bundle` DCE strips `feature('SKILL_LEARNING')` to false in source-mode). CCB also ships `__tests__/` we don't (per fork convention "port source, leave tests"). (3) **Remote skill discovery CCB `✅ → ⚠️`** — CCB's `remoteSkillLoader.ts` (17 LOC) + `remoteSkillState.ts` (3 LOC) + `telemetry.ts` (11 LOC) are explicitly auto-generated stubs returning no-ops. The actual fetch+parse+cache logic does not exist in CCB's source tree. Three-way `⚠️ ⚠️ ⚠️` is the honest classification — all three forks ship stub-shaped placeholders. CCB previously `✅` was paper-knowledge. (4) **Bundled `/hunter` CCB `⚠️ → ❌`** — CCB's `bundled/index.ts:43` has `if (feature('REVIEW_ARTIFACT')) { require('./hunter.js') }` but the `.ts` file does not exist in CCB or Gitlawb source trees (verified via `command grep -rln "registerHunterSkill" /tmp/ccb-docs/` — the only hit is `bundled/index.ts` itself). Ours has a 1-LOC stub `.ts` so the require resolves to a no-op handler — most honest as `⚠️` (registration succeeds, no-op behavior). CCB's `⚠️` was overstated. (5) **Bundled `/runSkillGenerator` CCB `⚠️ → ❌`** — same shape as `/hunter`, paired feature-gated companion. Same missing `.ts` in CCB+Gitlawb, same 1-LOC stub in ours. (6) **Bundled browser-automation Gitlawb `⚠️ → ✅`** — Gitlawb's `bundled/claudeInChrome.ts` is **byte-identical to CCB's** (`diff` returns zero bytes; both 34 LOC). Both register `claude-in-chrome` skill with `BROWSER_TOOLS`/`BASE_CHROME_PROMPT`/`shouldAutoEnableClaudeInChrome()` gate. Gitlawb's `⚠️` was wrong. Three-way `✅ ✅ ✅`. Annotation: ours uses zendriver-mcp (registered via `browserAutomation.ts`), CCB+Gitlawb use Anthropic's `@ant/claude-for-chrome-mcp` — architecturally divergent, row-level parity. (7) **Teach-Me skill ours `❌ → ✅`** — initially expected to be a phantom-row per the §15 protocol (kickoff said "if grep returns empty, flip CCB to ❌"). Recon revealed Teach-Me is **NOT a phantom** — it lives at `/tmp/ccb-docs/.claude/skills/teach-me/SKILL.md` (368 LOC) + `references/pedagogy.md` (235 LOC) as a markdown skill, not a TypeScript module under `src/skills/bundled/`. The kickoff's `grep /tmp/ccb-docs/src/` was looking in the wrong directory. Mini-port shipped at commit `64fbb97`: drop-in copy of CCB's `.claude/skills/teach-me/` into our repo (byte-identical, 603 LOC of pure markdown, no TypeScript). `.gitignore` tweak `.claude/` → `.claude/*` + negation rules `!.claude/skills/` and `!.claude/skills/**` so bundled-as-markdown skills can ship in source while user-level state under `.claude/` stays ignored. Skill is a Socratic tutor: diagnoses level, builds learning path, teaches via guided questions with `AskUserQuestion`, persists state under `.claude/skills/teach-me/records/{topic-slug}/`. Loaded at runtime via `loadSkillsDir.ts`'s `getSkillsPath('projectSettings', 'skills')` → `.claude/skills` relative to cwd. **Hunter / runSkillGenerator port** declined — no source exists in any fork to port from; would be green-field implementation, not a port. CCB's distributed cli.js is not in `/tmp/ccb-docs/` (clone is source-only). **Remote skill discovery port** declined — same green-field situation; if user wants real remote-fetch later it's a fresh ~50-100 LOC implementation against any fork. **Net**: 6 audit-correction flips + 1 row rename + 1 ours flip from the mini-port = 7 column changes total. Closer in shape to §11 (column-flip-heavy hygiene) than §15 (Tier-2 ports). Full per-row analysis at `coffeegrind123/openclaude:context/skills-deepdive.md`.

- **2026-04-25 (§15 adapts shipped: Hook Chains + AutoFix from Gitlawb — 4 ours-column flips)** — Same-day follow-up on the §15 deep-dive: both Tier-2/Tier-3 adapt candidates greenlit and shipped. **(1) Hook Chains** (commit `9c4cb7e`, 2121 insertions across 11 files): ported `src/utils/hookChains.ts` 1518 LOC verbatim from Gitlawb (zero path adjustments — all 14 dependency imports line up at identical paths in our tree: `agentSdkTypes.js` re-exports `HOOK_EVENTS` from `coreTypes.js`, `bootstrap/state.js`, `services/{analytics,policyLimits}/index.js`, `utils/{debug,diagLogs,envUtils,errors,fileRead,json,teammate,teammateMailbox}.js`, `utils/swarm/teamHelpers.js`, `utils/telemetry/events.js` — all present byte-compatibly). 333 LOC `docs/hook-chains.md` ported verbatim. Integration: `hooks.ts` +203 LOC (`dispatchHookChainFromHookRuntime` + `launchFallbackAgentFromHookChains` + `normalizeFallbackAgentModel` helpers; refactored `executePostToolUseFailureHooks` early-return to flag-based + dispatch unconditionally; refactored `executeTaskCompletedHooks` to track `blockingHookCount`/`preventedContinuation` + dispatch with computed outcome). `Tool.ts:252` extends `ToolUseContext` with `hookChainsCanUseTool?: CanUseToolFn`. `services/tools/toolExecution.ts:1257` injects on every `tool.call(...)`; `:1788` re-injects in PostToolUseFailure path with `try/finally` cleanup. Two gates: `feature('HOOK_CHAINS')` added to `bundle` polyfill + `bun-bundle-runtime.ts` + `bun-bundle-preload.ts` (all three) AND env var `CLAUDE_CODE_ENABLE_HOOK_CHAINS=1` (defaults disabled). `feature` import from `'bundle'` (runtime eval, NOT `bun:bundle` DCE). Three actions all have working backing infra: `spawn_fallback_agent` wired through `onSpawnFallbackAgent` callback launching `AgentTool`; `notify_team` uses built-in `writeToMailbox` fallback (no callback wiring needed); `warm_remote_capacity` uses built-in `getReplBridgeHandle` + RCS `teleport/environments.ts` fallback. Live-verified end-to-end: `dispatchHookChainsForEvent({eventName:"TaskCompleted",...})` against sample `notify_team` rule returns `{enabled:true, evaluatedRuleCount:1, matchedRuleIds:["test-rule"], actionResults:[{status:"skipped", reason:"No team context is available"}]}` — full pipeline (config load + zod parse + rule match + action handler + structured-skip safety guard) verified. Notice: `HookChainsNotice.tsx`. **(2) AutoFix** (commit `7ff1396`, 408 insertions across 11 files): ported `src/services/autoFix/{autoFixConfig.ts(52), autoFixHook.ts(28), autoFixRunner.ts(186)}` verbatim from Gitlawb (one tool-name change: `AUTO_FIX_TOOLS` Set extended from `['file_edit','file_write']` to add `['Edit','Write']` since ours uses upstream Anthropic PascalCase — both kept for migration). Slash command `/auto-fix` (25-LOC verbatim) returns LLM prompt walking the user through `.claude/settings.json` config. Wired into `services/tools/toolHooks.ts` `runPostToolUseHooks` +66 LOC (after for-loop's PostToolUse hooks finish, before outer catch): reads `toolUseContext.getAppState().settings.autoFix`, runs `runAutoFixCheck({lint, test, timeout, cwd, signal})` which spawns shell with timeout + abort + tree-kill (Win `taskkill /T /F` + Unix `process.kill(-pgid, 'SIGTERM')`); on errors emits `<auto_fix_feedback>` content block via `createAttachmentMessage({type:'hook_additional_context', hookName:'AutoFix:<tool>', hookEvent:'PostToolUse'})`. Per-conversation `autoFixRetryCount` Map keyed by `queryTracking.chainId`, capped at `maxRetries` (default 3). Settings schema field added at `utils/settings/types.ts:435` next to `hooks` field. **Opt-in, OFF by default** — requires `settings.autoFix.enabled: true` AND at least one of `lint`/`test` (zod `.refine` rejects `enabled: true` without either). Live-verified end-to-end: `getAutoFixConfig` parses sample OK; `shouldRunAutoFix('Edit', cfg)` true / `('Bash', cfg)` false; `runAutoFixCheck` against `echo lint-ok` → `hasErrors: false`; against `sh -c "echo lint-error >&2; exit 1"` → `hasErrors: true, errorSummary:"Lint errors (exit code 1):\nlint-error"`; `buildAutoFixContext` produces correct `<auto_fix_feedback>` block. Notice: `AutoFixNotice.tsx`. **Row flips:** Hook Chains ours `❌ → ✅`; AutoFix service ours `❌ → ✅`; Auto-fix hook integration ours `❌ → ✅`; PostToolUseFailure dispatch ours `❌ → ✅`. 4 ours-column flips closing the entire §15 Tier-2/Tier-3 adapt-decision surface from the deep-dive.

- **2026-04-25 (§15 Hooks / Self-Healing deep-dive — 8 cell flips across 6 rows)** — Source-level pass on §15 Hooks / Self-Healing / Automation. Re-verified hooks.ts, stopHooks.ts, hookChains.ts, autoFix/, and 18 `provider*.ts` files across all three forks. **8 cell flips landed — significantly more than the kickoff's "5-6" estimate, primarily because the audit's `✅` marks for Gitlawb on the two 2.1.89-backport rows turned out to be paper-knowledge errors (Gitlawb does not ship those backports), and Provider self-healing #738 turns out to not exist as source in any fork (phantom citation).** (1) **Cleanup registry CCB `— → ✅`** — `cleanupRegistry.ts` is byte-identical 25 LOC across all three forks (`diff -q` shows zero bytes). CCB's `—` em-dash was paper-knowledge mistake. (2) **TaskCompleted hook CCB `❌ → ✅` + ours `⚠️ → ✅`** — `executeTaskCompletedHooks` async generator + `getTaskCompletedHookMessage` formatter are fully implemented in all three forks (CCB hooks.ts:3940/2063, Gitlawb 3953/2066, ours 4050/2045) and wired identically into stopHooks.ts. The "Hook Chains hook into this" annotation was wrongly gating the TaskCompleted row — that's a Hook Chains-row property only, not a TaskCompleted-event property. (3) **`defer` permission Gitlawb `✅ → ❌`** — Gitlawb's `permissionDecision` enum at hooks.ts:565,569,713 is exactly `"allow"|"deny"|"ask"`, no `defer` value. CCB also lacks `defer`. Only ours backports the 2.1.89 fix (hooks.ts:411,522,526,677). CCB stays at `⚠️` since the broader permissionDecision framework ships. (4) **Hook output >50K → disk Gitlawb `✅ → ❌`** — zero hits across all three patterns (`HOOK_OUTPUT_DISK_THRESHOLD`, `50_?000`, `output.length` + size threshold) in CCB or Gitlawb. Only ours has hooks.ts:452-460 spill-to-disk implementation. (5) **Provider self-healing Gitlawb `✅ → ❌`** — phantom citation. Zero hits for `selfHeal`/`self_heal`/`providerHealth`/`isProviderReady`/`readinessCheck` in `/tmp/gitlawb-oc/src/`. Read `providerStartupOverrides.ts`/`providerAutoDetect.ts`/`providerRecommendation.ts`/`providerProfile.ts` end-to-end + 14 other `provider*.ts` files; no retry/circuit-breaker/recover/heal logic anywhere. The audit cites issue #738; if the issue exists upstream in Gitlawb's GitHub it didn't ship as runtime source. Row is now `❌ ❌ ❌` across the board — recommend drop in next pass. **Two open Gitlawb-only adapt candidates surfaced** (no code shipped this session, deferred for user decision): **Hook Chains** (Tier-2, ~2000 LOC port + 6-12h, 1518-LOC core + 333-LOC docs + 3 backing-infra wirings — `spawn_fallback_agent` via our `forkSubagent`, `notify_team` via `teammateMailbox`, `warm_remote_capacity` via RCS bridge); **AutoFix service** (Tier-3, ~360 LOC port + 3-4h, conditional reframing as a Hook Chain ~2h if Hook Chains lands). Full per-row analysis + cost estimates + decision-blocker questions at `coffeegrind123/openclaude:context/hooks-self-healing-deepdive.md`.

- **2026-04-25 (§8 four-tool port: ours-column ⚠️→✅ on CtxInspect/TerminalCapture/ReviewArtifact/DiscoverSkills)** — Same-day follow-up on the §8 deep-dive: the four §8 tools the deep-dive surfaced as ours-stubs got ported. (1) **ReviewArtifactTool** — 142-LOC verbatim port from CCB packages at `src/tools/ReviewArtifactTool/ReviewArtifactTool.ts`; stateless emit of artifact + per-line annotations + severity to transcript. (2) **CtxInspectTool** — 122-LOC verbatim port from CCB packages at `src/tools/CtxInspectTool/CtxInspectTool.ts`; reports total tokens via `tokenCountWithEstimation()` + message count + caching/session-memory/collapse status. Required adding 5-LOC `getStats()` no-op to `services/contextCollapse/index.ts` (returns `{collapsedSpans:0, stagedSpans:0, collapsedMessages:0}` since contextCollapse stays stubbed). (3) **TerminalCaptureTool** — CCB's tool itself is a no-op stub returning empty content (TERMINAL_PANEL infra never shipped in CCB); ours implements a real version (~120 LOC) that taps MonitorTool's task buffer via `getTaskOutputPath(panel_id)` for the trailing-N-lines view, and `getRunningTasks(state).filter(isMonitorMcpTask)` for session enumeration when `panel_id` is omitted — annotated `(++)` because ours is functionally working where CCB's only ever returns empty data. (4) **DiscoverSkillsTool** — full TF-IDF infrastructure (~700 LOC across 5 files: 107 LOC tool + 16 LOC prompt + 444 LOC `services/skillSearch/localSearch.ts` index/searcher with light Porter-style stemmer + IDF + cosine similarity + name-match bonus + hyphen-split fallback + 161 LOC adapted `prefetch.ts` for assistant-turn auto-discovery + 10 LOC `signals.ts` `DiscoverySignal` type referenced by `attachments.ts:91` + updated `featureCheck.ts` with env-var override `SKILL_SEARCH_ENABLED=0|1`). **CJK / Chinese-language `intentNormalize.ts` infrastructure deliberately NOT ported** per user request — ASCII-only TF-IDF, no Haiku-driven Chinese-to-English query normalization layer. Live-verified end-to-end via `-p` mode against z.ai: `description="reverse engineering binary analysis"` → returned `ghidra-re` skill ranked at score 0.32 from the bundled-skills index. **Wiring pattern: direct imports + dual-fallback spread** (`import { X as XDirect } from './tools/X/X.js'` at module top + `CtxInspectTool ?? CtxInspectToolDirect` in registry array), following the `commands.ts:74-89` precedent from CLAUDE.md. Avoids the `feature() ? require : null` DCE trap that hides feature-gated tools when imported via `from 'bun:bundle'`, while keeping the rest of `tools.ts`'s feature gates untouched (no cascade risk to other tools' DCE'd branches). **Companion deliverable**: `coffeegrind123/openclaude:context/snip-tool-comparison.md` documents the SnipTool inspection (no port — comparison only): underlying `services/compact/snipCompact.ts` is byte-identical between CCB and ours, but CCB's prompt overpromises "compact summary" while shipping the same fast string truncation as ours; CCB exposes selective `message_ids` + `reason` input, ours uses empty schema. Recommendation: don't port CCB's selectivity (intentional UX call — `/compact` covers selective compression better). Notice: `DiscoverSkillsNotice.tsx`. **Row flips:** `CtxInspectTool` ours `⚠️ → ✅`; `TerminalCaptureTool` ours `⚠️ → ✅ (++)`; `ReviewArtifactTool` ours `⚠️ → ✅`; `DiscoverSkillsTool` ours `⚠️ → ✅`. Four ours-column flips closing the §8 stub-port backlog.
- **2026-04-25 (§8 source-level deep-dive + 26 column flips + 5 row additions)** — Source-level pass on §8 Tools (model-facing). Re-read every tool directory across all three forks: `/tmp/ccb-docs/packages/builtin-tools/src/tools/` (the real CCB tool location — the audit was originally `ls`'ing only `src/tools/`, missing CCB's split-package layout entirely), `/tmp/gitlawb-oc/src/tools/`, `/home/claudeuser/openclaude/src/tools/`. **Largest single-section correction count to date — 26 column flips across 21 rows + 5 entirely-missing rows added = 31 row-level changes.** Three classes of correction landed. (1) **18 CCB false-negatives flipped `—` → `✅`/`⚠️`** — `ListMcpResourcesTool` (178 LOC), `ReadMcpResourceTool` (218), `SendMessageTool` (1060), `RemoteTriggerTool` (308), `ScheduleCronTool` (552), `PowerShellTool` (10124 — heavyweight), `REPLTool` (174), `BriefTool` (614), `ConfigTool` (820), `SuggestBackgroundPRTool` (84 → ⚠️ paired with Gitlawb demotion), `ToolSearchTool` (593), `SyntheticOutputTool` (163), `TeamCreateTool` (360), `TeamDeleteTool` (265), `TungstenTool` (8 stub-shape → ⚠️ paired with Gitlawb demotion), `CtxInspectTool` (324), `OverflowTestTool` (3-LOC auto-generated stub → ⚠️), `TerminalCaptureTool` (83). Plus `ListPeersTool` `❌` → `✅` (CCB packages ships 107-LOC real `buildTool()` impl). (2) **Three Gitlawb demotions the kickoff didn't anticipate** — `SuggestBackgroundPRTool` Gitlawb `✅` → `⚠️` (3-LOC `// Stub\nexport default null\nexport const SuggestBackgroundPRTool = null` — file exists as null-export, same shape as ours), `TungstenTool` Gitlawb `✅` → `⚠️` (4-LOC null-export stub), `VerifyPlanExecutionTool` Gitlawb `❌` → `⚠️` (refinement — file exists at 3-LOC null-export, per audit's "file-exists-vs-truly-missing" convention should be `⚠️`). (3) **One ours flip + 5 row additions** — `SyntheticOutputTool` ours `❌` → `✅` (163 LOC at `src/tools/SyntheticOutputTool/SyntheticOutputTool.ts`, dynamic-injected at `main.tsx:1855` + `cli/print.ts:1544` after `getTools()` filtering for `--output-format=json` flow — registry-grep alone misses it). New rows: `DiscoverSkillsTool` `✅ ❌ ⚠️ (stub, prompt-only)`; `NativeAdvisorTool` `❌ ❌ ✅` (ours-unique 210-LOC advisor-executor surface, `sideQuery()`-bound); `ReviewArtifactTool` `✅ ❌ ⚠️ (stub, intentional via feature('REVIEW_ARTIFACT'))`; `SendUserFileTool` `✅ ❌ ⚠️ (stub, KAIROS-future — no file-delivery transport)`; `WebBrowserTool` `✅ ❌ ⚠️ (stub, deliberately disabled — replaced by zendriver-mcp)` — `tools.ts:121` hardcodes `const WebBrowserTool = null` with the require explicitly commented out (not feature-gated). **Stub-classification annotation pass** applied on 7 ours `⚠️` cells: `(ant-only intentional)` × 2, `(dev-only intentional)` × 3, `(future-feature stub)` × 2, `(deliberately-disabled, replaced by X)` × 1. **Adapt backlog: zero ports shipped.** Single Tier-3 candidate: `DiscoverSkillsTool` re-estimated at ~700 LOC (not the kickoff's 174) because `services/skillSearch/localSearch.ts` is a 1-LOC stub in our tree and the tool depends on the full TF-IDF index (444 LOC) + intentNormalize (149 LOC) infrastructure. Half-day to full-day port if user gives go; recommendation is skip unless concrete need surfaces (we've gone 6 months without users asking). All other ours `⚠️` cells are stay-stub by design (ant-only / dev-only / KAIROS-future / replaced). Closer in shape to §5 (0 adapts, 3 row corrections) than §7 (1 adapt + 14 flips) or §4 (1 adapt + 9 flips) — but with the highest correction count of any §-area to date. Full per-row analysis + cost re-estimate + decision-blocker question at `coffeegrind123/openclaude:context/tools-model-facing-deepdive.md`.
- **2026-04-25 (§7 Tier-2 adapt shipped: MCP doctor)** — Ported Gitlawb's `services/mcp/doctor.ts` (695 LOC) verbatim plus `commands/mcp/doctorCommand.ts` (25 LOC) verbatim plus `formatDoctorReport()` + `mcpDoctorHandler()` (~120 LOC inserted into our existing `cli/handlers/mcp.tsx`) plus 2-line wiring in `main.tsx` (`registerMcpDoctorCommand` import + call). All `services/mcp/` deps (`getAllMcpConfigs`, `getMcpConfigsByScope`, `isMcpServerDisabled`, `connectToServer`, `clearServerCache`, `describeMcpConfigFilePath`, `getProjectMcpServerStatus`) line up byte-for-byte with Gitlawb's; no compatibility shims needed. Verified end-to-end: `claude mcp doctor --help` (usage shown), `claude mcp doctor --config-only` (6 servers reported, 0 blocking — browser/cheatengine/ghidra + 3 claude.ai-proxy), `claude mcp doctor --config-only --json` (structured JSON), `claude mcp doctor ghidra --config-only` (single-server target), `claude mcp doctor --scope bogus` (rejected with valid-scope list). User-driven: matches the user's open `/mcp freeze` issue per `session_06apr_issues.md` memory — diagnostic surfaces validation errors / scope conflicts / live-connection state in one report. Row flipped `❌ ✅ ❌` → `❌ ✅ ✅` (CCB still has no doctor.ts). §7 deep-dive backlog now closed: 1 Tier-2 shipped (MCP doctor), 1 demoted to no-op (`OPENCLAUDE_DISABLE_STRICT_TOOLS` env-gate — architectural mismatch), 0 deferred.
- **2026-04-25 (§7 source-level deep-dive + 14 column flips across 8 rows)** — Source-level pass on §7 MCP Servers + Tool Infrastructure. Re-read every `src/services/mcp/` file, `src/utils/{mcpValidation,claudeInChrome,computerUse,browserMcp,ghidraMcp}/` directory, and provider-shim file (`services/api/openaiShim.ts` Gitlawb / `services/api/openai/` CCB / `services/api/openaiBridge/` ours) across all three forks. **Most correction-heavy area audited so far** — 14 column flips across 8 rows (vs §11's 8 + §4's 9). Three classes of correction landed. (1) **Three byte-identical-LOC false-negatives** — `xaaIdpLogin.ts` (487 LOC), `vscodeSdkMcp.ts` (112 LOC), `elicitationHandler.ts` (313 LOC) all confirmed byte-identical across all three forks via `diff -q` (zero output). Wiring in ours is active (5+ non-test callers each in `commands/mcp/addCommand.ts`, `services/mcp/auth.ts`, `services/mcp/client.ts`, `tools/{Bash,FileEdit,FileWrite}Tool`, `useManageMCPConnections.ts`, `components/mcp/ElicitationDialog.tsx`, etc.). All three rows flipped `— ✅ ⚠️/❌` → `✅ ✅ ✅`. (2) **MCP doctor — biggest §7 audit error.** Audit had `✅ ✅ ✅`; verified only Gitlawb ships `services/mcp/doctor.ts` (695 LOC). CCB and ours both have NO `doctor.ts` (`ls /tmp/ccb-docs/src/services/mcp/doctor.ts` → MISSING). Architecture: pure-logic `doctorAllServers()` + `doctorServer(name)` in services/mcp/doctor.ts → `commands/mcp/doctorCommand.ts` (CLI subcommand `claude mcp doctor [name] [--scope] [--config-only] [--json]`) → `mcpDoctorHandler` + `formatDoctorReport` in `cli/handlers/mcp.tsx` → `main.tsx:3897` registration. Two-column flip: `✅ ✅ ✅` → `❌ ✅ ❌`. **Single genuine §7 adapt candidate** — Tier 2 if user-reported MCP-server breakage is recurring (we ship 3 MCP servers by default: zendriver / ghidra / computer-use; Ghidra alone exposes 158 tools), Tier 3 otherwise. Estimated 1-day port (~840 LOC across 3 files + 2-line wiring; all `services/mcp/` deps already exist in our fork). Decision deferred pending user signal. (3) **Two Gitlawb-demotions on backport rows the audit credited Gitlawb with.** **MCP `maxResultSizeChars` 500K override** `⚠️ ✅ ✅` → `❌ ❌ ✅` — `mcpValidation.ts` is 208 LOC in CCB+Gitlawb, 244 LOC in ours; the diff is the 2.1.91 superset (`MAX_RESULT_SIZE_CHARS_CEILING = 500_000` + `resolveMaxMcpOutputChars()` + `metaOverrideChars` threading through `mcpContentNeedsTruncation`/`truncateMcpContent`/`truncateMcpContentIfNeeded`). `services/mcp/client.ts` `_meta['anthropic/maxResultSizeChars']` wiring at lines 1888-1891 / 2751 / 2872 / 3077 is also ours-only. Cross-fork grep for `MAX_RESULT_SIZE_CHARS_CEILING|anthropic/maxResultSizeChars` in CCB+Gitlawb returned zero hits — confirms neither fork has the backport. **MCP tool error: all content blocks** `— ✅ ✅` → `❌ ❌ ✅` — verified by reading the `isError` handler in each fork's `services/mcp/client.ts`: ours (line 3160-3190) joins text from all content blocks via `.filter().map().join('\n')`; Gitlawb (line 3171-3199) and CCB (line 3126-3151) both still use `firstContent = result.content[0]` (pre-2.1.89). Both forks demoted from `✅`/`—` to `❌`. (4) **MCP schema normalization (strict tools)** `⚠️ ✅ ⚠️` → `⚠️ ✅ ✅` — kickoff predicted a 5-minute env-gate port of Gitlawb's `OPENCLAUDE_DISABLE_STRICT_TOOLS` at `openaiShim.ts:774`. Reality: **ours has no openaiShim.ts at all** — replaced by `services/api/openaiBridge/` per-provider registry where `supportsStrictTools` is opt-in (default off). Gitlawb's env gate buys "no strict-tools sent to compat providers"; that's our default behavior unmodified for z.ai/DeepSeek (Anthropic-native endpoint, no normalization) and NVIDIA NIM (no `supportsStrictTools` flag set in `providers/nvidiaNim.ts`). Env gate structurally unnecessary — adapt action: none. (5) **Chrome MCP** `✅ ✅ ❌` → `✅ ✅ ⚠️` — ours ships full 2337-LOC `utils/claudeInChrome/` directory + tool-rendering wired in `services/mcp/client.ts:238` + settings UI in `components/Settings/Config.tsx`; MCP server registration deliberately commented out at `main.tsx:118-119` ("DISABLED: browser functionality replaced by external MCP server" — zendriver-mcp). `⚠️ (disabled in favor of zendriver-mcp)` more accurate than `❌`. (6) **Computer Use (cross-platform)** `✅ ✅ ⚠️` → `✅ ✅ ✅ (npx)` — ours ships same 15-file shim shape as Gitlawb (15 files / 2131 LOC vs Gitlawb's 2161); `setup.ts` runs `npx -y computer-use-mcp` to deliver domdomegg's upstream. CCB's 35-file 8806-LOC + 3 separate `@ant/computer-use-{mcp,swift,input}` packages is heavier but functional surface is parity at runtime. (7) **WeChat/Weixin channel** `✅ ⚠️ ⚠️` → `✅ (+native package) ✅ ✅` — `channelNotification.ts` is 316 LOC byte-identical between Gitlawb and ours (CCB 266); user-facing WeChat surface fully covered by generic pipeline; CCB additionally ships dedicated `packages/weixin/` native transport. Both `⚠️`s flip to `✅`. **Audit error counts: 14 column flips, 8 rows.** `OPENCLAUDE_DISABLE_STRICT_TOOLS` env-gate port demoted to no-op (architectural mismatch). Single deferred adapt: MCP doctor (~1 day if user signals interest). Full per-row analysis + verification commands + diff outputs at `coffeegrind123/openclaude:context/mcp-tool-infrastructure-deepdive.md`.
- **2026-04-25 (§5 adapt candidates skipped per user)** — Both Gitlawb-only adapt candidates surfaced in the §5 deep-dive were user-confirmed-skipped: **VS Code extension** (5616 LOC JS, marketplace extension) — skipped because stock IDE integration + integrated-terminal launch already covers the convenience surface and marketplace presence isn't a current goal; **headless gRPC server** (252 LOC server + 100 LOC proto + 121 LOC test client) — skipped because the existing CCR HTTP+SSE server already covers the JS / browser / shell consumer surface and no non-JS headless consumers (Go / Rust / Python micro-services) are anticipated. **§5 closed: 3 audit cell flips landed (1 ours-promotion on Deep linking, 2 §4-mirror demotions on the runner-command rows); 0 source changes; backlog clean.** Adapt-backlog table in `coffeegrind123/openclaude:context/integration-headless-ide-deepdive.md` updated to record both skips with rationale.
- **2026-04-25 (§5 source-level deep-dive + 3 row corrections)** — Source-level pass on §5 Integration / Headless / IDE (numbered `## 6.` in this file; `§5` is the deep-dive's working name per kickoff). Re-read every `src/services/acp/`, `src/services/acpLink/`, `src/ssh/`, `src/ccr-server/`, `src/grpc/`, `src/proto/`, `src/utils/deepLink/`, `src/environment-runner/`, `src/self-hosted-runner/` file across all three forks plus Gitlawb's `vscode-extension/openclaude-vscode/`. **Three cell flips landed.** (1) **Deep linking (URL protocol handler)** ours `⚠️` → `✅ (++)` — the kickoff predicted ours ships only 411 LOC across 2 files; reality is **1629 LOC across 7 files** (full 6-file `deepLink/{registerProtocol,terminalPreference,protocolHandler,terminalLauncher,banner,parseDeepLink}` + `desktopDeepLink.ts`), byte-identical to Gitlawb on 4 of 6 files (`banner`, `protocolHandler`, `terminalLauncher`, `terminalPreference`), 1-line cosmetic diff on `registerProtocol` (`~/.openclaude.json` vs `~/.claude.json`), and `parseDeepLink.ts` is a **superset** of Gitlawb/CCB with the 2.1.91 multi-line-prompts backport (5 extra lines for `containsControlChars(s, allowNewlines)` so encoded `%0A` survives in `?q=` while `cwd`/`repo` still reject control chars). (2) **`claude environment-runner` (BYOC)** §5 row CCB `❌` → `⚠️`, Gitlawb `❌` → `⚠️` — mirrors §4 verdict (commit `03e63e8`): CCB ships 3-line `Promise.resolve()` stub, Gitlawb ships dead routing pointing at deleted `src/environment-runner/` module. The §5 row's "command exists at top-level CLI" lens technically matched both forks via cli.tsx routing; aligning to §4's wired-stub `⚠️` is more consistent. (3) **`claude self-hosted-runner`** §5 row CCB `❌` → `⚠️`, Gitlawb `❌` → `⚠️` — same §4-mirror. **Two genuine adapt candidates surface but stay user-decision-deferred** (no Tier-1 / no Tier-2 work shipped from §5): (a) **VS Code extension** (Gitlawb `vscode-extension/openclaude-vscode/`, 5616 LOC JS, 10 commands + chat panel + control center, publisher `devnull-bootloader`, talks to CLI via stream-json NDJSON over stdin/stdout — provider-agnostic) — three paths: skip with rationale (recommended pending concrete user demand; stock IDE integration + integrated terminal already covers the convenience surface), verbatim port as `coffeegrind123/openclaude-vscode` sibling package (1–2 days), or TS rewrite (1–2 weeks, worst-of-both). (b) **Headless gRPC server** (Gitlawb `src/grpc/server.ts` 252 LOC + `src/proto/openclaude.proto` 100 LOC + `scripts/grpc-cli.ts` 121 LOC test client + `scripts/start-grpc.ts` 50 LOC entry shim — only invoked via `bun run scripts/start-grpc.ts`, no `claude` subcommand wiring even in Gitlawb) — Tier 2 if non-JS headless consumers (Go / Rust / Python micro-services) are anticipated; skip otherwise (CCR HTTP+SSE server already covers the JS / browser / shell consumer surface; gRPC adds bidir streaming + protobuf typing + native backpressure but duplicates the dispatch role). 1–2 days verbatim port + `claude grpc-server start` subcommand if user gives go. **The kickoff's "Tier 3 polish — backport Gitlawb's full deepLink shape" item is moot — we already ship it.** Full per-row analysis + cost estimates + decision-blocker questions at `coffeegrind123/openclaude:context/integration-headless-ide-deepdive.md`.
- **2026-04-25 (§4 source-level deep-dive + 9 row corrections)** — Re-read every `src/bridge/`, `src/server/`, `src/remote/`, `src/ssh/`, `src/daemon/`, `src/environment-runner/`, `src/self-hosted-runner/` file across all three forks plus `packages/remote-control-server/` (CCB). **Nine cell flips landed.** Five ours-promotions reverting 2026-04-24 false negatives: (a) **Trusted-device tokens** ❌→✅ — `bridge/trustedDevice.ts` byte-identical to CCB at 210 lines, 5 non-test callers in bridge core + login/logout flows. (b) **Capacity-wake signal** ❌→✅ — `bridge/capacityWake.ts` byte-identical (56 lines) across all three forks, wired in bridgeMain + replBridge. (c) **Direct-connect session manager** ⚠️→✅ — the 3 real client files (`createDirectConnectSession.ts` + `directConnectManager.ts` + `types.ts`) byte-identical across all three; the 7 placeholder server stubs in CCB and ours are inert (`export {}` / `Promise.resolve()`); `useDirectConnect` + REPL + `main.tsx:203` all wired. CCB also credited from `—` → `✅` since they ship the same 3 real files. (d) **RemoteSessionManager + SessionsWebSocket** ⚠️→✅ — `src/remote/` 4 files byte-identical to Gitlawb across all three forks, wired through `useRemoteSession` → REPL.tsx:1442. CCB also `—` → `✅`. (e) **Long-poll task assignment** ⚠️→✅ — `pollConfig.ts` (110) + `pollConfigDefaults.ts` (82) byte-identical; `bridgeMain.ts` has 20+ runtime references using `pollConfig.{multisession_poll_interval_ms_at_capacity, _partial_capacity, _not_at_capacity, non_exclusive_heartbeat_interval_ms}`; `bridgeApi.ts#pollForWork` matches Gitlawb byte-for-byte. **Two CCB demotions (file-exists-but-inert pattern, same as §11 tokenAnalytics):** (f) **BYOC environment runner** CCB ✅→⚠️ — `src/environment-runner/main.ts` is a 3-line `Promise.resolve()` stub. The 2026-04-24 audit-changelog credit was based on file-existence only; the `entrypoints/cli.tsx` routing then resolves to a no-op. Ours is the only fork shipping a working 342-line BYOC runner. (g) **Self-hosted runner (CCR v2)** CCB ✅→⚠️ — same 3-line stub pattern; ours is the only fork with a working 252-line CCR v2 worker. **Two CCB credits previously marked `❌`/`—`:** (h) **`/remote-env`, `/remote-setup`** CCB ❌→✅ — both commands ship in CCB at `commands/remote-env/` (2 files) + `commands/remote-setup/` (3 files). Slash-commands-table row at line 372 also flipped `—` → `✅`. (i) **`/bridge-kick`** CCB `—` → ✅, Gitlawb ❌ → ✅ — byte-identical 200-line file across all three forks; "Our unique" annotation dropped (Ant-only debug command but vendored identically by all three). **Row 14 also renamed:** "Debug mode (`--debug` + Bun inspect)" → **"Debug mode (`-d, --debug` filter flag)"** — the "+ Bun inspect" suffix was a misread of CCB's argv-based `--inspect`/`--inspect-brk` *detection* (runtime introspection, not a feature). Both ours and Gitlawb already detect the bare flag via `utils/debug.ts:49`; gap is just the top-level `-d, --debug [filter]` commander option. Cells moved to `⚠️` to reflect the smaller actual gap. **Adapt backlog: 1 Tier-2 (handleRemoteInterrupt → pauseProactive port — fixes /super + /assistant remote-interrupt vs proactive-tick-loop race), 3 Tier-3 (debug-flag commander option, bridgeResultScheduling /clear deferral, rcDebugLog adoption). Self-hosted RCS React UI confirmed skip — 24K LOC across 50 backend + 89 frontend files (React 19 + Radix + Tailwind v4 + Vite v6).** Full per-row analysis + verification commands + line counts at `coffeegrind123/openclaude:context/remote-control-ssh-bridge-deepdive.md`.
- **2026-04-25 (§3 Tier-2 adapts shipped)** — Both Tier-2 polish items from the §3 deep-dive landed in openclaude commit `7f3ff65`. (1) **`/dream` skill upgraded to superset.** `src/skills/bundled/dream.ts` (28L → 73L) prepends CCB's `DREAM_PROMPT_PREFIX` ("you are performing a manual dream — this run has full tool permissions and the user is watching, unlike the automatic background dream") and appends Gitlawb's session-list block (`listSessionsTouchedSince(lastAt)` + "last run: Xh ago" + filter-out current session). Both helpers (`readLastConsolidatedAt`, `listSessionsTouchedSince`) already exported byte-identically from `services/autoDream/consolidationLock.ts`. Manual `/dream` runs now distinguish themselves from background autoDream (preamble) and have concrete consolidation targets (session-list) instead of forcing the model to guess what "recent" means. Row updated `✅ ✅ ✅ (skill)` → `✅ ✅ ✅ (skill, ++)`. (2) **`/proactive on` primer system-reminder.** `src/commands/proactive-impl.ts` (39L → 51L) now enqueues `<system-reminder>` ahead of the first tick via `enqueuePendingNotification` (same queue path `useProactive.ts` uses for tick injection). Eliminates the "first-tick filler" problem where the model produces "I'm now in proactive mode. Standing by." on its first tick after activation. Two guards prevent double-priming when interacting with `/super`: skip if `wasActive=true` (already running) and skip if `process.env.CLAUDE_CODE_SUPER_MODE === '1'` (super's stricter orchestrator-protocol primer supersedes). `/super on` activates proactive directly via `super-impl.ts:42` (does NOT route through the `/proactive` command path), so super's own primer remains the only one that fires when entering super mode. Verified across 8 interaction paths between `/proactive`, `/super`, and `/dream` — no harmful collisions. Path 4 (proactive→super in succession) leaves both primers in the queue; super's "this overrides any conflicting guidance" sentence resolves it cleanly. Row note for "Proactive tick loop" updated to reference the activation-primer port. **§3 deep-dive backlog now closed: 0 Tier-1 + 2 Tier-2 shipped + 6 Tier-3 deferred (CCB autonomy/CCR/swarm-team-bound items, correctly excluded per kickoff).**
- **2026-04-25 (§3 source-level deep-dive + row corrections)** — Re-read every assistant/proactive/autoDream/awaySummary/Sleep/PushNotification/SubscribePR file across all three forks. The §3 area is mostly verification + `(++)` annotations (no Gitlawb-advantage rows; CCB-advantage is autonomy-bound and excluded by design). Five row updates landed: (a) **Proactive tick loop** annotated `(++)` for ours — `swarmNudge.ts` (149-line `/super`-mode parallel-fanout enforcer) has no equivalent in CCB, plus coordinator-conflict guard in `/proactive on`. (b) **Push notifications** annotated `(++)` for ours — CCB's `PushNotificationTool` is bridge-bound (axios POST to `/v1/sessions/{id}/events`, returns `sent:false` without a connected RCS bridge — functionally inert outside Anthropic-hosted infra); ours is local terminal escapes (iTerm2/Kitty/Ghostty/bell) + notification hooks, independently functional. Different scope by design. (c) **Auto-Dream consolidation** annotated `(++)` for ours — autoDream runs in KAIROS mode (CCB + Gitlawb both `return false` if `getKairosActive()`) and ours short-circuits the `tengu_onyx_plover` GrowthBook check to default-on. (d) **Mobile push (KAIROS feature set)** row renamed to **"`/mobile` slash command (Anthropic-app QR code)"** — all three forks ship a `/mobile` command showing a QR code linking to Anthropic's 1st-party mobile app (iOS App Store / Google Play); aliases `/ios` + `/android`. Pure marketing surface — not a push feature. Audit row was previously mislabelled. (e) **New row: SubscribePR tool** split out from "Push notifications" — CCB ships an 88-line stub returning `error: 'requires KAIROS GitHub webhook subsystem'` unconditionally; Gitlawb has no SubscribePR tool; ours has a 193-line working implementation (`gh` CLI polling + cron task + per-PR state file at `~/.claude/pr-subscriptions/`). Only fork that actually subscribes to PRs. §8 row updated to `✅ (stub) ❌ ✅` to match. Also extended the **Assistant mode (persistent)** row note to clarify ours is local-only KAIROS by design — every CCB-only sub-feature (`initializeAssistantTeam` real impl, `discoverAssistantSessions`, JSX `/assistant` panel, `NewInstallWizard`) is autonomy/CCR/swarm-team-bound and correctly excluded per kickoff. **2 Tier-2 adapt candidates surfaced (no Tier-1 work)**: `/dream` skill should borrow CCB's `DREAM_PROMPT_PREFIX` preamble + Gitlawb's `listSessionsTouchedSince(lastAt)` + "last run: Xh ago" timing-context block (~30 min combined); `/proactive on` should emit CCB's primer system-reminder (`"do useful work on each tick or call Sleep — don't say 'still waiting'"`) on activation (~10 min). Both are pure prompt-shaping wins, deferred until user requests them. Full per-row analysis lives in `coffeegrind123/openclaude:context/assistant-proactive-kairos-deepdive.md`.
- **2026-04-24** — Initial CCB audit. First Explore-agent pass had ~10 false negatives; corrected via direct verification. 3 Tier-1 gaps identified: ACP, SSH Remote, acp-link. (Prior `ccb-parity-audit.md`.)
- **2026-04-24** — ACP, acp-link, SSH Remote ported from CCB. Three Tier-1 CCB gaps closed.
- **2026-04-24** — Initial Gitlawb audit (source-first, no doc catalogue). ~40 features classified. (Prior `gitlawb-parity-audit.md`.)
- **2026-04-24** — **This file.** Merged the two audits into a single three-way comparison with 24 categorized tables. Rebuilt slash-command section by enumerating our actual `src/commands/` directory — prior Gitlawb audit had ~20 false-negative command claims (`teleport`/`rewind`/`thinkback`/`passes`/`insights`/`issue`/`pr_comments`/`sandbox-toggle`/`rate-limit-options`/`reload-plugins`/`mobile`/`privacy-settings`/`perf-issue`/`remote-env`/`remote-setup`/`rename`/`reset-limits`/`share`/`summary`/`stats`). Also corrected: vim keybindings (we have `src/utils/swarm/` not just nudge), swarm/teammate (full parity with Gitlawb's `src/utils/swarm/` 13-file layout), doctor diagnostic utils (`utils/doctorContextWarnings.ts` + `doctorDiagnostic.ts` exist in ours). 20 prioritized backport items identified; DuckDuckGo WebSearch recommended as #1.
- **2026-04-24 (correction — CCB source re-inventory)** — User flagged that the CCB half was classified from docs only. The clone directory `/tmp/ccb-docs` is actually a full source repo: 2741 TS files in `src/` + 13 `packages/` including 5 native NAPI modules (`audio-capture-napi`, `color-diff-napi`, `image-processor-napi`, `modifiers-napi`, `url-handler-napi`). Protocol rewritten (`coffeegrind123/openclaude:context/fork-parity-audit-protocol.md` §2–§3) — doc-based vs source-based framing removed; every fork is source-based. Delegated a second Explore agent to inventory CCB source; substantive corrections landed in this revision:
  - §1 Provider/Auth: Gemini now ✅ CCB (`src/services/api/gemini/`); new Grok row (CCB ✅ only, `src/services/api/grok/`); `/provider` reclassified CCB ⚠️ (env toggler, not wizard).
  - §4 Remote Control: RCS now full ✅ CCB (React 19 + Vite + Radix + Tailwind + Shiki + QR code via `packages/remote-control-server/`); BYOC environment-runner + self-hosted runner CCB ✅ (confirmed `src/environment-runner/main.ts` + `src/self-hosted-runner/main.ts`); SSH Remote CCB ✅ (confirmed 5-file `src/ssh/` layout at source — matches ours).
  - §7 MCP: CCB Chrome + Computer Use now attributed to `@ant/*` packages (`@ant/claude-for-chrome-mcp`, `@ant/computer-use-mcp`, `@ant/computer-use-input`, `@ant/computer-use-swift`). New WeChat/Weixin row.
  - §8 Tools: `/force-snip`, `/subscribe-pr` reclassified CCB ✅ (previously wrongly "ours unique").
  - §9 Commands: `/init-verifiers`, `/attach`, `/claim-main`, `/detach`, `/peers`, `/pipe-status`, `/pipes`, `/send`, `/fork`, `/daemon`, `/monitor` all reclassified CCB ✅. New CCB-unique commands: `/autonomy`, `/lang`, `/poor`, `/skill-search`, `/skill-learning`, `/history`, `/job`, `/debug`.
  - §14 Langfuse: now ✅ CCB real service (`src/services/langfuse/` + `packages/langfuse-dashboard/`).
  - §16 Skills: Experimental Skill Search **major reclassification** — CCB ✅ with ~970 lines real impl (`localSearch.ts` 444, `prefetch.ts` 328, `intentNormalize.ts` 149); Gitlawb ❌ (no `services/skillSearch/` at all); ours ⚠️ 20-line stubs. Prior audit's "symmetric stub" finding was wrong. New Skill Learning row: CCB ✅ unique.
  - §17a/17b/17c (new) — Native NAPI modules table + `@ant/*` forked-Anthropic packages + CCB auxiliary packages (cc-knowledge, langfuse-dashboard, mcp-server, shell, swarm, weixin, acp-link, agent-tools, mcp-client, remote-control-server, builtin-tools).
  - §21 Unique-to-CCB: complete rewrite with source-verified features organized by category; added 5 NAPI modules, `@ant/*` package list, real Skill Search, Skill Learning, Autonomy subsystem, VCR service, sessionTranscript service, commands `/autonomy`/`/lang`/`/poor`/`/skill-search`/`/skill-learning`/`/history`/`/job`/`/debug`, Grok native, RCS React UI, WeChat native package, cc-knowledge package. Explicit "parity with ours (previously misclassified)" subsection flags the prior errors.
  - §22 Backlog: added #19 Real Skill Search, #20 Autonomy subsystem, #23 RCS React UI, #24 Grok native, #25 Native NAPI audio-capture. Renumbered existing items.
- **2026-04-24 (away-summary correction + idle-fallback port)** — Audit had `Away summary` as ❌ on our column in both §3 and §15; actually the feature was shipped already (service + hook + REPL wiring + message subtype + `AWAY_SUMMARY` flag in force-enabled bundle) — false negative from the same docs-without-ls pattern that hit CCB. On inspection we had Gitlawb's shape (`'unknown'` focus state → no-op), so in our interactive Docker container (piped stdin, no DECSET 1004 focus events) the summary would never fire. Ported CCB's 3rd `useEffect` block — idle-timer path gated on `state === 'unknown'` that treats `isLoading` transitions as presence signal (turn starts = cancel timer + abort, turn ends = restart). Preserved our `hasPendingInput` guard inside the idle path so it still skips when user is mid-composition. Added `AwaySummaryNotice.tsx` (4 sessions, same convention as the other 21 notices). Registered in `SingleNotice.tsx` rotation + `awaySummaryNoticeSeenCount` in globalConfig. Row updated to `✅ (++)` in §3 (we're now the union of CCB's fallback + Gitlawb's simpler service + our three additions: settings gating, env override, pending-input guard). Row updated to `✅` in §15. CLAUDE.md paragraph added under "Key Architecture Decisions" + row in Feature Notices table.
- **2026-04-24 (§2 adapt backlog shipped)** — 4 of 5 §2 deep-dive adapts landed in openclaude commit `c07d7f5`. (P0) `src/coordinator/workerAgent.ts` stub replaced with real hybrid impl (Gitlawb's `GENERAL_PURPOSE_AGENT` reuse + CCB's orchestration-tool curation), fixes runtime `TypeError` on first `/coordinator` worker spawn. Row flipped back to `✅ ✅ ✅`. (Tier 1) Gitlawb's `withGitWorktreeMutationLock` ported to `src/utils/worktree.ts` with double-checked locking — `getOrCreateWorktree` fast-reads head outside lock, re-checks inside lock, then delegates to new `doCreateWorktreeLocked` helper. `removeAgentWorktree` also wrapped. (Tier 1) Graceful non-git fallback added at `src/tools/AgentTool/AgentTool.tsx:592` — try/catch re-throws only on explicit `isolation: 'worktree'`, otherwise logs + falls back to cwd. Worktree isolation row upgraded to `✅ ✅ ✅ (++)`. (Tier 2 correction) `leaderPermissionMode` investigation showed it was **already shipped in ours** — earlier audit misread the `diff` direction (`>`-prefixed lines are ours, not theirs). Our `spawnInProcess.ts:67` declares the field, `:175-177` threads it through. Deep-dive annotation corrected. (Tier 3) Eight `@deprecated` JSDoc markers added to file-based permission functions in `src/utils/swarm/permissionSync.ts` — `writePermissionRequest` / `readPendingPermissions` / `readResolvedPermission` / `resolvePermission` / `cleanupOldResolutions` / `pollForResponse` / `deleteResolvedPermission` / `submitPermissionRequest`. Each cites the mailbox-based successor + the unauthenticated-directory security concern. Pure documentation — verified by grep no non-self callers. All §2 deep-dive adapts DONE.
- **2026-04-24 (§2 source-level deep-dive + row corrections + production bug surfaced)** — Re-read every `src/tools/AgentTool/`, `src/coordinator/`, `src/utils/swarm/`, `src/utils/teammate*`, `src/utils/{forkedAgent,standaloneAgent,worktree,worktreeModeEnabled}.ts`, and `src/tools/VerifyPlanExecutionTool/` file across all three forks (CCB's equivalents live at `packages/builtin-tools/src/tools/` as a workspace package). Four row corrections: (a) **Swarm / Agent Teams** `⚠️ ✅ ✅` → `✅ ✅ ✅` — CCB ships the full 14-file swarm dir (~4571 lines, byte-identical on most files), not a "⚠️ experimental stub" as docs suggested; (b) **Teammate mailbox** `⚠️ ✅ ✅` → `✅ ✅ ✅` — byte-identical across all three (4-line trivial diff); (c) **VerifyPlanExecution** `— ✅ ✅` → `⚠️ ❌ ✅` — CCB's 93-line tool is a self-report (agent claims completion, tool echoes back), Gitlawb is 3-line stub, ours is 223-line active forked-agent verifier (uniquely advanced); (d) **Coordinator Mode** `✅ ✅ ✅` → `✅ ✅ ⚠️` to flag our production bug: `src/coordinator/workerAgent.ts` is a 1-line `export default {}` stub, but call-site at `builtInAgents.ts:38-41` expects `getCoordinatorAgents()` export — throws TypeError on first `/coordinator`-mode worker spawn. All dependencies (`ASYNC_AGENT_ALLOWED_TOOLS`, `GENERAL_PURPOSE_AGENT`, `EXPLORE_AGENT`, `PLAN_AGENT`) exist in our tree. Full row-by-row analysis + 5-item adapt backlog (P0 workerAgent fix, Tier 1: withGitWorktreeMutationLock + non-git fallback, Tier 2: leaderPermissionMode inherit, Tier 3: permissionSync deprecation comments) lives in `coffeegrind123/openclaude:context/agents-coordinator-swarm-deepdive.md`. Adapt-surface ~2 hours total.
- **2026-04-24 (§10 Tier-2 + Tier-3 shipped)** — Two further adapts from the deep-dive landed in openclaude commit `1e1983f`. (a) **Real cachedMicrocompact port** — replaced our 29-line type-stub at `services/compact/cachedMicrocompact.ts` with CCB's full 112-line implementation (Set-backed `registeredTools`, ordered `toolOrder`, `deletedRefs`, `pinnedEdits[]`, `toolsSentToAPI`). `isCachedMicrocompactEnabled()` reads `CLAUDE_CACHED_MICROCOMPACT=1`; `isModelSupportedForCacheEditing()` regex-matches `/claude-[a-z]+-4[-\d]/`. `getCachedMCConfig()` returns `{triggerThreshold: 10, keepRecent: 5}`. Added our own `markToolsDeleted(state, ids)` helper so `microCompact.ts` can mark IDs as deleted right after `pendingCacheEdits` is queued — eager-mark semantics matching CCB's test fixture. Aligned `CachedMCEditsBlock` type in `services/api/claude.ts` with CCB's shape (`{type: 'delete_tool_result', tool_use_id}`) — the pre-existing `{type: 'delete', cache_reference}` shape was dead infrastructure, we never set `cache_control.name` so there was nothing to reference. Added empty-string `CACHE_EDITING_BETA_HEADER` placeholder to `constants/betas.ts` since the exact identifier is ant-gated upstream; Claude 4.x accepts `cache_edits` without the header. Cached MicroCompact row flipped from `✅ ❌ ⚠️` → `✅ ❌ ✅`. (b) **compressToolHistory port** — new `src/services/api/compressToolHistory.ts` (~230 lines). Tiered recent/mid/old compression scaled to `getEffectiveContextWindowSize()`. Mid-tier 2KB truncate with trailing marker; old-tier stub `[<toolName> args=… → N chars omitted]`. Reuses `isCompactableTool` + `TOOL_RESULT_CLEARED_MESSAGE`. Wired as a pre-translate pass at the top of `translateAnthropicRequestToOpenAI()`. Default-off via `toolHistoryCompressionEnabled` setting. Runs only on `openaiBridge` routes (NIM today, future OpenAI-compat providers) — Anthropic-native path bypasses entirely. Small-context tool_result compression row flipped from `❌ ✅ ⚠️` → `❌ ✅ ✅`; removed from main-audit Tier 2 backlog as #21. Only remaining deep-dive item: `stripThinkingBlocks` 3P-provider resume guard (Tier 2 #4) — non-blocking since our DeepSeek-via-Anthropic-endpoint doesn't hit the issue.
- **2026-04-24 (§10 Tier-1 adapt backlog shipped)** — Three Tier-1 adapts from the deep-dive landed in openclaude commit `7a36283`: (a) **MCP tool compaction** — added exported `isCompactableTool(name)` helper with `mcp__*` prefix match to `services/compact/microCompact.ts`, swapped call site from `COMPACTABLE_TOOLS.has()`; unlocks compaction for the 200+ MCP tools from Ghidra + zendriver + Computer Use. (b) **autoCompact universal floor** — `getEffectiveContextWindowSize()` now clamps with `Math.max(effectiveContext, reservedTokensForSummary + getAutoCompactBufferTokens(model))`. Universal safety net on top of the DeepSeek-specific `lowContextMode` path; prevents #635-style negative-threshold loops on unknown 3P providers. All 6 existing `getEffectiveContextWindowSize` tests stay green. (c) **8 MiB resume transcript cap** — added exported `ResumeTranscriptTooLargeError` + internal `assertResumeMessageSize()` in `utils/conversationRecovery.ts`, wired at two call sites (post-deserialize pre-hook, and post-hook-append). Fails fast before REPL boot on corrupted sessions instead of wedging on multi-GB loads. Row updates: MicroCompact → `✅ ✅ ✅ (++)`, Forced auto-compact fallback notes updated with floor, Conversation recovery → `✅ ✅ (++) ✅ (++)` (ours matches Gitlawb's shape now, still open: 3P-provider thinking-block strip from Tier 2). Deep-dive §Tier-1 items marked DONE.
- **2026-04-24 (§10 source-level deep-dive + row corrections)** — Re-read every `services/compact/`, `services/SessionMemory/`, `services/extractMemories/`, `services/teamMemorySync/`, `services/contextCollapse/`, `services/sessionTranscript/`, `src/memdir/`, and `utils/{sessionRestore,conversationRecovery,sessionIngressAuth,crossProjectResume}.ts` file across all three forks. Found four row misclassifications and corrected them: (a) **Cached MicroCompact** flipped from `— ✅ ✅` to `✅ ❌ ⚠️` — only CCB has real 112-line impl; Gitlawb is 12-line stub; ours is 29-line stub with wired-up types but no-op logic; (b) **Context Collapse** flipped from `⚠️ ✅ ✅` to `⚠️ ⚠️ ⚠️` — Gitlawb's "full impl" was actually a 7-line stub, all three ship stubs, our overflow recovery lives in reactiveCompact + forced auto-compact not contextCollapse; (c) **Session ingress auth** flipped from `— ✅ ⚠️` to `✅ ✅ ✅` — `utils/sessionIngressAuth.ts` is byte-identical 140 lines across all three; (d) **Conversation recovery** flipped from `— ✅ ❌` to `✅ ✅ (++) ✅` — we have 617-line impl; Gitlawb has two additions we lack (8 MiB hard cap + `stripThinkingBlocks` for 3P-provider resume) plus our unique malformed-text-block sanitization. Also clarified the Session transcript row to point at `utils/sessionStorage.ts` (the real path) vs the `services/sessionTranscript/` stub that exists in name only. Full per-row analysis + 6-item adapt backlog (Tier 1: MCP tool compaction in microCompact, universal autoCompact floor, 8 MiB resume cap; Tier 2: 3P-provider thinking-block strip during resume, real cachedMicrocompact port for Claude 4.x users; Tier 3: compressToolHistory already tracked in §22) lives in `coffeegrind123/openclaude:context/memory-compaction-session-deepdive.md`.
- **2026-04-24 (§11 source-level deep-dive + row corrections)** — Re-read every context/token-management file across all three forks (`services/api/{promptCacheBreakDetection,compressToolHistory,thinkTagSanitizer,toolArgumentNormalization,openaiSchemaSanitizer}.ts`, `utils/{tokenBudget,tokens,tokenAnalytics,thinkingTokenExtractor,schemaSanitizer,lowContextMode}.ts`, `utils/model/{check1mAccess,contextWindowUpgradeCheck}.ts`, `query/tokenBudget.ts`). Found three row misclassifications and corrected them: (a) **Prompt cache break detection** flipped from `— ✅ ⚠️` to `✅ ✅ ✅` — the 727-line `services/api/promptCacheBreakDetection.ts` is **byte-identical** between Gitlawb and ours (zero diff), CCB differs by one type-cast character; wired identically in all three via claude.ts + compact.ts + microCompact.ts + autoCompact.ts + AgentTool/runAgent.ts. Our `⚠️` was a false negative. (b) **1M context entitlement check** flipped from `— ✅ ⚠️` to `✅ ✅ ✅` — the 72-line `utils/model/check1mAccess.ts` is byte-identical across all three forks with identical 3-site wiring (`commands/model/model.tsx` + `utils/model/modelOptions.ts` + `utils/model/contextWindowUpgradeCheck.ts`). Our `⚠️` was a false negative. (c) **Tool argument normalization** flipped from `— ✅ ⚠️` to `— ✅ ❌` — we have **zero implementation** (grep for `normalizeToolArguments`/`STRING_ARGUMENT_TOOL_FIELDS` in our tree returns no hits); the `⚠️` was over-generous. Also verified: `thinkTagSanitizer` (162 lines, actively wired into Gitlawb's openaiShim + codexShim) and `schemaSanitizer` (258 lines, actively wired in Gitlawb's openaiShim) are real Tier-1/Tier-2 adapt candidates; `ThinkingTokenAnalyzer` + `TokenUsageTracker` are **unwired dead library code in Gitlawb** (only referenced by their own test files) — deferred to Tier 3 with no current value. Full per-row analysis + 3-item runtime adapt backlog (Tier 1: thinkTagSanitizer + toolArgumentNormalization into openaiBridge; Tier 2: schemaSanitizer replacing our no-op `sanitizeToolParameters`; Tier 3 deferred: ThinkingTokenAnalyzer + TokenUsageTracker) lives in `coffeegrind123/openclaude:context/context-token-deepdive.md`.
- **2026-04-24 (§11 deep-dive follow-ups — scoping + Gitlawb demotions)** — User flagged two things on review: (a) the three Tier-1/Tier-2 runtime adapts should all be **openaiBridge-scoped** to match the `compressToolHistory` pattern shipped in commit `1e1983f` (Anthropic-native path — z.ai, DeepSeek-via-Anthropic-endpoint, first-party — bypasses entirely since those providers serialize reasoning to proper `thinking` blocks server-side, emit structured `tool_use.input` JSON, and accept the full JSON Schema spec). Prior framing "matters immediately since z.ai→GLM-4.7 is our default route" removed — z.ai's Anthropic-compat endpoint doesn't hit any of these paths. (b) Two rows where Gitlawb's cell was too generous given the file is unwired: **Token analytics** demoted `⚠️ ✅ ⚠️` → `⚠️ ⚠️ ⚠️` (Gitlawb's `tokenAnalytics.ts`/`TokenUsageTracker` imported only by its own test file — file-exists-but-inert, same pattern §10's deep-dive flagged for Gitlawb's "contextCollapse full impl"), and **Thinking token extraction (3P `<think>` tags)** demoted `❌ ✅ ❌` → `❌ ⚠️ ❌` (Gitlawb's `thinkingTokenExtractor.ts`/`ThinkingTokenAnalyzer` also unwired). Structural note for audit consumers: Token analytics is the one §11 item without a natural openaiBridge-scoping since it's an in-memory historical tracker, not a request/response translator. Full scoping rationale added inline to deep-dive rows 3, 5, 9, and 10.
- **2026-04-25 (§11 Tier 2 adapt shipped)** — Final §11 runtime adapt landed in openclaude commit `a60a05d`. **OpenAI strict schema sanitizer** — ported `utils/schemaSanitizer.ts` (258 lines) + 3 unit tests verbatim from Gitlawb. Wired into `openaiBridge/requestTranslator.ts:sanitizeToolParameters()` in commit `a60a05d` (replaced the prior pass-through no-op stub at line 355). Sanitizes JSON Schema for OpenAI-compat strict-mode acceptance: strips 17 incompatible keywords ($comment/$schema/default/else/examples/format/if/maxLength/maximum/minLength/minimum/multipleOf/pattern/patternProperties/propertyNames/then/unevaluatedProperties), recurses into anyOf/oneOf/allOf and array `items`, filters `required[]` against the post-sanitization property set, validates `enum[]`/`const` entries against the remaining type constraint, and normalizes `type:"null"`/array-typed `type` fields. **openaiBridge-scoped only** — call site is bridge-only by construction so replacing the no-op body preserves scoping. Pays off the moment a user points `ANTHROPIC_BASE_URL` at NIM/Groq/Together/Fireworks + installs an MCP server with rich schemas (Ghidra has 158 tools, many with `pattern` regexes and `examples` arrays that strict mode rejects). Verified end-to-end via `/tmp/schema-smoke.ts` running an MCP-shaped Ghidra-style schema through `translateTools()` — 17/17 checks pass (pattern/examples/minimum/maximum/default/$schema/$comment all stripped; required[] filtered to existing fields; type kept; non-tagged fields preserved). 102/102 unit tests + 40/40 openaiBridge regression tests stay green; 0 type errors on touched files. Row flipped `— ✅ ❌` → `— ✅ ✅`. With this all 3 §11 deep-dive Tier 1+2 runtime adapts are shipped; Tier 3 ThinkingTokenAnalyzer + TokenUsageTracker remain deferred (no consumer in our tree).
- **2026-04-24 (§11 Tier 1 adapts shipped)** — Both Tier-1 items from the §11 deep-dive landed in openclaude commit `7ceea66`. **(1) Thinking-tag sanitizer** — ported `services/api/thinkTagSanitizer.ts` (162 lines) + 42 unit tests verbatim from Gitlawb; wired into openaiBridge via a per-stream `createThinkTagFilter()` in `streamTranslator.ts` (text-delta `feed()` + finalize `flush()` to handle tags split across SSE frames, e.g. `</th` + `ink>`) and a post-stream `stripThinkTags()` in `responseTranslator.ts` for non-streaming completions. Reasoning/refusal/error paths intentionally bypass the filter so they can't strip content that isn't tag-wrapped. Row flipped `❌ ✅ ❌` → `❌ ✅ ✅`. **(2) Tool argument normalization** — ported `services/api/toolArgumentNormalization.ts` (69 lines) + 20 unit tests verbatim from Gitlawb; wired into openaiBridge `streamTranslator.ts` with a per-tool `jsonBuffer` + `normalizeAtStop` boolean keyed on `hasToolFieldMapping(name)`. For the six mapped tools (Bash/Read/Write/Edit/Glob/Grep), fragments are held back during streaming and a single normalized `input_json_delta` is emitted at `content_block_stop` — plain-string args like `"ls -la"` would leak through `input_json_delta` partial_json otherwise and break SDK assembly. Truncated output (`finish_reason='length'`) preserves the raw buffer to avoid turning garbage into a confidently-malformed command. Non-mapped tools (MCP, custom) pass fragments through unchanged. Row flipped `— ✅ ❌` → `— ✅ ✅`. Both adapts openaiBridge-scoped only — Anthropic-native path bypasses. Smoke-tested end-to-end with synthesized OpenAI-shaped streaming + non-streaming fixtures including boundary cases (partial-tag across frames, non-mapped MCP tool fragments, stop_reason upgrade). All 62 new unit tests pass; 40 existing openaiBridge tests stay green. Tier 2 `schemaSanitizer` still open; Tier 3 deferred.
