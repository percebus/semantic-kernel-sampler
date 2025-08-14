from dataclasses import dataclass
from textwrap import dedent

from semantic_kernel_sampler.agents.base import ChatSemanticAgentBase


@dataclass
class MathAgent(ChatSemanticAgentBase):
    def __post_init__(self):
        # TODO
        # self.agent_card__public = public_agent_card
        # self.agent_card__authenticated = authenticated_agent_card

        # TODO read from file
        self.system_prompt = dedent("""
            You are a helpful Mathematician assistant.
            You will only use the registered plugin(s).
            If it's not in the plugins, say 'I cannot help with that.'""")
