"""Harbor agent adapter for openclaude (coffeegrind123/openclaude).

openclaude is a Claude Code fork: it installs as the ``claude`` binary, accepts
the same ``--print --output-format=stream-json`` flags, and writes the identical
session-JSONL transcript format. So this adapter subclasses Harbor's
``ClaudeCode`` agent and inherits its entire ATIF trajectory parser,
``populate_context_post_run`` cost/token accounting, and MCP/skills/memory
registration verbatim.

Only four things differ from stock Claude Code, and only those are overridden:

* ``name()`` — registers as the ``openclaude`` agent.
* ``install()`` — fetches the fork's self-contained binary via its hosted
  installer (``https://cs16.net/openclaude/install.sh``) instead of the
  ``@anthropic-ai/claude-code`` npm package. The binary is a compiled Bun
  executable, so no Node runtime is required at run time.
* ``run()`` — the fork routes to z.ai / DeepSeek / NVIDIA NIM through
  ``ANTHROPIC_BASE_URL`` + ``ANTHROPIC_AUTH_TOKEN`` (HTTP ``Authorization:
  Bearer``). Stock ``ClaudeCode.run()`` collapses any token into
  ``ANTHROPIC_API_KEY`` (which becomes an ``x-api-key`` header) — those proxies
  reject that, so this override preserves ``ANTHROPIC_AUTH_TOKEN`` as a Bearer
  token. It also suppresses the fork's built-in MCP auto-install
  (browser/Ghidra/...) for lean benchmark runs unless Harbor explicitly
  requests MCP servers.
* ``_parse_total_cost_from_stream_json()`` — reads the fork's tee'd stdout log
  (``openclaude.txt``) instead of ``claude-code.txt``.

Drop this file into ``harbor/src/harbor/agents/installed/openclaude.py`` and
register it (see ``README.md`` / ``install-into-harbor.sh``).
"""

import json
import os
import shlex
from typing import override

from harbor.agents.installed.base import with_prompt_template
from harbor.agents.installed.claude_code import ClaudeCode
from harbor.environments.base import BaseEnvironment
from harbor.models.agent.context import AgentContext
from harbor.models.agent.name import AgentName
from harbor.models.trial.paths import EnvironmentPaths

# Harbor "provider/model" prefixes that are routing labels rather than part of
# the real upstream model id. For these, the segment after the first "/" is the
# model the fork should send (e.g. "zai/glm-4.6" -> "glm-4.6"). Anything else
# (notably NVIDIA NIM ids like "nvidia/llama-3.3-nemotron-super-49b-v1") keeps
# its full slug.
_ROUTING_PREFIXES = {"zai", "z-ai", "deepseek", "anthropic", "openclaude"}

# Optional provider/fork env vars forwarded into the run when present. These are
# all no-ops unless the user set them, so forwarding is always safe.
_PASSTHROUGH_ENV = (
    "NVIDIA_NIM_API_KEY",
    "ZAI_CUSTOMER_ID",
    "ZAI_SESSION_TOKEN",
    "ZAI_RPM_MODEL_CODE",
    "API_TIMEOUT_MS",
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS",
)


class OpenClaude(ClaudeCode):
    """openclaude — a Claude Code research fork that routes to z.ai / DeepSeek /
    NVIDIA NIM / Anthropic through an Anthropic-compatible endpoint."""

    SUPPORTS_ATIF: bool = True

    _OUTPUT_FILENAME = "openclaude.txt"

    @staticmethod
    @override
    def name() -> str:
        return AgentName.OPENCLAUDE.value

    @override
    def get_version_command(self) -> str | None:
        return 'export PATH="/usr/local/bin:$HOME/.local/bin:$PATH"; claude --version'

    @override
    async def install(self, environment: BaseEnvironment) -> None:
        # System deps: curl + ca-certificates to fetch the installer and reach
        # the API; git for repo operations; procps because the fork (like Claude
        # Code) shells out to ps/pgrep via node-tree-kill when reaping process
        # trees.
        await self.exec_as_root(
            environment,
            command=(
                "if command -v apk &> /dev/null; then"
                "  apk add --no-cache curl bash git procps ca-certificates;"
                " elif command -v apt-get &> /dev/null; then"
                "  apt-get update && apt-get install -y curl git procps ca-certificates;"
                " elif command -v yum &> /dev/null; then"
                "  yum install -y curl git procps-ng ca-certificates;"
                " else"
                '  echo "Warning: no known package manager found, assuming curl is available" >&2;'
                " fi"
            ),
            env={"DEBIAN_FRONTEND": "noninteractive"},
        )
        # The hosted installer downloads the matching openclaude-<platform>
        # binary from GitHub Releases and installs it as `claude` in
        # /usr/local/bin (falling back to ~/.local/bin). Override the endpoint
        # with OPENCLAUDE_UPDATE_ENDPOINT (e.g. to pin a mirror).
        endpoint = (
            self._get_env("OPENCLAUDE_UPDATE_ENDPOINT")
            or "https://cs16.net/openclaude"
        ).rstrip("/")
        # Resilient fetch: fail fast on a stalled connect and retry, so a
        # transient blip reaching the installer host doesn't burn the whole
        # agent-setup timeout on one hung connection.
        await self.exec_as_agent(
            environment,
            command=(
                "set -euo pipefail; "
                f"curl -fsSL --connect-timeout 30 --max-time 300 "
                f"--retry 5 --retry-delay 5 --retry-connrefused "
                f"{shlex.quote(endpoint + '/install.sh')} | bash && "
                "echo 'export PATH=\"/usr/local/bin:$HOME/.local/bin:$PATH\"' >> ~/.bashrc && "
                'export PATH="/usr/local/bin:$HOME/.local/bin:$PATH" && '
                "claude --version"
            ),
        )

    @override
    def _parse_total_cost_from_stream_json(self) -> float | None:
        """Read the authoritative ``total_cost_usd`` from the fork's tee'd
        stream-json stdout. Identical to the parent except for the filename."""
        stream_path = self.logs_dir / self._OUTPUT_FILENAME
        try:
            content = stream_path.read_text(encoding="utf-8")
        except OSError:
            return None
        for line in content.splitlines():
            line = line.strip()
            if not line or not line.startswith("{"):
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") == "result":
                cost = event.get("total_cost_usd")
                if cost is None:
                    return None
                try:
                    return float(cost)
                except (TypeError, ValueError):
                    return None
        return None

    def _resolve_model(self) -> str | None:
        """Resolve the model the fork should run.

        An explicit ``ANTHROPIC_MODEL`` in the environment always wins (this is
        how fork users configure z.ai/DeepSeek). Otherwise derive from Harbor's
        ``model_name``, stripping only a known routing prefix.
        """
        explicit = self._get_env("ANTHROPIC_MODEL")
        if explicit:
            return explicit
        if not self.model_name:
            return None
        model = self.model_name
        if "/" in model:
            prefix, rest = model.split("/", 1)
            if prefix.lower() in _ROUTING_PREFIXES:
                return rest
        return model

    @with_prompt_template
    async def run(
        self, instruction: str, environment: BaseEnvironment, context: AgentContext
    ) -> None:
        escaped_instruction = shlex.quote(instruction)

        base_url = self._get_env("ANTHROPIC_BASE_URL")
        auth_token = (self._get_env("ANTHROPIC_AUTH_TOKEN") or "").strip()
        api_key = (self._get_env("ANTHROPIC_API_KEY") or "").strip()

        if not auth_token and not api_key:
            raise RuntimeError(
                "openclaude needs credentials. Set ANTHROPIC_AUTH_TOKEN "
                "(Bearer — z.ai / DeepSeek / NIM) or ANTHROPIC_API_KEY "
                "(direct Anthropic)."
            )

        env: dict[str, str] = {}

        # Bearer-first: preserve ANTHROPIC_AUTH_TOKEN as a Bearer token. The
        # fork's proxies authenticate with it; downgrading to x-api-key fails.
        if auth_token:
            env["ANTHROPIC_AUTH_TOKEN"] = auth_token
        if api_key:
            env["ANTHROPIC_API_KEY"] = api_key
        if base_url:
            env["ANTHROPIC_BASE_URL"] = base_url

        model = self._resolve_model()
        if model:
            env["ANTHROPIC_MODEL"] = model
            # With a custom base URL (z.ai/DeepSeek/NIM) pin every model alias to
            # the single benchmarked model so the small/fast (Haiku) and subagent
            # routes don't silently fall back to a different model.
            if base_url:
                env["ANTHROPIC_DEFAULT_SONNET_MODEL"] = model
                env["ANTHROPIC_DEFAULT_OPUS_MODEL"] = model
                env["ANTHROPIC_DEFAULT_HAIKU_MODEL"] = model
                env["CLAUDE_CODE_SUBAGENT_MODEL"] = model

        # Forward optional provider/fork env knobs when present.
        for key in _PASSTHROUGH_ENV:
            val = self._get_env(key)
            if val:
                env[key] = val

        # Telemetry off; allow bypassPermissions when running as root in a
        # container (the fork also defaults to bypass, but be explicit).
        env["CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"] = "1"
        env["IS_SANDBOX"] = "1"
        env["FORCE_AUTO_BACKGROUND_TASKS"] = "1"
        env["ENABLE_BACKGROUND_TASKS"] = "1"

        # Keep benchmark runs lean: skip the fork's built-in MCP auto-install
        # (browser/Ghidra/computer-use/VoxCPM/Cheat-Engine) unless Harbor asked
        # for MCP servers, in which case the inherited registration wires them.
        if not self.mcp_servers:
            env.setdefault("OPENCLAUDE_SKIP_MCP_INSTALL", "1")

        # Disable adaptive thinking if requested (parity with stock).
        if (self._get_env("CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING") or "").strip() == "1":
            env["CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING"] = "1"

        # Merge declarative env vars (e.g. MAX_THINKING_TOKENS) from ENV_VARS.
        env.update(self._resolved_env_vars)

        # Isolate the session/config dir so the inherited _get_session_dir()
        # finds exactly one transcript to convert.
        env["CLAUDE_CONFIG_DIR"] = (EnvironmentPaths.agent_dir / "sessions").as_posix()

        # Drop empty values so the CLI can pick the right auth method.
        env = {k: v for k, v in env.items() if v}

        setup_command = (
            "mkdir -p $CLAUDE_CONFIG_DIR/debug $CLAUDE_CONFIG_DIR/projects/-app "
            "$CLAUDE_CONFIG_DIR/shell-snapshots $CLAUDE_CONFIG_DIR/statsig "
            "$CLAUDE_CONFIG_DIR/todos $CLAUDE_CONFIG_DIR/skills && "
            "if [ -d ~/.claude/skills ]; then "
            "cp -r ~/.claude/skills/. $CLAUDE_CONFIG_DIR/skills/ 2>/dev/null || true; "
            "fi"
        )

        skills_command = self._build_register_skills_command()
        if skills_command:
            setup_command += f" && {skills_command}"

        memory_command = self._build_register_memory_command()
        if memory_command:
            setup_command += f" && {memory_command}"

        mcp_command = self._build_register_mcp_servers_command()
        if mcp_command:
            setup_command += f" && {mcp_command}"

        cli_flags = self.build_cli_flags()
        extra_flags = (cli_flags + " ") if cli_flags else ""

        await self.exec_as_agent(environment, command=setup_command, env=env)
        await self.exec_as_agent(
            environment,
            command=(
                'export PATH="/usr/local/bin:$HOME/.local/bin:$PATH"; '
                f"claude --verbose --output-format=stream-json "
                f"{extra_flags}"
                f"--print -- {escaped_instruction} 2>&1 </dev/null | tee "
                f"/logs/agent/{self._OUTPUT_FILENAME}"
            ),
            env=env,
        )
