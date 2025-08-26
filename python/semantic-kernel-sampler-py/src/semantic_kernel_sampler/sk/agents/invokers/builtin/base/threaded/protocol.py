from typing import Generic, Optional, Protocol, TypeVar

from semantic_kernel.agents.agent import Agent, TMessage, TThreadType

from semantic_kernel_sampler.sk.agents.invokers.builtin.protocol import BuiltinAgentInvokerProtocol

TAgent = TypeVar("TAgent", bound=Agent)


class ThreadedBuiltinAgentInvokerProtocol(Generic[TAgent, TThreadType, TMessage], BuiltinAgentInvokerProtocol[TAgent, TMessage], Protocol):
    # Inherits
    # agent: TAgent
    # async def invoke(self, messages: list[TMessage]) -> AgentResponseItem[TMessage]: ...

    agent_thread: Optional[TThreadType]

    async def cleanup(self) -> None: ...
