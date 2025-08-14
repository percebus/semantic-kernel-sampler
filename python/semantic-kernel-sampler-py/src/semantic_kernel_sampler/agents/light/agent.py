from dataclasses import dataclass
from textwrap import dedent

from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from semantic_kernel_sampler.agents.base import ChatSemanticAgentBase

# TODO use plugin's methods as skills instead

# fmt: off
agent_skill__get_state = AgentSkill(
    id="light__get_state",
    name="get state",
    description="Gets the current state of the light switch",
    tags=["light", "get", "state"],
    examples=[
        "Is the light on?",
        "Is the light off?",]
)
# fmt: on

# fmt: off
agent_skill__change_state = AgentSkill(
    id="light__change_state",
    name="change state",
    description="Turns on and off the light switch",
    tags=["light", "set", "change", "state"],
    examples=[
        "Turn on the light",
        "Turn off the light"]
)
# fmt: on

agent_capabilities = AgentCapabilities(streaming=False)

# fmt: off
public_agent_card = AgentCard(
    name="Light Agent",
    description=agent_skill__get_state.description,
    url='http://localhost:9999/',  # FIXME read from container
    version='1.0.0', # FIXME READ from pyproject.toml
    default_input_modes=["text"],
    default_output_modes=["text"],
    capabilities=agent_capabilities,
    supports_authenticated_extended_card=True,
    skills=[
        agent_skill__get_state,
    ]
)
# fmt: on


# fmt: off
authenticated_agent_card: AgentCard = public_agent_card.model_copy( # type: ignore # FIXME
    update={
        'name': "Stateful Light Agent (Authenticated)",
        'description': 'Gets or sets the state of the light switch',
        'skills': [
            agent_skill__get_state,
            agent_skill__change_state
        ]
    }
)
# fmt: on


@dataclass
class LightAgent(ChatSemanticAgentBase):
    def __post_init__(self):
        self.agent_card__public = public_agent_card
        self.agent_card__authenticated = authenticated_agent_card
        self.system_prompt = dedent("""
            You are a helpful Light Switch assistant.
            You will only use the registered plugin(s).
            If it's not in the plugins, say 'I cannot help with that.'""")
