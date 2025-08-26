from dataclasses import dataclass

from semantic_kernel_sampler.sk.agents.invokers.custom.mixins.chat.agent import CustomSemanticChatAgentInvokerMixin


@dataclass
class MathCustomAgentInvoker(CustomSemanticChatAgentInvokerMixin):
    def __post_init__(self):
        # TODO
        # self.agent_card__public = public_agent_card
        # self.agent_card__authenticated = authenticated_agent_card
        pass
