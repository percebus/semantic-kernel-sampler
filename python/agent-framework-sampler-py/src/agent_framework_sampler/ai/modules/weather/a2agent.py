from dataclasses import dataclass
from typing import TYPE_CHECKING

from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from agent_framework_sampler.a2a.cards.protocol import A2ACardsProtocol
from agent_framework_sampler.agent_framework.agents.builtin.chat.threaded import ThreadedChatAgentRunner
from agent_framework_sampler.config.mixin import ConfigurableMixin

if TYPE_CHECKING:
    from agent_framework_sampler.config.os_environ.a2a import A2ASettings


@dataclass
class WeatherA2AgentRunner(ConfigurableMixin, ThreadedChatAgentRunner, A2ACardsProtocol):
    def createAgentSkill__get_weather(self) -> AgentSkill:
        return AgentSkill(
            id="get_weather",
            name="get weather",
            description="Get the weather for a given location.",
            tags=["weather", "location"],
            examples=["What's the weather like in New York?", "What's the weather in London?"],
        )

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
        # TODO use plugin's methods as skills instead

        get_weather_AgentSkill: AgentSkill = self.createAgentSkill__get_weather()
        get_time_AgentSkill: AgentSkill = self.createAgentSkill__get_time()

        skills = [get_weather_AgentSkill, get_time_AgentSkill]
        authenticated_skills = skills

        self.agent_card = self.createAgentCard__public(skills=skills)
        self.extended_agent_card = self.createAgentCard__authenticated(skills=authenticated_skills)
