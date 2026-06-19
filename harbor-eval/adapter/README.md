# openclaude → Harbor agent adapter

Lets [Harbor](https://github.com/harbor-framework/harbor) (the agent-evaluation
framework behind Terminal-Bench) run **openclaude** as a benchmarkable agent,
side by side with Claude Code, Codex, Hermes, pi.dev, and the rest.

openclaude is a Claude Code fork, so this adapter is a thin subclass of Harbor's
`ClaudeCode` agent — it inherits the entire ATIF trajectory parser, token/cost
accounting, and MCP/skills/memory registration unchanged. Only what actually
differs is overridden:

| Override | Why |
|---|---|
| `name()` | registers as the `openclaude` agent |
| `install()` | installs the fork's self-contained Bun binary via `https://cs16.net/openclaude/install.sh` (no Node runtime needed) instead of the `@anthropic-ai/claude-code` npm package |
| `run()` | preserves `ANTHROPIC_AUTH_TOKEN` as an **HTTP Bearer** token (z.ai / DeepSeek / NVIDIA NIM authenticate this way — stock `ClaudeCode` collapses it into an `x-api-key`, which those proxies reject); mirrors model aliases for single-model parity; sets `OPENCLAUDE_SKIP_MCP_INSTALL=1` so the fork's built-in MCP servers (browser/Ghidra/…) don't auto-install on lean benchmark runs |
| `_parse_total_cost_from_stream_json()` | reads the tee'd `openclaude.txt` stdout log |

## Install into a Harbor checkout

```bash
git clone https://github.com/harbor-framework/harbor.git
./install-into-harbor.sh /path/to/harbor
```

The script copies `openclaude.py` + `test_openclaude.py` into Harbor and
idempotently registers the agent in two places:

1. `src/harbor/models/agent/name.py` — adds `OPENCLAUDE = "openclaude"` to the
   `AgentName` enum.
2. `src/harbor/agents/factory.py` — adds
   `AgentName.OPENCLAUDE: "harbor.agents.installed.openclaude:OpenClaude"` to
   `AgentFactory._AGENT_MAP`.

Verify:

```bash
cd /path/to/harbor
python -c "from harbor.agents.factory import AgentFactory; \
from harbor.models.agent.name import AgentName; \
print(AgentFactory.get_agent_class(AgentName.OPENCLAUDE))"
# -> <class 'harbor.agents.installed.openclaude.OpenClaude'>

uv run pytest tests/unit/agents/installed/test_openclaude.py -q
```

## Running an evaluation

openclaude is provider-agnostic. Point it at any Anthropic-compatible endpoint
with the same env vars the fork uses.

**z.ai (GLM) — the primary target:**
```bash
export ANTHROPIC_BASE_URL="https://api.z.ai/anthropic"   # note: /anthropic, not /api/anthropic
export ANTHROPIC_AUTH_TOKEN="<your z.ai token>"           # Bearer; never commit it
harbor run --agent openclaude --model zai/glm-5.2 --dataset terminal-bench ...
```
The `zai/` prefix is stripped, so `glm-5.2` is sent to z.ai. (z.ai exposes both
`https://api.z.ai/anthropic` and `https://api.z.ai/api/anthropic` — use whichever
your account/plan is provisioned for; the adapter forwards it verbatim.)

**DeepSeek:**
```bash
export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
export ANTHROPIC_AUTH_TOKEN="<deepseek token>"
harbor run --agent openclaude --model deepseek/deepseek-v4-pro ...
```

**Direct Anthropic:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
harbor run --agent openclaude --model anthropic/claude-sonnet-4-6 ...
```

### Model id rules

- An explicit `ANTHROPIC_MODEL` in the environment always wins.
- Otherwise Harbor's `--model provider/model` is used. A leading routing prefix
  (`zai/`, `deepseek/`, `anthropic/`, `openclaude/`) is stripped so the upstream
  model id is sent (`zai/glm-4.6` → `glm-4.6`). Real namespaced ids such as NIM's
  `nvidia/llama-3.3-nemotron-super-49b-v1` are kept whole.
- With a custom `ANTHROPIC_BASE_URL`, every model alias (Sonnet/Opus/Haiku/
  subagent) is pinned to the one benchmarked model so the small/fast and subagent
  routes can't silently diverge.

### Optional env knobs (forwarded when set)

`NVIDIA_NIM_API_KEY`, `ZAI_CUSTOMER_ID`, `ZAI_SESSION_TOKEN`, `ZAI_RPM_MODEL_CODE`,
`API_TIMEOUT_MS`, `CLAUDE_CODE_MAX_OUTPUT_TOKENS`, `OPENCLAUDE_UPDATE_ENDPOINT`
(installer mirror), and the inherited Claude Code CLI flags
(`--effort`, `--thinking`, `--max-turns`, `--permission-mode`, …).

## Notes / limitations

- **Lean by default:** built-in MCP servers are skipped
  (`OPENCLAUDE_SKIP_MCP_INSTALL=1`) unless Harbor requests MCP servers, in which
  case the inherited Claude Code MCP registration wires them into
  `~/.claude.json`.
- **Version pinning:** the hosted installer always fetches the latest release;
  the running version is auto-detected post-install via `claude --version`.
- Targets Linux container environments (the Harbor norm). The binary is a
  compiled Bun executable; only `curl`, `git`, `ca-certificates`, and `procps`
  are required in the image.
