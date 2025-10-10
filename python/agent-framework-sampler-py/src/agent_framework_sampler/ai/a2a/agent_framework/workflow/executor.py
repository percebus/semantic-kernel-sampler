from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Sequence

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message
from agent_framework import ChatMessage, Role, WorkflowRunResult

from agent_framework_sampler.agent_framework.builtin.workflow.runner.protocol import WorkflowRunnerProtocol

if TYPE_CHECKING:
    from a2a.types import Message


# SRC: https://github.com/a2aproject/a2a-samples/blob/main/samples/python/agents/helloworld/agent_executor.py
@dataclass
class WorkflowA2AgentFrameworkRunnerExecutor(AgentExecutor):
    workflow: WorkflowRunnerProtocol = field()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        user_input: str = context.get_user_input()
        oChatMessage = ChatMessage(role=Role.USER, text=user_input)
        messages: list[ChatMessage] = [oChatMessage]
        oWorkflowRunResult: WorkflowRunResult = await self.workflow.run_async(messages)

        responses: Sequence[ChatMessage] = oWorkflowRunResult.get_outputs()
        message_text: str = "\n".join(responses)
        oMessage: Message = new_agent_text_message(message_text)
        await event_queue.enqueue_event(oMessage)

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("cancel not supported")  # pylint: disable=broad-exception-raised
