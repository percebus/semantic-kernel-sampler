from abc import ABC
from dataclasses import dataclass, field
from typing import Optional

from a2a.types import AgentCard

from semantic_kernel_sampler.a2a.cards.protocol import A2ACardsProtocol
from semantic_kernel_sampler.utils.lodash import noop

noop(A2ACardsProtocol)


@dataclass
class A2ACardsMixin(ABC):  # , A2ACardsProtocol)
    agent_card: AgentCard = field(init=False)

    extended_agent_card: Optional[AgentCard] = field(default=None)
