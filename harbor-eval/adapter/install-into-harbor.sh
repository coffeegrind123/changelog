#!/usr/bin/env bash
# Install the openclaude agent adapter into a Harbor checkout.
#
# Usage:
#   ./install-into-harbor.sh /path/to/harbor
#   HARBOR_DIR=/path/to/harbor ./install-into-harbor.sh
#
# Idempotent: copies openclaude.py + test_openclaude.py and registers the
# agent in AgentName (name.py) and AgentFactory._AGENT_MAP (factory.py).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HARBOR_DIR="${1:-${HARBOR_DIR:-}}"

if [ -z "$HARBOR_DIR" ]; then
  echo "usage: $0 /path/to/harbor   (or set HARBOR_DIR)" >&2
  exit 2
fi
if [ ! -f "$HARBOR_DIR/src/harbor/agents/factory.py" ]; then
  echo "error: '$HARBOR_DIR' does not look like a harbor checkout" \
       "(missing src/harbor/agents/factory.py)" >&2
  exit 1
fi

ADAPTER_DST="$HARBOR_DIR/src/harbor/agents/installed/openclaude.py"
TEST_DST="$HARBOR_DIR/tests/unit/agents/installed/test_openclaude.py"

cp "$HERE/openclaude.py" "$ADAPTER_DST"
echo "copied -> $ADAPTER_DST"
if [ -d "$(dirname "$TEST_DST")" ]; then
  cp "$HERE/test_openclaude.py" "$TEST_DST"
  echo "copied -> $TEST_DST"
fi

python3 - "$HARBOR_DIR" <<'PY'
import re, sys
from pathlib import Path

harbor = Path(sys.argv[1])

# 1) Register the enum member in AgentName.
name_py = harbor / "src/harbor/models/agent/name.py"
text = name_py.read_text()
if 'OPENCLAUDE = "openclaude"' not in text:
    # Insert right after the CLAUDE_CODE member to keep the family together.
    text, n = re.subn(
        r'(\n([ \t]*)CLAUDE_CODE = "claude-code"\n)',
        r'\1\2OPENCLAUDE = "openclaude"\n',
        text,
        count=1,
    )
    if n != 1:
        sys.exit("could not locate CLAUDE_CODE member in name.py")
    name_py.write_text(text)
    print("patched name.py: + OPENCLAUDE")
else:
    print("name.py already has OPENCLAUDE")

# 2) Register the class in AgentFactory._AGENT_MAP.
factory_py = harbor / "src/harbor/agents/factory.py"
text = factory_py.read_text()
if "AgentName.OPENCLAUDE:" not in text:
    text, n = re.subn(
        r'(\n([ \t]*)AgentName\.CLAUDE_CODE: "harbor\.agents\.installed\.claude_code:ClaudeCode",\n)',
        r'\1\2AgentName.OPENCLAUDE: "harbor.agents.installed.openclaude:OpenClaude",\n',
        text,
        count=1,
    )
    if n != 1:
        sys.exit("could not locate CLAUDE_CODE entry in factory._AGENT_MAP")
    factory_py.write_text(text)
    print("patched factory.py: + AgentName.OPENCLAUDE")
else:
    print("factory.py already has AgentName.OPENCLAUDE")
PY

echo "done. verify with:  cd '$HARBOR_DIR' && python -c \"from harbor.agents.factory import AgentFactory; from harbor.models.agent.name import AgentName; print(AgentFactory.get_agent_class(AgentName.OPENCLAUDE))\""
