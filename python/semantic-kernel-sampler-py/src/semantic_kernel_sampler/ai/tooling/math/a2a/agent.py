from dataclasses import dataclass

from semantic_kernel_sampler.a2a.agents.base.semantic.chat.agent import SemanticChatAgentBase


@dataclass
class MathAgent(SemanticChatAgentBase):

    def __post_init__(self):
        # TODO
        # self.agent_card__public = public_agent_card
        # self.agent_card__authenticated = authenticated_agent_card
        pass
