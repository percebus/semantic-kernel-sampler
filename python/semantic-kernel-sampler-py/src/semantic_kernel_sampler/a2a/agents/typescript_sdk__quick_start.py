from dataclasses import dataclass
from textwrap import dedent
from typing import TYPE_CHECKING, ClassVar

from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from semantic_kernel_sampler.a2a.agents.base.semantic.chat.agent import SemanticChatAgentBase
from semantic_kernel_sampler.sk.plugins.mcp.typescript_sdk__quick_start import DemoServerMCPStdioPlugin
from semantic_kernel_sampler.sk.plugins.protocol import PluginProtocol
from semantic_kernel_sampler.third_party.modelcontextprotocol.typescript_sdk.quick_start import createMCPStdioPlugin
from semantic_kernel_sampler.utils.lodash import noop

if TYPE_CHECKING:
    from semantic_kernel_sampler.configuration.os_environ.a2a import A2ASettings


noop(createMCPStdioPlugin)
noop(DemoServerMCPStdioPlugin)


@dataclass
class DemoMcpServerAgent(SemanticChatAgentBase):
    plugins: ClassVar[list[PluginProtocol]] = [DemoServerMCPStdioPlugin()]

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

        # TODO read from file
        self.system_message = dedent("""
            You are a helpful assistant that leverages MCP services.
            You will only use the registered plugin(s).
            If it's not in the plugins, say 'I cannot help with that.'""")

        super().__post_init__()
