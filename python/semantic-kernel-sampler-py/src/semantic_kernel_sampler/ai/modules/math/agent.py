from dataclasses import dataclass

from semantic_kernel_sampler.ai.mixins.semantic.chat.custom_agent import CustomSemanticChatAgentMixin


@dataclass
class MathAgent(CustomSemanticChatAgentMixin):
    def __post_init__(self):
        # TODO
        # self.agent_card__public = public_agent_card
        # self.agent_card__authenticated = authenticated_agent_card
        pass
