from dataclasses import dataclass, field
from logging import Logger
from typing import TYPE_CHECKING

from semantic_kernel.agents import Agent, GroupChatManager, GroupChatOrchestration  # pylint: disable=no-name-in-module
from semantic_kernel.agents.runtime import InProcessRuntime
from semantic_kernel.contents import ChatMessageContent

from semantic_kernel_sampler.sk.invokers.builtin.agents.orchestration.protocol import BuiltinOrchestrationInvokerProtocol

if TYPE_CHECKING:
    from semantic_kernel.agents.orchestration.orchestration_base import DefaultTypeAlias, OrchestrationResult


@dataclass
class GroupChatOrchestrationBuiltinAgentInvoker(BuiltinOrchestrationInvokerProtocol):
    logger: Logger = field()

    group_chat_manager: GroupChatManager = field()

    runtime: InProcessRuntime = field()

    agents: list[Agent] = field(default_factory=list)  # pyright: ignore[reportUnknownVariableType]

    orchestration: GroupChatOrchestration = field(init=False)

    def agent_response_callback(self, message: ChatMessageContent) -> None:
        """Observer function to print the messages from the agents."""
        self.logger.info("**%s**\n%s", message.name, message.content)

    def __post_init__(self) -> None:
        # fmt: off
        self.orchestration = GroupChatOrchestration(
            members=self.agents,
            manager=self.group_chat_manager,
            agent_response_callback=self.agent_response_callback  # pyright: ignore[reportArgumentType]
        )
        # fmt: on

    async def invoke(self, messages: list[ChatMessageContent]) -> list[ChatMessageContent]:
        firstChatMessageContent: ChatMessageContent = messages[0]
        oOrchestrationResult: OrchestrationResult[DefaultTypeAlias] = await self.orchestration.invoke(
            task=firstChatMessageContent.content,
            runtime=self.runtime,
        )

        # DefaultTypeAlias = ChatMessageContent | list[ChatMessageContent]
        message_or_messages: DefaultTypeAlias = await oOrchestrationResult.get()
        messages = [message_or_messages] if isinstance(message_or_messages, ChatMessageContent) else message_or_messages
        self.logger.info("Final result:\n%s", messages)
        return messages
