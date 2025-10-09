from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from agent_framework import AgentRunResponse, AgentThread, ChatAgent, ChatMessage

from agent_framework_sampler.a2a.cards.mixin import A2ACardsMixin
from agent_framework_sampler.a2a.cards.protocol import A2ACardsProtocol
from agent_framework_sampler.agent_framework.agents.builtin.chat.threaded import ThreadedChatAgentRunner
from agent_framework_sampler.config.mixin import ConfigurableMixin
from agent_framework_sampler.utils.lodash import noop

if TYPE_CHECKING:
    from agent_framework_sampler.config.os_environ.a2a import A2ASettings


noop(A2ACardsMixin)
noop(ThreadedChatAgentRunner)


@dataclass
class WeatherA2AgentRunner(ConfigurableMixin, A2ACardsProtocol):  # , A2ACardsMixin, ThreadedChatAgentRunner):
    chat_agent: ChatAgent = field()

    extended_agent_card: Optional[AgentCard] = field(default=None)

    service_thread_id: Optional[str] = field(default=None)

    agent_card: AgentCard = field(init=False)

    agent_thread: AgentThread = field(init=False)

    async def run_async(self, messages: list[ChatMessage]) -> AgentRunResponse:
        return await self.chat_agent.run(messages, thread=self.agent_thread)

    def createAgentSkill__get_weather(self) -> AgentSkill:
        # fmt: off
        return AgentSkill(
            id="get_weather",
            name="get weather",
            description="Get the weather for a given location.",
            tags=["weather", "location"],
            examples=[
                "What's the weather like in New York?",
                "What's the weather in London?"
            ],
        )
        # fmt: on

    def createAgentSkill__get_time(self) -> AgentSkill:
        # fmt: off
        return AgentSkill(
            id="get_time",
            name="get time",
            description="Get the current UTC time.",
            tags=["time", "utc"],
            examples=[
                "What's the current UTC time?",
            ],
        )
        # fmt: on

    def createAgentCard__public(self, skills: list[AgentSkill]) -> AgentCard:
        oA2ASettings: A2ASettings = self.configuration.settings.a2a
        oAgentCapabilities = AgentCapabilities(streaming=True)

        # fmt: off
        return AgentCard(
            name="Weather Agent",
            description="Gets the current weather information",
            url=oA2ASettings.next_url,
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
                'name': "Weather Agent (Authenticated)",
                'skills': skills
            }
        )
        # fmt: on

    def __post_init__(self):
        get_weather_AgentSkill: AgentSkill = self.createAgentSkill__get_weather()
        get_time_AgentSkill: AgentSkill = self.createAgentSkill__get_time()

        skills = [get_weather_AgentSkill, get_time_AgentSkill]
        authenticated_skills = skills

        self.agent_card = self.createAgentCard__public(skills=skills)
        self.extended_agent_card = self.createAgentCard__authenticated(skills=authenticated_skills)

        self.agent_thread = self.chat_agent.get_new_thread(service_thread_id=self.service_thread_id)
