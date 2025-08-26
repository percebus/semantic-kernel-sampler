from typing import Optional, Protocol

from a2a.types import AgentCard


class A2ACardsProtocol(Protocol):
    agent_card: AgentCard

    extended_agent_card: Optional[AgentCard]
