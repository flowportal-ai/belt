from unittest.mock import patch, MagicMock

from flow_portal.runners.smolagents import run_smolagents_agent


def test_run_openai_default():
    runner_mock = MagicMock()
    with patch("flow_portal.runners.openai.Runner", runner_mock):
        agent_mock = MagicMock()
        run_smolagents_agent(agent_mock, "Test Query")
        agent_mock.run.assert_called_with("Test Query")
