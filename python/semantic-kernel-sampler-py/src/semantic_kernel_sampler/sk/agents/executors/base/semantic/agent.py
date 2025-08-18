from abc import ABC
from dataclasses import dataclass, field
from typing import Optional

from semantic_kernel import Kernel
from semantic_kernel.agents import Agent
from semantic_kernel.agents.agent import AgentResponseItem, AgentThread
from semantic_kernel.contents import ChatMessageContent

from semantic_kernel_sampler.sk.agents.executors.base.semantic.protocol import SemanticAgentExecutorProtocol


@dataclass
class SemanticAgentExecutorBase(SemanticAgentExecutorProtocol[Agent, AgentThread, ChatMessageContent], ABC):
    kernel: Kernel = field()

    agent: Agent = field()

    agent_thread: Optional[AgentThread] = field(default=None)

    async def invoke(self, messages: list[ChatMessageContent]) -> AgentResponseItem[ChatMessageContent]:
        # fmt: off
        response: AgentResponseItem[ChatMessageContent] = \
            await self.agent.get_response(messages=messages, thread=self.agent_thread)  # pyright: ignore[reportArgumentType, reportUnknownMemberType]
        # fmt: on

        self.agent_thread = response.thread

        return response

    # TODO REFACTOR convert to dispisable w/ __exit__
    async def cleanup(self) -> None:
        if self.agent_thread:
            await self.agent_thread.delete()
