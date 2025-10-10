from dataclasses import dataclass
from typing import TYPE_CHECKING

from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from agent_framework_sampler.a2a.cards.mixin import A2ACardsMixin
from agent_framework_sampler.ai.modules.chemistry_expert.a2a.skills.chat import ChemistryAgentSkill
from agent_framework_sampler.ai.modules.physics_expert.a2a.skills.chat import PhysicsAgentSkill
from agent_framework_sampler.config.mixin import ConfigurableMixin

if TYPE_CHECKING:
    from agent_framework_sampler.config.os_environ.a2a import A2ASettings


@dataclass
class ExpertsPanelA2AgentCards(A2ACardsMixin, ConfigurableMixin):
    # TODO move to DI
    def createAgentCard__public(self, skills: list[AgentSkill]) -> AgentCard:
        oA2ASettings: A2ASettings = self.configuration.settings.a2a
        oAgentCapabilities = AgentCapabilities(streaming=True)

        # fmt: off
        return AgentCard(
            name="Experts Panel Agent",
            description="Gets science answers from its experts",
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
                'name': "Experts Panel Agent (Authenticated)",
                'skills': skills
            }
        )
        # fmt: on

    def __post_init__(self):
        oPhysicsAgentSkill: AgentSkill = PhysicsAgentSkill()
        oChemistryAgentSkill: AgentSkill = ChemistryAgentSkill()

        skills: list[AgentSkill] = [oPhysicsAgentSkill, oChemistryAgentSkill]

        authenticated_skills = skills

        self.agent_card = self.createAgentCard__public(skills=skills)
        self.extended_agent_card = self.createAgentCard__authenticated(skills=authenticated_skills)
