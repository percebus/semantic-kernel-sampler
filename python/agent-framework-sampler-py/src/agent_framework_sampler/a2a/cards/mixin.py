from abc import ABC
from dataclasses import dataclass, field
from typing import Optional

from a2a.types import AgentCard

from agent_framework_sampler.a2a.cards.protocol import A2ACardsProtocol


@dataclass
class A2ACardsMixin(A2ACardsProtocol, ABC):
    agent_card: AgentCard = field(init=False)

    extended_agent_card: Optional[AgentCard] = field(default=None)
