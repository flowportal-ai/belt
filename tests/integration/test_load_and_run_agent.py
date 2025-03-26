import os

import pytest

from flow_portal import load_agent, run_agent, AgentSchema


@pytest.mark.parametrize("framework", ("langchain", "openai", "smolagents"))
@pytest.mark.skipif(
    "OPENAI_API_KEY" not in os.environ,
    reason="Integration tests require `OPENAI_API_KEY` env var",
)
def test_load_and_run_agent(framework):
    agent = load_agent(framework, AgentSchema(model_id="gpt-4o-mini"))
    result = run_agent(agent, "What day is today?")
    assert result
