from typing import Generic, Protocol, TypeVar

from semantic_kernel.agents.agent import Agent, AgentResponseItem, TMessage

TAgent = TypeVar("TAgent", bound=Agent)


class BuiltinAgentInvokerProtocol(Protocol, Generic[TAgent, TMessage]):
    agent: TAgent

    async def invoke(self, messages: list[TMessage]) -> AgentResponseItem[TMessage]: ...
