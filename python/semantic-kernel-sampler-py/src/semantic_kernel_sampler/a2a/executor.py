from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message

from semantic_kernel_sampler.a2a.agents.protocol import AgentProtocol
from semantic_kernel_sampler.rest.models.request import RequestModel

if TYPE_CHECKING:
    from a2a.types import Message

    from semantic_kernel_sampler.rest.models.response import ResponseModel


# SRC: https://github.com/a2aproject/a2a-samples/blob/main/samples/python/agents/helloworld/agent_executor.py
@dataclass
class MyAgentExecutor(AgentExecutor):
    agent: AgentProtocol = field()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        user_input: str = context.get_user_input()
        request: RequestModel = RequestModel(message=user_input)
        response: ResponseModel = await self.agent.invoke(request)
        if not response.message:
            raise ValueError("No message found in response")

        message: Message = new_agent_text_message(response.message)
        await event_queue.enqueue_event(message)

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("cancel not supported")  # pylint: disable=broad-exception-raised
