from typing import Protocol

from semantic_kernel_sampler.a2a.cards.protocol import A2ACardsProtocol
from semantic_kernel_sampler.rest.models.request import RequestModel
from semantic_kernel_sampler.rest.models.response import ResponseModel


class A2AInvokerProtocol(A2ACardsProtocol, Protocol):
    # NOTE: Inherited
    # agent_card: AgentCard
    # extended_agent_card: Optional[AgentCard]

    # TODOs?
    # - Replace RequestModel for a2a.types.RequestContext
    # - Replace ResponseModel for a2a.types.Message
    async def invoke(self, request: RequestModel) -> ResponseModel: ...
