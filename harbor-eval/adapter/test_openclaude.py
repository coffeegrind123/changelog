"""Unit tests for the openclaude Harbor adapter — install, auth wiring,
provider/model routing, MCP-skip default, and stream-json cost parsing.

Drop into ``harbor/tests/unit/agents/installed/test_openclaude.py`` (it relies
on the ``temp_dir`` fixture in ``tests/conftest.py``).
"""

from unittest.mock import AsyncMock

import pytest

from harbor.agents.installed.openclaude import OpenClaude
from harbor.models.agent.name import AgentName


def _mock_env():
    """An AsyncMock BaseEnvironment whose exec() always succeeds."""
    env = AsyncMock()
    env.default_user = "agent"
    env.exec.return_value = AsyncMock(return_code=0, stdout="", stderr="")
    return env


def _exec_calls(mock_env):
    return mock_env.exec.call_args_list


def _exec_envs(mock_env):
    """All env dicts passed to environment.exec() during run()."""
    return [c.kwargs.get("env", {}) for c in _exec_calls(mock_env)]


def _run_call(mock_env):
    """The exec call carrying the main `claude --print` run command."""
    for call in _exec_calls(mock_env):
        cmd = call.kwargs.get("command", "")
        if "--output-format=stream-json" in cmd and "--print" in cmd:
            return call
    raise AssertionError("no openclaude run command found")


def _clear_env(monkeypatch):
    for var in (
        "ANTHROPIC_API_KEY",
        "ANTHROPIC_AUTH_TOKEN",
        "ANTHROPIC_BASE_URL",
        "ANTHROPIC_MODEL",
        "CLAUDE_CODE_OAUTH_TOKEN",
        "CLAUDE_CODE_MAX_OUTPUT_TOKENS",
        "MAX_THINKING_TOKENS",
        "NVIDIA_NIM_API_KEY",
        "ZAI_CUSTOMER_ID",
        "ZAI_SESSION_TOKEN",
        "ZAI_RPM_MODEL_CODE",
        "OPENCLAUDE_SKIP_MCP_INSTALL",
        "OPENCLAUDE_UPDATE_ENDPOINT",
        "CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING",
    ):
        monkeypatch.delenv(var, raising=False)


def test_name():
    assert OpenClaude.name() == AgentName.OPENCLAUDE.value == "openclaude"


class TestInstall:
    @pytest.mark.asyncio
    async def test_uses_hosted_installer(self, monkeypatch, temp_dir):
        _clear_env(monkeypatch)
        agent = OpenClaude(logs_dir=temp_dir, model_name="zai/glm-4.6")
        mock_env = _mock_env()
        await agent.install(mock_env)
        cmds = [c.kwargs.get("command", "") for c in _exec_calls(mock_env)]
        joined = "\n".join(cmds)
        assert "cs16.net/openclaude/install.sh" in joined
        assert "| bash" in joined
        assert "claude --version" in joined

    @pytest.mark.asyncio
    async def test_endpoint_override(self, monkeypatch, temp_dir):
        _clear_env(monkeypatch)
        monkeypatch.setenv("OPENCLAUDE_UPDATE_ENDPOINT", "https://mirror.example/oc/")
        agent = OpenClaude(logs_dir=temp_dir, model_name="zai/glm-4.6")
        mock_env = _mock_env()
        await agent.install(mock_env)
        joined = "\n".join(c.kwargs.get("command", "") for c in _exec_calls(mock_env))
        assert "https://mirror.example/oc/install.sh" in joined
        assert "cs16.net" not in joined


class TestRunAuth:
    @pytest.mark.asyncio
    async def test_zai_bearer_token_preserved(self, monkeypatch, temp_dir):
        """z.ai authenticates via Bearer — the token must stay in
        ANTHROPIC_AUTH_TOKEN, NOT be downgraded to ANTHROPIC_API_KEY."""
        _clear_env(monkeypatch)
        monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "zai-bearer-tok")
        monkeypatch.setenv("ANTHROPIC_BASE_URL", "https://api.z.ai/api/anthropic")
        agent = OpenClaude(logs_dir=temp_dir, model_name="zai/glm-4.6")
        mock_env = _mock_env()
        await agent.run("do something", mock_env, AsyncMock())
        env = _run_call(mock_env).kwargs["env"]
        assert env["ANTHROPIC_AUTH_TOKEN"] == "zai-bearer-tok"
        assert "ANTHROPIC_API_KEY" not in env
        assert env["ANTHROPIC_BASE_URL"] == "https://api.z.ai/api/anthropic"

    @pytest.mark.asyncio
    async def test_no_credentials_raises(self, monkeypatch, temp_dir):
        _clear_env(monkeypatch)
        agent = OpenClaude(logs_dir=temp_dir, model_name="zai/glm-4.6")
        mock_env = _mock_env()
        with pytest.raises(RuntimeError, match="ANTHROPIC_AUTH_TOKEN"):
            await agent.run("do something", mock_env, AsyncMock())

    @pytest.mark.asyncio
    async def test_direct_anthropic_api_key(self, monkeypatch, temp_dir):
        """No base URL → direct Anthropic; api key kept and the provider prefix
        is stripped from the model id (no alias mirroring without a base URL)."""
        _clear_env(monkeypatch)
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-xyz")
        agent = OpenClaude(
            logs_dir=temp_dir, model_name="anthropic/claude-sonnet-4-6"
        )
        mock_env = _mock_env()
        await agent.run("do something", mock_env, AsyncMock())
        env = _run_call(mock_env).kwargs["env"]
        assert env["ANTHROPIC_API_KEY"] == "sk-ant-xyz"
        assert env["ANTHROPIC_MODEL"] == "claude-sonnet-4-6"
        assert "ANTHROPIC_DEFAULT_HAIKU_MODEL" not in env  # no base URL → no mirror


class TestModelRouting:
    @pytest.mark.asyncio
    async def test_routing_prefix_stripped_and_aliases_mirrored(
        self, monkeypatch, temp_dir
    ):
        _clear_env(monkeypatch)
        monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "tok")
        monkeypatch.setenv("ANTHROPIC_BASE_URL", "https://api.deepseek.com/anthropic")
        agent = OpenClaude(logs_dir=temp_dir, model_name="deepseek/deepseek-v4-pro")
        mock_env = _mock_env()
        await agent.run("x", mock_env, AsyncMock())
        env = _run_call(mock_env).kwargs["env"]
        assert env["ANTHROPIC_MODEL"] == "deepseek-v4-pro"
        for alias in (
            "ANTHROPIC_DEFAULT_SONNET_MODEL",
            "ANTHROPIC_DEFAULT_OPUS_MODEL",
            "ANTHROPIC_DEFAULT_HAIKU_MODEL",
            "CLAUDE_CODE_SUBAGENT_MODEL",
        ):
            assert env[alias] == "deepseek-v4-pro"

    @pytest.mark.asyncio
    async def test_nim_model_slug_kept_full(self, monkeypatch, temp_dir):
        """A real namespaced model id (NVIDIA NIM) must NOT be prefix-stripped."""
        _clear_env(monkeypatch)
        monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "tok")
        monkeypatch.setenv("ANTHROPIC_BASE_URL", "https://integrate.api.nvidia.com")
        model = "nvidia/llama-3.3-nemotron-super-49b-v1"
        agent = OpenClaude(logs_dir=temp_dir, model_name=model)
        mock_env = _mock_env()
        await agent.run("x", mock_env, AsyncMock())
        env = _run_call(mock_env).kwargs["env"]
        assert env["ANTHROPIC_MODEL"] == model

    @pytest.mark.asyncio
    async def test_explicit_env_model_wins(self, monkeypatch, temp_dir):
        _clear_env(monkeypatch)
        monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "tok")
        monkeypatch.setenv("ANTHROPIC_BASE_URL", "https://api.z.ai/api/anthropic")
        monkeypatch.setenv("ANTHROPIC_MODEL", "glm-4.7")
        agent = OpenClaude(logs_dir=temp_dir, model_name="zai/glm-4.6")
        mock_env = _mock_env()
        await agent.run("x", mock_env, AsyncMock())
        env = _run_call(mock_env).kwargs["env"]
        assert env["ANTHROPIC_MODEL"] == "glm-4.7"


class TestForkEnvDefaults:
    @pytest.mark.asyncio
    async def test_skip_mcp_and_sandbox_defaults(self, monkeypatch, temp_dir):
        _clear_env(monkeypatch)
        monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "tok")
        monkeypatch.setenv("ANTHROPIC_BASE_URL", "https://api.z.ai/api/anthropic")
        agent = OpenClaude(logs_dir=temp_dir, model_name="zai/glm-4.6")
        mock_env = _mock_env()
        await agent.run("x", mock_env, AsyncMock())
        env = _run_call(mock_env).kwargs["env"]
        assert env["OPENCLAUDE_SKIP_MCP_INSTALL"] == "1"
        assert env["IS_SANDBOX"] == "1"
        assert env["CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"] == "1"

    @pytest.mark.asyncio
    async def test_passthrough_env_forwarded(self, monkeypatch, temp_dir):
        _clear_env(monkeypatch)
        monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "tok")
        monkeypatch.setenv("ANTHROPIC_BASE_URL", "https://integrate.api.nvidia.com")
        monkeypatch.setenv("NVIDIA_NIM_API_KEY", "nim-key")
        monkeypatch.setenv("API_TIMEOUT_MS", "600000")
        agent = OpenClaude(logs_dir=temp_dir, model_name="nvidia/foo")
        mock_env = _mock_env()
        await agent.run("x", mock_env, AsyncMock())
        env = _run_call(mock_env).kwargs["env"]
        assert env["NVIDIA_NIM_API_KEY"] == "nim-key"
        assert env["API_TIMEOUT_MS"] == "600000"

    @pytest.mark.asyncio
    async def test_run_command_shape(self, monkeypatch, temp_dir):
        _clear_env(monkeypatch)
        monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "tok")
        monkeypatch.setenv("ANTHROPIC_BASE_URL", "https://api.z.ai/api/anthropic")
        agent = OpenClaude(logs_dir=temp_dir, model_name="zai/glm-4.6")
        mock_env = _mock_env()
        await agent.run("solve it", mock_env, AsyncMock())
        cmd = _run_call(mock_env).kwargs["command"]
        assert "claude --verbose --output-format=stream-json" in cmd
        assert "--print --" in cmd
        assert "tee /logs/agent/openclaude.txt" in cmd
        # inherited default permission mode
        assert "--permission-mode=bypassPermissions" in cmd


class TestCostParsing:
    def test_reads_openclaude_txt(self, temp_dir):
        agent = OpenClaude(logs_dir=temp_dir, model_name="zai/glm-4.6")
        (temp_dir / "openclaude.txt").write_text(
            '{"type":"system","subtype":"init"}\n'
            '{"type":"result","subtype":"success","total_cost_usd":0.0123}\n'
        )
        assert agent._parse_total_cost_from_stream_json() == pytest.approx(0.0123)

    def test_missing_file_returns_none(self, temp_dir):
        agent = OpenClaude(logs_dir=temp_dir, model_name="zai/glm-4.6")
        assert agent._parse_total_cost_from_stream_json() is None
