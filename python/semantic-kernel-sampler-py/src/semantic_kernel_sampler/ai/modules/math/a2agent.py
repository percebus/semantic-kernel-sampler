from dataclasses import dataclass

# from semantic_kernel_sampler.a2a.cards.protocol import A2ACardsProtocol  # TODO
from semantic_kernel_sampler.sk.invokers.custom.chat.invoker import CustomSemanticChatInvoker


@dataclass
class MathCustomSemanticA2AgentInvoker(CustomSemanticChatInvoker):
    def __post_init__(self):
        # TODO
        # self.agent_card__public = public_agent_card
        # self.agent_card__authenticated = authenticated_agent_card
        pass
