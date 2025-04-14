from unittest.mock import patch, MagicMock

import pytest

from flow_portal import AgentFramework, AgentConfig, AnyAgent
from flow_portal.tools import (
    search_web,
    visit_webpage,
)


def test_load_agno_default():
    mock_agent = MagicMock()
    mock_model = MagicMock()

    with (
        patch("flow_portal.frameworks.agno.Agent", mock_agent),
        patch("flow_portal.frameworks.agno.LiteLLM", mock_model),
    ):
        AnyAgent.create(AgentFramework.AGNO, AgentConfig(model_id="gpt-4o"))
        mock_agent.assert_called_once_with(
            name="flow_portal",
            instructions="",
            model=mock_model(model="gpt-4o"),
            tools=[search_web, visit_webpage],
        )


def test_load_agno_agent_missing():
    with patch("flow_portal.frameworks.agno.agno_available", False):
        with pytest.raises(ImportError):
            AnyAgent.create(AgentFramework.AGNO, AgentConfig(model_id="gpt-4o"))
