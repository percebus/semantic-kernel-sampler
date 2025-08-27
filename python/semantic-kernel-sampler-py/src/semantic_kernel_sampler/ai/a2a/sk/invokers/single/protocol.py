from semantic_kernel_sampler.a2a.cards.protocol import A2ACardsProtocol
from semantic_kernel_sampler.sk.invokers.protocol import InvokerProtocol


class SemanticA2AInvokerProtocol(A2ACardsProtocol, InvokerProtocol):
    # NOTE: Inherited
    # agent_card: AgentCard
    # extended_agent_card: Optional[AgentCard]

    # NOTE: Inherited
    # async def invoke(self, messages: list[KernelContent]) -> Optional[KernelContent]:
    ...
