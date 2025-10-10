from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message

from agent_framework import AgentRunResponse, ChatMessage, Role
from agent_framework_sampler.agent_framework.builtin.agent.chat.runner.protocol import ChatAgentRunnerProtocol

if TYPE_CHECKING:
    from a2a.types import Message


# SRC: https://github.com/a2aproject/a2a-samples/blob/main/samples/python/agents/helloworld/agent_executor.py
@dataclass
class ChatAgentRunnerA2AgentFrameworkExecutor(AgentExecutor):
    runner: ChatAgentRunnerProtocol = field()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        user_input: str = context.get_user_input()
        oChatMessage = ChatMessage(role=Role.USER, text=user_input)
        messages: list[ChatMessage] = [oChatMessage]
        oAgentRunResponse: AgentRunResponse = await self.runner.run_async(messages)  # type: ignore # FIXME
        message_text: str = str(oAgentRunResponse)  # pyright: ignore[reportUnknownArgumentType]
        oMessage: Message = new_agent_text_message(message_text)
        await event_queue.enqueue_event(oMessage)

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("cancel not supported")  # pylint: disable=broad-exception-raised
