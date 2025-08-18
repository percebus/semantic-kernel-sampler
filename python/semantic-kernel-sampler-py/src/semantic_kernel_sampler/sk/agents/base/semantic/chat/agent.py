from abc import ABC
from dataclasses import dataclass, field
from typing import ClassVar, Optional

from flask import Config
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.agents.agent import AgentResponseItem
from semantic_kernel.contents import ChatMessageContent

from semantic_kernel_sampler.sk.agents.base.semantic.protocol import SemanticAgentExecutorProtocol
from semantic_kernel_sampler.sk.plugins.protocol import PluginProtocol


@dataclass
class ChatCompletionSemanticAgentExecutorBase(SemanticAgentExecutorProtocol[ChatCompletionAgent, ChatHistoryAgentThread, ChatMessageContent], ABC):
    plugins: ClassVar[list[PluginProtocol]] = []

    config: Config = field()

    kernel: Kernel = field()

    agent: ChatCompletionAgent = field()

    agent_thread: Optional[ChatHistoryAgentThread] = field(default=None)

    def __post_init__(self):
        self.name = self.__class__.__name__

        for plugin in self.plugins:
            self.kernel.add_plugin(plugin, plugin_name=plugin.__class__.__name__)

    async def invoke(self, messages: list[ChatMessageContent]) -> AgentResponseItem[ChatMessageContent]:
        # fmt: off
        item: AgentResponseItem[ChatMessageContent] = \
            await self.agent.get_response(messages=messages, thread=self.agent_thread)  # pyright: ignore[reportArgumentType, reportUnknownMemberType]
        # fmt: on

        if self.agent_thread:
            await self.agent_thread.delete()

        return item
