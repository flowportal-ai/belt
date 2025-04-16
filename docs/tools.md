# Agent Tools

`any-agent` provides 2 options to specify what `tools` are available to your agent: `Callable`, or `MCP` ([Model Context Protocol](https://modelcontextprotocol.io/introduction)).

You can use any combination of options in the same agent.

Under the hood, `any-agent` takes care of wrapping the
tool so it becomes usable by the selected framework.

=== "Callable"

    ```python
    from flow_portal import AgentConfig, AgentFramework, AnyAgent
    from flow_portal.tools import search_web

    framework = AgentFramework("openai")

    main_agent = AgentConfig(
        model_id="gpt-4o-mini",
        tools=[search_web]
    )
    ```

=== "MCP"

    ```python
    from flow_portal import AgentConfig, AgentFramework, AnyAgent
    from flow_portal.config import MCPTool

    framework = AgentFramework("openai")

    main_agent = AgentConfig(
        model_id="gpt-4o-mini",
        tools=[
            MCPTool(
                command="docker",
                args=["run", "-i", "--rm", "mcp/fetch"],
                tools=["fetch"]
            ),
        ]
    )
    ```
