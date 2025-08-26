from dataclasses import dataclass

# from semantic_kernel_sampler.a2a.mixins.cards import A2ACardsMixin  # TODO
from semantic_kernel_sampler.sk.agents.invokers.custom.base.chat.agent import CustomSemanticChatAgentInvokerBase


@dataclass
class MathCustomSemanticA2AgentInvoker(CustomSemanticChatAgentInvokerBase):
    def __post_init__(self):
        # TODO
        # self.agent_card__public = public_agent_card
        # self.agent_card__authenticated = authenticated_agent_card
        pass
