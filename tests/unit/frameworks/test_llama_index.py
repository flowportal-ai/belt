from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from flow_portal import AgentConfig, AgentFramework, AnyAgent
from flow_portal.tools import (
    search_web,
    visit_webpage,
)


def test_load_llama_index_agent_default() -> None:
    model_mock = MagicMock()
    create_mock = MagicMock()
    agent_mock = MagicMock()
    create_mock.return_value = agent_mock
    tool_mock = MagicMock()
    from llama_index.core.tools import FunctionTool

    with (
        patch("flow_portal.frameworks.llama_index.DEFAULT_AGENT_TYPE", create_mock),
        patch("flow_portal.frameworks.llama_index.DEFAULT_MODEL_TYPE", model_mock),
        patch.object(FunctionTool, "from_defaults", tool_mock),
    ):
        AnyAgent.create(
            AgentFramework.LLAMA_INDEX,
            AgentConfig(
                model_id="gemini/gemini-2.0-flash",
                instructions="You are a helpful assistant",
            ),
        )

        model_mock.assert_called_once_with(
            model="gemini/gemini-2.0-flash", api_key=None, api_base=None
        )
        create_mock.assert_called_once_with(
            name="flow_portal",
            llm=model_mock.return_value,
            system_prompt="You are a helpful assistant",
            description="The main agent",
            tools=[tool_mock(search_web), tool_mock(visit_webpage)],
        )


def test_load_llama_index_agent_missing() -> None:
    with patch("flow_portal.frameworks.llama_index.llama_index_available", False):
        with pytest.raises(ImportError):
            AnyAgent.create(AgentFramework.LLAMA_INDEX, AgentConfig(model_id="gpt-4o"))


def test_load_llama_index_multiagent() -> None:
    model_mock = MagicMock()
    create_mock = MagicMock()
    agent_mock = MagicMock()
    create_mock.return_value = agent_mock
    tool_mock = MagicMock()
    from llama_index.core.tools import FunctionTool

    with (
        patch("flow_portal.frameworks.llama_index.DEFAULT_AGENT_TYPE", create_mock),
        patch("flow_portal.frameworks.llama_index.AgentWorkflow"),
        patch("flow_portal.frameworks.llama_index.DEFAULT_MODEL_TYPE", model_mock),
        patch.object(FunctionTool, "from_defaults", tool_mock),
    ):
        main_agent = AgentConfig(model_id="gpt-4.1-mini")

        managed_agents = [
            AgentConfig(
                model_id="gpt-4.1-nano",
                tools=[
                    search_web,
                    visit_webpage,
                ],
            ),
        ]

        AnyAgent.create(
            AgentFramework.LLAMA_INDEX, main_agent, managed_agents=managed_agents
        )

        create_mock.assert_any_call(
            name="managed_agent_0",
            description="A managed agent",
            llm=model_mock.return_value,
            tools=[
                tool_mock(search_web),
                tool_mock(visit_webpage),
            ],
            system_prompt=None,
            can_handoff_to=["flow_portal"],
        )

        create_mock.assert_called_with(
            name="flow_portal",
            description="The main agent",
            llm=model_mock.return_value,
            system_prompt=None,
            can_handoff_to=["managed_agent_0"],
            tools=[],
        )


def test_run_llama_index_agent_custom_args() -> None:
    create_mock = MagicMock()
    agent_mock = AsyncMock()
    create_mock.return_value = agent_mock
    from llama_index.core.tools import FunctionTool

    with (
        patch("flow_portal.frameworks.llama_index.DEFAULT_AGENT_TYPE", create_mock),
        patch("flow_portal.frameworks.llama_index.DEFAULT_MODEL_TYPE"),
        patch.object(FunctionTool, "from_defaults"),
    ):
        agent = AnyAgent.create(
            AgentFramework.LLAMA_INDEX,
            AgentConfig(
                model_id="gemini/gemini-2.0-flash",
                instructions="You are a helpful assistant",
            ),
        )
        agent.run("foo", timeout=10)
        agent_mock.run.assert_called_once_with("foo", timeout=10)
