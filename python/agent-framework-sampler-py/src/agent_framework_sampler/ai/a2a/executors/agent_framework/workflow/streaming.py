from dataclasses import dataclass, field
from typing import TYPE_CHECKING, cast

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message

from agent_framework import ChatMessage, Role, Workflow, WorkflowOutputEvent
from agent_framework_sampler.config.mixin import ConfigurableMixin

if TYPE_CHECKING:
    from a2a.types import Message


# SRC: https://github.com/a2aproject/a2a-samples/blob/main/samples/python/agents/helloworld/agent_executor.py
@dataclass
class StreamingWorkflowA2AgentFrameworkExecutor(ConfigurableMixin, AgentExecutor):
    workflow: Workflow = field()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        user_input: str = context.get_user_input()
        conversations: list[list[ChatMessage]] = []
        async for oWorkflowEvent in self.workflow.run_stream(user_input):
            if isinstance(oWorkflowEvent, WorkflowOutputEvent):
                input_messages: list[ChatMessage] = cast("list[ChatMessage]", oWorkflowEvent.data)
                conversations.append(input_messages)
                if self.settings.debug:
                    for message in input_messages:
                        name = message.author_name or Role.ASSISTANT
                        print(f"[{name}] {message.text}")
                    print()

        # fmt: off
        output_messages: list[ChatMessage] = [
            message
            for messages in conversations
            for message in messages
            if message.role != Role.USER
        ]
        # fmt: on

        responses = (message.text for message in output_messages)
        message_text: str = self.settings.multi_agent_delimiter.join(responses)
        a2aMessage: Message = new_agent_text_message(message_text)
        await event_queue.enqueue_event(a2aMessage)

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("cancel not supported")  # pylint: disable=broad-exception-raised
