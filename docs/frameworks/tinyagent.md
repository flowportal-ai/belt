# TinyAgent

As part of the bare bones library, we provide our own Python implementation based on [HuggingFace Tiny Agents](https://huggingface.co/blog/tiny-agents).

You can find it in [`flow_portal.frameworks.tinyagent`](https://github.com/mozilla-ai/any-agent/blob/main/src/flow_portal/frameworks/tinyagent.py).

## Examples

### Use MCP Tools

```python
from flow_portal import AnyAgent, AgentConfig
from flow_portal.config import MCPStdio

agent = AnyAgent.create(
    "tinyagent",
    AgentConfig(
        model_id="gpt-4.1-nano",
        instructions="You must use the available tools to find an answer",
        tools=[
            MCPStdio(
                command="uvx",
                args=["duckduckgo-mcp-server"]
            )
        ]
    )
)

result = agent.run(
    "Which Agent Framework is the best??"
)
print(result.final_output)
```
