from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message
from semantic_kernel.contents import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole

from semantic_kernel_sampler.ai.a2a.sk.semantic.protocol import A2AInvokerProtocol

if TYPE_CHECKING:
    from a2a.types import Message
    from semantic_kernel.contents.kernel_content import KernelContent


# SRC: https://github.com/a2aproject/a2a-samples/blob/main/samples/python/agents/helloworld/agent_executor.py
@dataclass
class A2AgentInvokerExecutor(AgentExecutor):
    agent: A2AInvokerProtocol = field()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        user_input: str = context.get_user_input()
        requestChatMessageContent = ChatMessageContent(role=AuthorRole.USER, content=user_input)
        responseKernelContent: Optional[KernelContent] = await self.agent.invoke(requestChatMessageContent)
        if not responseKernelContent:
            raise ValueError("No message found in response")

        message_text: str = str(responseKernelContent)
        message: Message = new_agent_text_message(message_text)
        await event_queue.enqueue_event(message)

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("cancel not supported")  # pylint: disable=broad-exception-raised
