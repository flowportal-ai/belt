from unittest.mock import patch, MagicMock

from flow_portal.schema import AgentSchema
from flow_portal.loaders.langchain import (
    load_lanchain_agent,
)
from flow_portal.tools import (
    search_web,
    visit_webpage,
)


def test_load_langchain_agent_default():
    model_mock = MagicMock()
    create_mock = MagicMock()
    agent_mock = MagicMock()
    create_mock.return_value = agent_mock
    tool_mock = MagicMock()

    with (
        patch("flow_portal.loaders.langchain.create_react_agent", create_mock),
        patch("flow_portal.loaders.langchain.init_chat_model", model_mock),
        patch("langchain_core.tools.tool", tool_mock),
    ):
        load_lanchain_agent(AgentSchema(model_id="gpt-4o"))
        model_mock.assert_called_once_with("gpt-4o")
        create_mock.assert_called_once_with(
            model=model_mock.return_value,
            tools=[tool_mock(search_web), tool_mock(visit_webpage)],
            prompt=None,
        )
