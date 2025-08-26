from typing import Optional, Protocol

from semantic_kernel.contents.kernel_content import KernelContent

from semantic_kernel_sampler.a2a.cards.protocol import A2ACardsProtocol


class SemanticA2AInvokerProtocol(A2ACardsProtocol, Protocol):
    # NOTE: Inherited
    # agent_card: AgentCard
    # extended_agent_card: Optional[AgentCard]

    async def invoke(self, messages: list[KernelContent]) -> Optional[KernelContent]: ...
