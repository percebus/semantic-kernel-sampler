from abc import ABC
from dataclasses import dataclass, field
from typing import Optional

from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread  # pylint: disable=E0611 #no-name-in-module
from semantic_kernel.agents.agent import AgentResponseItem
from semantic_kernel.contents import ChatMessageContent

from semantic_kernel_sampler.sk.agents.executors.base.semantic.protocol import SemanticAgentExecutorProtocol


@dataclass
class ChatCompletionSemanticAgentExecutorBase(SemanticAgentExecutorProtocol[ChatCompletionAgent, ChatHistoryAgentThread, ChatMessageContent], ABC):
    kernel: Kernel = field()

    agent: ChatCompletionAgent = field(init=False)

    agent_thread: Optional[ChatHistoryAgentThread] = field(default=None)

    _instructions: str = field(init=False, default="You are a helpful assistant.")

    async def invoke(self, messages: list[ChatMessageContent]) -> AgentResponseItem[ChatMessageContent]:
        # fmt: off
        response: AgentResponseItem[ChatMessageContent] = \
            await self.agent.get_response(messages=messages, thread=self.agent_thread)  # pyright: ignore[reportArgumentType, reportUnknownMemberType]
        # fmt: on

        self.agent_thread = response.thread  # pyright: ignore[reportAttributeAccessIssue]

        return response

    # TODO REFACTOR convert to dispisable w/ __exit__
    async def cleanup(self) -> None:
        if self.agent_thread:
            await self.agent_thread.delete()
