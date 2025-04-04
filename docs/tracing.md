# Agent Tracing

`any-agent` uses [`openinference`](https://github.com/Arize-ai/openinference) to generate
standardized [OpenTelemetry](https://opentelemetry.io/) traces for any of the supported [agent frameworks](./frameworks.md).

## Example

```py
from flow_portal import AgentConfig, AgentFramework, AnyAgent
from flow_portal.tracing import setup_tracing

framework = AgentFramework("openai")

agent = AnyAgent.create(
        main_agent=AgentConfig(
        model_id="gpt-4o",
        tools=["flow_portal.tools.search_web", "flow_portal.tools.visit_webpage"]
    )
)

setup_tracing(framework)
```
