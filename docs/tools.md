# Agent Tools

`any-agent` provides 3 options to specify what `tools` are available to your agent: `Import`, `Callable`, and `MCP` ([Model Context Protocol](https://modelcontextprotocol.io/introduction)).

You can use any combination of options in the same agent.

Under the hood, `any-agent` takes care of importing (for the first case) and wrapping (in any case needed) the
tool so it becomes usable by the selected framework.

=== "Import"

    For a tool that you would import like:

    ```python
    from flow_portal.tools import search_web
    ```

    The expected syntax is `flow_portal.tools.search_web`

    ```python
    from flow_portal import AgentConfig, AgentFramework, AnyAgent

    framework = AgentFramework("openai")

    main_agent = AgentConfig(
        model_id="gpt-4o-mini",
        tools=[
            "langchain_community.tools.TavilySearchResults",
            "flow_portal.tools.visit_webpage"
        ]
    )
    ```

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
