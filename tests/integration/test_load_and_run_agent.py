import os

import pytest

from flow_portal import AgentFramework, AgentConfig, AnyAgent


@pytest.mark.parametrize(
    "framework", ("google", "langchain", "openai", "smolagents", "llama_index")
)
@pytest.mark.skipif(
    "OPENAI_API_KEY" not in os.environ,
    reason="Integration tests require `OPENAI_API_KEY` env var",
)
def test_load_and_run_agent(framework):
    agent_framework = AgentFramework(framework)
    kwargs = {}
    if framework == "smolagents":
        kwargs["agent_type"] = "ToolCallingAgent"
    agent_config = AgentConfig(
        model_id="gpt-4o-mini",
        tools=["flow_portal.tools.search_web"],
        instructions="Search the web to answer",
        **kwargs,
    )
    agent = AnyAgent.create(agent_framework, agent_config)
    assert len(agent.tools) > 0
    result = agent.run("Which agent framework is the best?")
    assert result
