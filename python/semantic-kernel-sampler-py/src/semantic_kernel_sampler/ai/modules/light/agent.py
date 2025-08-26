from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from semantic_kernel.contents import ChatHistory

from semantic_kernel_sampler.a2a.agents.mixins.agent import A2AgentMixin
from semantic_kernel_sampler.ai.mixins.semantic.chat.custom_agent import CustomSemanticChatAgentMixin
from semantic_kernel_sampler.configuration.mixin import ConfigurableMixin

if TYPE_CHECKING:
    from semantic_kernel_sampler.configuration.os_environ.a2a import A2ASettings


# TODO? REFACTOR? as Mixin only?
#  - w/o SemanticChatAgentBase
#  - and only a2a stuff
@dataclass
class LightAgent(ConfigurableMixin, A2AgentMixin, CustomSemanticChatAgentMixin):
    kernel: Kernel = field()

    chat_history: ChatHistory = field()

    chat_completion: ChatCompletionClientBase = field()

    prompt_execution_settings: PromptExecutionSettings = field()

    agent_card: AgentCard = field(init=False)

    extended_agent_card: Optional[AgentCard] = field(default=None)

    def createAgentSkill__get_state(self) -> AgentSkill:
        return AgentSkill(
            id="light__get_state",
            name="get state",
            description="Gets the current state of the light switch",
            tags=["light", "get", "state"],
            examples=[
                "Is the light on?",
                "Is the light off?",
            ],
        )

    def createAgentSkill__change_state(self) -> AgentSkill:
        # fmt: off
        return AgentSkill(
            id="light__change_state",
            name="change state",
            description="Turns on and off the light switch",
            tags=["light", "set", "change", "state"],
            examples=[
                "Turn on the light",
                "Turn off the light"]
        )
        # fmt: on

    def createAgentCard__public(self, skills: list[AgentSkill]) -> AgentCard:
        oA2ASettings: A2ASettings = self.config.settings.a2a
        oAgentCapabilities = AgentCapabilities(streaming=True)

        # fmt: off
        return AgentCard(
            name="Light Agent",
            description="Gets the current state of the light switch",
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
        return self.agent_card.model_copy( # type: ignore # FIXME
            update={
                'name': "Stateful Light Agent (Authenticated)",
                'description': 'Gets or sets the state of the light switch',
                'skills': skills
            }
        )
        # fmt: on

    def __post_init__(self):
        # TODO use plugin's methods as skills instead

        get_state_AgentSkill: AgentSkill = self.createAgentSkill__get_state()
        change_state_AgentSkill: AgentSkill = self.createAgentSkill__change_state()

        # fmt: off
        self.agent_card = self.createAgentCard__public(skills=[
            get_state_AgentSkill])
        # fmt: on

        # fmt: off
        self.extended_agent_card = self.createAgentCard__authenticated(skills=[
            get_state_AgentSkill,
            change_state_AgentSkill])
        # fmt: on
