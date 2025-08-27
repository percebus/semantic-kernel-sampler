from typing import Protocol

from semantic_kernel_sampler.a2a.cards.protocol import A2ACardsProtocol
from semantic_kernel_sampler.sk.invokers.builtin.agents.orchestration.protocol import BuiltinOrchestrationInvokerProtocol


class SemanticOrchestrationA2AInvokerProtocol(A2ACardsProtocol, BuiltinOrchestrationInvokerProtocol, Protocol):
    # NOTE: Inherited
    # agent_card: AgentCard
    # extended_agent_card: Optional[AgentCard]

    # NOTE: Inherited
    # async def invoke(self, messages: list[ChatMessageContent]) -> list[ChatMessageContent]: ...
    ...
