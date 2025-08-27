from abc import ABC
from dataclasses import dataclass, field
from typing import Optional

from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread  # pylint: disable=no-name-in-module
from semantic_kernel.agents.agent import AgentResponseItem
from semantic_kernel.contents import ChatMessageContent

from semantic_kernel_sampler.sk.invokers.builtin.agents.threaded.protocol import ThreadedBuiltinAgentInvokerProtocol


@dataclass
class ChatCompletionBuiltinAgentInvoker(ABC, ThreadedBuiltinAgentInvokerProtocol[ChatCompletionAgent, ChatHistoryAgentThread, ChatMessageContent]):
    # NOTE: kernel holds the plugins!
    kernel: Kernel = field()

    instructions: str = field()

    name: Optional[str] = field(default=None)

    description: Optional[str] = field(default=None)

    agent_thread: Optional[ChatHistoryAgentThread] = field(default=None)

    agent: ChatCompletionAgent = field(init=False)

    def __post_init__(self):
        # fmt: off
        self.agent = ChatCompletionAgent(
            kernel=self.kernel,
            name=self.name or self.__class__.__name__,
            description=self.description,
            instructions=self.instructions)
        # fmt: on

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
