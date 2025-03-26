from unittest.mock import MagicMock

from flow_portal.runners.langchain import run_langchain_agent


def test_run_langchain_default():
    agent_mock = MagicMock()
    run_langchain_agent(agent_mock, "Test Query")
    agent_mock.stream.assert_called_with(
        {"messages": [("user", "Test Query")]}, stream_mode="values"
    )
