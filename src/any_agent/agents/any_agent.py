from typing import Any, Optional
from abc import ABC, abstractmethod

from flow_portal.config import AgentFramework, AgentConfig


class AnyAgent(ABC):
    """Base abstract class for all agent implementations.

    This provides a unified interface for different agent frameworks.
    """

    # factory method
    @classmethod
    def create(
        cls,
        agent_framework: AgentFramework,
        agent_config: AgentConfig,
        managed_agents: Optional[list[AgentConfig]] = None,
    ) -> "AnyAgent":
        if agent_framework == AgentFramework.SMOLAGENTS:
            from flow_portal.agents.smolagents import SmolagentsAgent

            return SmolagentsAgent(agent_config, managed_agents=managed_agents)
        elif agent_framework == AgentFramework.LANGCHAIN:
            from flow_portal.agents.langchain import LangchainAgent

            return LangchainAgent(agent_config, managed_agents=managed_agents)
        elif agent_framework == AgentFramework.OPENAI:
            from flow_portal.agents.openai import OpenAIAgent

            return OpenAIAgent(agent_config, managed_agents=managed_agents)
        elif agent_framework == AgentFramework.LLAMAINDEX:
            from flow_portal.agents.llama_index import LlamaIndexAgent

            return LlamaIndexAgent(agent_config, managed_agents=managed_agents)
        else:
            raise ValueError(f"Unsupported agent framework: {agent_framework}")

    @abstractmethod
    def _load_agent(self) -> None:
        """Load the agent instance."""
        pass

    @abstractmethod
    def run(self, prompt: str) -> Any:
        """Run the agent with the given prompt."""
        pass
