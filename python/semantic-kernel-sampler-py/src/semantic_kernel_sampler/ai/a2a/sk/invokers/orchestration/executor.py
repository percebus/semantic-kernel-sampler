from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message
from semantic_kernel.contents import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole

from semantic_kernel_sampler.ai.a2a.sk.invokers.orchestration.protocol import SemanticOrchestrationA2AInvokerProtocol

if TYPE_CHECKING:
    from a2a.types import Message


@dataclass
class A2AOrchestrationInvokerExecutor(AgentExecutor):
    orchestration: SemanticOrchestrationA2AInvokerProtocol = field()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        user_input: str = context.get_user_input()
        requestKernelContent = ChatMessageContent(role=AuthorRole.USER, content=user_input)
        messages: list[ChatMessageContent] = [requestKernelContent]

        self.orchestration.runtime.start()
        messages: list[ChatMessageContent] = await self.orchestration.invoke(messages)
        if not messages:
            raise ValueError("No message found in response")

        message_text: str = str(messages)
        message: Message = new_agent_text_message(message_text)
        await event_queue.enqueue_event(message)
        await self.orchestration.runtime.stop_when_idle()

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("cancel not supported")  # pylint: disable=broad-exception-raised
