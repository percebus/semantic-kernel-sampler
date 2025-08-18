from typing import Generic, Optional, Protocol, TypeVar

from flask import Config
from semantic_kernel.agents.agent import Agent, AgentResponseItem, TMessage, TThreadType

from semantic_kernel_sampler.sk.agents.protocol import AgentExecutorProtocol

TAgent = TypeVar("TAgent", bound=Agent)


class SemanticAgentExecutorProtocol(Generic[TAgent, TThreadType, TMessage], AgentExecutorProtocol[TAgent, TMessage], Protocol):
    config: Config

    agent: TAgent

    agent_thread: Optional[TThreadType]

    async def invoke(self, messages: list[TMessage]) -> AgentResponseItem[TMessage]: ...
