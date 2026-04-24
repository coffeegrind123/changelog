# CCB Port Kickoff — Next Session Prompt

> Save this file. Start the next session by saying: **"Read `ccb-port-kickoff.md` and begin Phase 1."**

---

## Session context — what landed previously (2026-04-24)

We ran a comprehensive feature-parity audit between our fork (openclaude) and the parallel reverse-engineering fork CCB (Claude Code Best, github.com/claude-code-best/claude-code). Output:

- **`fork-parity-audit.md`** — per-feature status table + prioritized backlog + audit changelog
- **`fork-parity-audit-protocol.md`** — 10-step methodology for future audits

Plus one shipped backport this pass:

- **TEAMMEM GitHub backend** — `src/services/teamMemorySync/githubBackend.ts`. Activates on `TEAMMEM_GITHUB_REPO=owner/repo`. Full pull/push via Trees + Blobs + Contents APIs, conflict retry, reuses upstream secret scanner + path-traversal guard. Provider-agnostic (works on z.ai/DeepSeek/NIM, not just Claude.ai OAuth).

The audit identified **3 Tier-1 gaps** to backport — that's this kickoff's scope.

---

## Recommended port order

Bottom-up by dependency + effort:

1. **SSH Remote backend** (4–7 days) — easiest. Wiring exists; just need backend impl.
2. **ACP (Agent Client Protocol)** (1–2 weeks) — bigger surface, but self-contained module.
3. **acp-link** (3–5 days, after ACP) — depends on ACP.

If you have to skip one, skip acp-link.

---

## Reference material — CCB docs

CCB docs were cloned to `/tmp/ccb-docs/`. If that's gone:

```bash
git clone --depth 1 https://github.com/claude-code-best/claude-code.git /tmp/ccb-docs
```

Key files for this porting work:

- `/tmp/ccb-docs/docs/features/ssh-remote.md` — SSH architecture, probe/deploy flow, auth proxy diagram
- `/tmp/ccb-docs/docs/features/acp-zed.md` — ACP protocol overview, agent state machine, Zed integration
- `/tmp/ccb-docs/docs/features/acp-link.md` — WebSocket bridge architecture
- CCB source is in the same clone — the `packages/` dir holds the per-package implementations they reference

The CCB code itself is the implementation reference. **Read CCB source before writing ours** — both forks are reverse-engineering the same upstream, so their implementation is a strong hint at what the right shape is. Cite specific CCB file paths in commit messages.

---

## Fork conventions — must follow

Before writing any code, read **`CLAUDE.md`** (project root) end-to-end. Highlights:

- **Runtime:** Bun, not Node. Build with `bun run build`. Dev with `bun run src/entrypoints/cli.tsx`.
- **All 87 feature flags enabled** via `node_modules/bundle/index.js`. SSH_REMOTE flag is already on; you don't need to enable it.
- **Stub files exist for many features.** When you implement one, replace the stub — don't add a sibling. The pattern is: keep the existing exports, fill them in.
- **CLAUDE.md updates:** Every major feature gets a one-paragraph entry under "Key Architecture Decisions". Keep it tight; this file is the agent ramp-up index.
- **Feature notices:** Every major user-visible feature gets a notice file in `src/components/LogoV2/Xxx Notice.tsx` (4-session count). See `GhidraMcpNotice.tsx` as the reference pattern. Required for SSH Remote and ACP, optional for acp-link.
- **CHANGELOG.md** lives in the public repo `coffeegrind123/changelog` (NOT this repo). After any commit, update it via the pattern in CLAUDE.md.
- **Don't re-read package-lock.json** or other huge files; use `head` / `jq`.
- **Build verification:** `bun run build` after every milestone. The bundled `dist/` is what's shipped.
- **Hot-patch the running container** with `docker cp <file> openclaude-interactive:/opt/openclaude-src/<file>` instead of rebuild — faster iteration. See CLAUDE.md "Hot-patching" section.

---

## Phase 1 — SSH Remote backend (start here)

### Current state in our repo

Wiring is **complete**:

- `src/main.tsx:593` — `_pendingSSH` PendingSSH state declaration
- `src/main.tsx:722` — pre-commander argv rewriter so `claude ssh host --flag` and `claude ssh --flag host` both work
- `src/main.tsx:3252` — session activation: imports `createSSHSession` / `createLocalSSHSession` / `SSHSessionError` from `./ssh/createSSHSession.js`
- `src/main.tsx:4106` — commander `program.command('ssh <host> [dir]')` registration with `--permission-mode`, `--dangerously-skip-permissions`, `--local` options
- `src/hooks/useSSHSession.ts` (241 lines, real implementation) — REPL session hook, calls `session.createManager({onMessage, onPermissionRequest})`
- `src/screens/REPL.tsx:1466` — `const sshRemote = useSSHSession({...})` mounted in REPL

Backend is **stub**:

- `src/ssh/createSSHSession.ts` — 5 lines, just `export interface SSHSession { id: string }` and `export {}`. No `createSSHSession`, no `createLocalSSHSession`, no `SSHSessionError`. `claude ssh host` would crash with `TypeError: createSSHSession is not a function` at `main.tsx:3258`.

### What to implement

The stub needs to export three things consumed by `main.tsx:3258`:

```typescript
export class SSHSessionError extends Error { ... }
export function createLocalSSHSession(opts: {...}): SSHSession  // --local e2e mode, no ssh/deploy
export function createSSHSession(opts: {...}): SSHSession        // full SSH path
```

And `SSHSession` must satisfy whatever shape `useSSHSession.ts` consumes — read that hook first to discover the contract (`session.createManager(...)` returns a manager with onMessage/onPermissionRequest hooks).

### CCB's architecture (per `ssh-remote.md`)

```
ccb ssh <host> [dir]
  ├── 1. SSHProbe: detect remote platform/arch, check for existing binary
  ├── 2. SSHDeploy: rsync/scp dist/ to remote
  ├── 3. SSHAuthProxy: local auth proxy
  │      ├─ Unix Socket (Linux/Mac)
  │      └─ TCP 127.0.0.1:<port> (Windows)
  └── 4. SSH -R reverse tunnel + spawn remote CLI
         ssh -R <remote>:<local> <host> \
             ANTHROPIC_BASE_URL=... \
             ANTHROPIC_AUTH_NONCE=... \
             /path/to/deployed/openclaude
```

Then the remote CLI's HTTP client routes through the tunnel back to the local auth proxy, which adds the real Anthropic credentials. The remote machine never sees the API key.

### Suggested module layout

```
src/ssh/
├── createSSHSession.ts    ← REPLACE stub. Top-level entry, assembles the others.
├── sshProbe.ts            ← NEW. Run `uname -ms` over ssh, check checksums of remote binary.
├── sshDeploy.ts           ← NEW. rsync/scp dist/ to remote (reuse Bun's binary if rsync absent).
├── sshAuthProxy.ts        ← NEW. Local TCP/UDS server forwarding to ANTHROPIC_BASE_URL with real auth header.
├── sshSession.ts          ← NEW. SSHSession class wrapping the spawned ssh subprocess + IPC manager.
└── sshSessionError.ts     ← NEW. Typed errors (ProbeFailed, DeployFailed, ConnectionLost, AuthProxyDown).
```

### Effort breakdown

- Read `useSSHSession.ts` to nail down the SSHSession contract: 30 min
- Read CCB's `ssh-remote.md` carefully: 30 min
- `sshSessionError.ts` + types: 1h
- `sshProbe.ts`: 4h (bun's `child_process` for ssh, parse uname output, sha256 checksum compare)
- `sshDeploy.ts`: 6h (handle rsync/scp fallback, progress bar, perm fix, sudo prompt UX)
- `sshAuthProxy.ts`: 1 day (HTTP proxy, header injection, nonce auth, both UDS + TCP modes)
- `sshSession.ts` + `createSSHSession.ts` + `createLocalSSHSession.ts`: 2 days (subprocess management, IPC over stdin/stdout JSON, manager createManager pattern matching what useSSHSession expects)
- `--local` mode for e2e testing: 4h (skip probe/deploy/ssh, spawn local Bun process with same env, exercise auth-proxy plumbing)
- Notice file `SshRemoteNotice.tsx`: 30 min
- CLAUDE.md entry: 30 min

**Total: 4–5 days of focused work.**

### Acceptance criteria

1. `claude ssh --local` starts a child Bun process with auth tunneled through the proxy. End-to-end test: child can call the API and get a response.
2. `claude ssh user@hostname` deploys the binary if absent, opens reverse tunnel, child REPL on remote works against local auth.
3. ESC in local REPL cleanly tears down the remote session.
4. Auth proxy never logs the actual API key.

---

## Phase 2 — ACP (Agent Client Protocol for Zed/Cursor)

### Current state in our repo

Nothing. No `src/services/acp/` directory, no `acp` references in source. Pure greenfield.

### What ACP is

A standardized stdio NDJSON protocol that lets IDEs (Zed has it built-in; Cursor and others adopting) drive an external AI agent process. The IDE spawns the agent as a child process, communicates over stdin/stdout in newline-delimited JSON, and renders the agent's responses in its native chat UI.

This is the major user-facing feature missing — Zed users especially want this. Our existing Emacs integration uses the Claude IDE protocol (a different beast); ACP is the broader cross-IDE standard.

### Core capabilities (per CCB's `acp-zed.md`)

- Session lifecycle: new / load / fork / close / restore from history
- History replay: when restoring a session, replay the prior turn history to the IDE
- Permission bridging: ACP's permission decisions map to our existing tool-permission system
- Slash commands & skills: surface our `/commit`, `/review`, etc. via ACP's command-list
- Context window tracking: emit `usage_update` events with model-prefix matching
- Prompt queueing: handle multiple prompts arriving back-to-back
- Mode switching: auto / default / acceptEdits / plan / dontAsk / bypassPermissions
- Runtime model switching

### Architecture

```
┌──────────────┐    NDJSON/stdio    ┌──────────────────┐
│  Zed / IDE   │ ◄────────────────► │  openclaude      │
│  (Client)    │   stdin / stdout   │  ACP Agent       │
└──────────────┘                    │                  │
                                    │  entry.ts        │ ← stdio → NDJSON stream
                                    │  agent.ts        │ ← protocol handler
                                    │  session.ts      │ ← session state machine
                                    │  permissions.ts  │ ← bridge to our perm system
                                    │  commands.ts     │ ← surface our slash commands
```

### Suggested module layout

```
src/services/acp/
├── entry.ts              ← stdio NDJSON reader + writer, line buffering
├── agent.ts              ← top-level protocol dispatcher
├── protocol.ts           ← Zod schemas for every ACP message type (request + response)
├── session.ts            ← per-session state, history, mode, model
├── sessionStore.ts       ← persist sessions to ~/.claude/acp-sessions/, restore on load
├── permissionBridge.ts   ← translate ACP permission requests ↔ our useCanUseTool path
├── commandsSurface.ts    ← enumerate our slash commands as ACP commands
├── usageEmitter.ts       ← emit usage_update events with token + cost calc
└── types.ts              ← ACP message type definitions
```

### Entry point wiring

ACP mode needs a CLI flag — probably `--acp` or auto-detected from `process.env.ACP=1` (Zed sets this when spawning). When detected:

- Skip the REPL render
- Don't write to stderr (corrupts the NDJSON stream)
- Hand control to `src/services/acp/entry.ts`

Add this branch early in `main.tsx`, similar to how `--print`/`-p` non-interactive mode short-circuits.

### CCB's ACP source location

CCB ships their ACP impl at `packages/<something>/src/services/acp/` in their repo. Read it directly:

```bash
find /tmp/ccb-docs/packages -path '*/acp/*' -type f 2>/dev/null
find /tmp/ccb-docs -path '*/services/acp/*' -type f 2>/dev/null
```

The protocol spec (message types, request/response shape) is the load-bearing part. Steal their Zod schemas verbatim if licensing allows; otherwise re-derive from the published ACP spec.

### Effort breakdown

- Study ACP protocol spec + read CCB's `acp-zed.md`: 1 day
- Read CCB's ACP source: 1 day
- `protocol.ts` (Zod schemas): 1 day
- `entry.ts` + `agent.ts` (dispatcher): 1 day
- `session.ts` + `sessionStore.ts`: 2 days
- `permissionBridge.ts`: 1 day (most fork-specific work — wiring to our existing perm system)
- `commandsSurface.ts` + `usageEmitter.ts`: 1 day
- Main.tsx wiring + `--acp` flag detection: 4h
- Test against Zed (real client): 1 day
- Notice file `AcpNotice.tsx` + CLAUDE.md entry: 1h

**Total: 8–10 days.**

### Acceptance criteria

1. Zed can spawn `openclaude --acp`, send a prompt, receive streaming response.
2. Tool calls trigger Zed's permission UI; user's decision flows back through ACP.
3. Closing and reopening Zed restores the session with full history.
4. `/commit` and other slash commands appear in Zed's command palette.

---

## Phase 3 — acp-link (WebSocket→stdio bridge)

### Current state

Nothing. Greenfield.

### What it is

An ACP agent only speaks stdio. acp-link is a small server that exposes a WebSocket endpoint, accepts a connection from a remote browser/client, and forwards the messages to a locally-spawned ACP agent's stdin/stdout. Combined with our Remote Control Server, it lets browser-based clients drive the local agent.

Per CCB's `acp-link.md`:

```
┌──────────────┐  WebSocket   ┌──────────────┐  stdio   ┌──────────────┐
│  Browser     │ ◄──────────► │  acp-link    │ ◄──────► │  ACP Agent   │
│  (WS Client) │              │  (Proxy)     │  spawn   │  (openclaude)│
└──────────────┘              └──────────────┘          └──────────────┘
```

Features:
- WebSocket → stdio bridging
- Session management (create, load, restore, list, close)
- Remote permission approval via WebSocket
- Optional RCS (Remote Control Server) integration — registers the ACP agent for Web UI access
- HTTPS support with self-signed cert generation
- Token authentication

### Suggested module layout

```
packages/acp-link/         ← Separate package — could be a sibling Bun workspace or a sub-CLI
├── src/
│   ├── server.ts          ← Bun WebSocket server
│   ├── bridge.ts          ← Per-connection bridge: spawn ACP agent, pipe stdin/stdout
│   ├── sessionRouter.ts   ← Multi-session: route WS messages to the right ACP agent process
│   ├── permissionRelay.ts ← Forward agent permission requests to WS client; route decisions back
│   ├── auth.ts            ← Bearer token verification
│   ├── tls.ts             ← Self-signed cert generation
│   └── rcsRegister.ts     ← Optional RCS integration
└── bin/acp-link.ts        ← CLI entry: `acp-link --port 8080 --token xxx`
```

Or build it as a subcommand: `claude acp-link start --port 8080`.

### Effort

- Server scaffolding + Bun WebSocket: 4h
- Bridge (spawn ACP child + pipe stdio): 1 day
- Multi-session routing: 1 day
- Permission relay: 4h
- Auth + TLS: 4h
- RCS integration: 4h
- CLI entry + docs: 4h

**Total: 3–5 days. Do not start until ACP is working.**

---

## Quality gates (apply to every phase)

Before marking any phase complete:

1. `bun run build` succeeds with zero output beyond the bundled-files line
2. Manually exercise the feature end-to-end (don't trust types alone)
3. Update CLAUDE.md "Key Architecture Decisions" with a one-paragraph entry
4. Add a notice file in `src/components/LogoV2/` (Phase 1, 2 — Phase 3 optional)
5. Update `fork-parity-audit.md`: row status from ❌/⚠️ to ✅, audit changelog entry
6. Commit with reference to CCB's source path so future-you knows where the inspiration came from
7. Update `CHANGELOG.md` in `coffeegrind123/changelog` repo

---

## Useful commands

```bash
# Build
bun run build

# Run from source (dev)
bun run src/entrypoints/cli.tsx

# Smoke test in interactive container
docker exec openclaude-interactive bash -c \
  'cd /opt/openclaude-src && IS_SANDBOX=1 bun run src/entrypoints/cli.tsx -p "test" --dangerously-skip-permissions'

# Hot-patch a single file into the running container (no rebuild)
docker cp src/path/to/file.ts openclaude-interactive:/opt/openclaude-src/src/path/to/file.ts

# Re-clone CCB if /tmp/ccb-docs is gone
git clone --depth 1 https://github.com/claude-code-best/claude-code.git /tmp/ccb-docs

# Find CCB's ACP source (path varies)
find /tmp/ccb-docs -path '*/acp/*' -type f 2>/dev/null

# Find CCB's SSH Remote source
find /tmp/ccb-docs -iname '*ssh*' -type f 2>/dev/null | head -20
```

---

## First actions for next session

1. Read this file (`ccb-port-kickoff.md`)
2. Read `CLAUDE.md` end-to-end
3. Read `fork-parity-audit.md` for the broader picture
4. Re-clone `/tmp/ccb-docs` if missing
5. Phase 1: read `src/hooks/useSSHSession.ts` (241 lines) to discover the SSHSession contract before writing the backend
6. Phase 1: read `/tmp/ccb-docs/docs/features/ssh-remote.md` for CCB's architecture
7. Then start implementing `src/ssh/createSSHSession.ts` and friends
