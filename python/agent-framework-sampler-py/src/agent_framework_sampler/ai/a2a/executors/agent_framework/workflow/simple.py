from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Sequence

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message

from agent_framework import ChatMessage, Role, Workflow, WorkflowRunResult

from agent_framework_sampler.config.mixin import ConfigurableMixin

if TYPE_CHECKING:
    from a2a.types import Message


# SRC: https://github.com/a2aproject/a2a-samples/blob/main/samples/python/agents/helloworld/agent_executor.py
@dataclass
class SimpleWorkflowA2AgentFrameworkExecutor(ConfigurableMixin, AgentExecutor):
    workflow: Workflow = field()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        user_input: str = context.get_user_input()
        oChatMessage = ChatMessage(role=Role.USER, text=user_input)
        messages: list[ChatMessage] = [oChatMessage]
        oWorkflowRunResult: WorkflowRunResult = await self.workflow.run(messages)
        output_messages: Sequence[ChatMessage] = oWorkflowRunResult.get_outputs()

        # fmt: off
        responses = (
            message.text
            for message in output_messages
            if message.role != Role.USER)
        # fmt: on

        message_text: str = self.settings.multi_agent_delimiter.join(responses)
        a2aMessage: Message = new_agent_text_message(message_text)
        await event_queue.enqueue_event(a2aMessage)

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("cancel not supported")  # pylint: disable=broad-exception-raised
