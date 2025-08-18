from typing import Generic, Protocol, TypeVar

from flask import Config
from semantic_kernel.agents.agent import Agent, AgentResponseItem, TMessage

TAgent = TypeVar("TAgent", bound=Agent)


class AgentExecutorProtocol(Protocol, Generic[TAgent, TMessage]):
    config: Config

    agent: TAgent

    async def invoke(self, messages: list[TMessage]) -> AgentResponseItem[TMessage]: ...
