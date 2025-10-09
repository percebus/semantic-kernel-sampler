from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message
from agent_framework import AgentRunResponse, ChatMessage, Role

from agent_framework_sampler.ai.a2a.agent_framework.agent.protocol import A2AgentFrameworkRunnerProtocol

if TYPE_CHECKING:
    from a2a.types import Message


# SRC: https://github.com/a2aproject/a2a-samples/blob/main/samples/python/agents/helloworld/agent_executor.py
@dataclass
class A2AgentInvokerExecutor(AgentExecutor):
    agent: A2AgentFrameworkRunnerProtocol = field()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        user_input: str = context.get_user_input()
        oChatMessage = ChatMessage(role=Role.USER, text=user_input)
        messages: list[ChatMessage] = [oChatMessage]
        oAgentRunResponse: AgentRunResponse = await self.agent.run_async(messages)
        message_text: str = str(oAgentRunResponse)
        oMessage: Message = new_agent_text_message(message_text)
        await event_queue.enqueue_event(oMessage)

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("cancel not supported")  # pylint: disable=broad-exception-raised
