from dataclasses import dataclass, field

from semantic_kernel import Kernel

from semantic_kernel_sampler.a2a.agents.base.semantic.chat.agent import SemanticChatAgentBase
from semantic_kernel_sampler.ai.tooling.math.instructions import SYSTEM_MESSAGE
from semantic_kernel_sampler.ai.tooling.math.sk.kernel import MathKernel


@dataclass
class MathAgent(SemanticChatAgentBase):

    kernel: Kernel = field(default_factory=MathKernel)

    def __post_init__(self):
        # TODO
        # self.agent_card__public = public_agent_card
        # self.agent_card__authenticated = authenticated_agent_card

        self._system_message = SYSTEM_MESSAGE

        super().__post_init__()
