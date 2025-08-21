from dataclasses import dataclass
from typing import TYPE_CHECKING

from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from semantic_kernel_sampler.ai.base.semantic.chat.agent import SemanticChatAgentBase

if TYPE_CHECKING:
    from semantic_kernel_sampler.configuration.os_environ.a2a import A2ASettings


@dataclass
class DemoMcpServerAgent(SemanticChatAgentBase):
    def createAgentSkill__add(self) -> AgentSkill:
        return AgentSkill(
            id="add",
            name="Addition Tool",
            description="Add two numbers",
            tags=["modelcontextprotocol", "typescript-sdk", "example", "Quick Start", "math"],
            examples=[
                "Add 2 and 3",
                "Add 5 and 7",
            ],
        )

    # NOTE: Should MCP "resources" also be listed as "skills"?
    def createAgentSkill__greeting(self) -> AgentSkill:
        # fmt: off
        return AgentSkill(
            id="greeting",
            name="Greeting Resource",
            description="Dynamic greeting generator",
            tags=["modelcontextprotocol", "typescript-sdk", "example", "Quick Start", "greeting"],
            examples=[
                "Greet JC"
            ]
        )
        # fmt: on

    def createAgentCard__public(self, skills: list[AgentSkill]) -> AgentCard:
        oA2ASettings: A2ASettings = self.config.settings.a2a
        oAgentCapabilities = AgentCapabilities(streaming=True)

        # fmt: off
        return AgentCard(
            name="Quick Start MCP Agent",
            description="Couple of MCP tools",
            url=oA2ASettings.url,
            version='1.0.0', # FIXME READ from pyproject.toml
            default_input_modes=["text"],
            default_output_modes=["text"],
            capabilities=oAgentCapabilities,
            supports_authenticated_extended_card=True,
            skills=skills
        )
        # fmt: on

    def createAgentCard__authenticated(self, skills: list[AgentSkill]) -> AgentCard:
        # fmt: off
        return self.agent_card.model_copy(
            update={
                'name': "Quick Start MCP Agent (Authenticated)",
                'skills': skills
            }
        )
        # fmt: on

    def __post_init__(self):
        addAgentSkill: AgentSkill = self.createAgentSkill__add()
        greetingAgentSkill: AgentSkill = self.createAgentSkill__greeting()

        # fmt: off
        all_skills: list[AgentSkill] = [
            addAgentSkill,
            greetingAgentSkill]
        # fmt: on

        self.agent_card = self.createAgentCard__public(all_skills)
        self.extended_agent_card = self.createAgentCard__authenticated(all_skills)
