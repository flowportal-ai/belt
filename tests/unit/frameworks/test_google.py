from unittest.mock import patch, MagicMock

from flow_portal import AgentFramework, AgentConfig, AnyAgent
from flow_portal.tools import (
    search_web,
    show_final_answer,
    visit_webpage,
)


def test_load_google_default():
    from google.adk.tools import FunctionTool

    mock_agent = MagicMock()
    mock_model = MagicMock()
    mock_function_tool = MagicMock()

    class MockedFunctionTool(FunctionTool):
        def __new__(cls, *args, **kwargs):
            return mock_function_tool

    with (
        patch("flow_portal.frameworks.google.Agent", mock_agent),
        patch("flow_portal.frameworks.google.LiteLlm", mock_model),
        patch("google.adk.tools.FunctionTool", MockedFunctionTool),
    ):
        AnyAgent.create(AgentFramework.GOOGLE, AgentConfig(model_id="gpt-4o"))
        mock_agent.assert_called_once_with(
            name="flow_portal",
            instruction="",
            model=mock_model(model="gpt-4o"),
            tools=[MockedFunctionTool(search_web), MockedFunctionTool(visit_webpage)],
            sub_agents=[],
            output_key="response",
        )


def test_load_google_multiagent():
    from google.adk.tools import FunctionTool

    mock_agent = MagicMock()
    mock_model = MagicMock()
    mock_agent_tool = MagicMock()
    mock_function_tool = MagicMock()

    class MockedFunctionTool(FunctionTool):
        def __new__(cls, *args, **kwargs):
            return mock_function_tool

    with (
        patch("flow_portal.frameworks.google.Agent", mock_agent),
        patch("flow_portal.frameworks.google.LiteLlm", mock_model),
        patch("flow_portal.frameworks.google.AgentTool", mock_agent_tool),
        patch("google.adk.tools.FunctionTool", MockedFunctionTool),
    ):
        AnyAgent.create(
            AgentFramework.GOOGLE,
            AgentConfig(model_id="gpt-4o"),
            managed_agents=[
                AgentConfig(
                    model_id="gpt-4o-mini",
                    name="search-web-agent",
                    tools=[
                        "flow_portal.tools.search_web",
                        "flow_portal.tools.visit_webpage",
                    ],
                ),
                AgentConfig(
                    model_id="gpt-4o-mini",
                    name="communication-agent",
                    tools=["flow_portal.tools.show_final_answer"],
                    handoff=True,
                ),
            ],
        )
        mock_agent.assert_any_call(
            model=mock_model(model="gpt-4o-mini"),
            instruction="",
            name="search-web-agent",
            tools=[MockedFunctionTool(search_web), MockedFunctionTool(visit_webpage)],
        )
        mock_agent.assert_any_call(
            model=mock_model(model="gpt-4o-mini"),
            instruction="",
            name="communication-agent",
            tools=[MockedFunctionTool(show_final_answer)],
        )
        mock_agent.assert_any_call(
            name="flow_portal",
            instruction="",
            model=mock_model(model="gpt-4o"),
            tools=[mock_agent_tool.return_value],
            sub_agents=[mock_agent.return_value],
            output_key="response",
        )
