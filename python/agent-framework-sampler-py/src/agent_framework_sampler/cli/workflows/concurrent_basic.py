import asyncio
from typing import Sequence, cast

from agent_framework import ChatMessage, Role, Workflow, WorkflowOutputEvent

from agent_framework_sampler.dependency_injection.container import container

PROMPT = "Explain the concept of temperature from multiple scientific perspectives."


async def run_agent_framework_example(prompt: str) -> Sequence[list[ChatMessage]]:
    oWorkflow = container[Workflow]
    outputs: list[list[ChatMessage]] = []
    async for oWorkflowEvent in oWorkflow.run_stream(prompt):  # type: ignore  # FIXME
        if isinstance(oWorkflowEvent, WorkflowOutputEvent):
            messages: list[ChatMessage] = cast("list[ChatMessage]", oWorkflowEvent.data)
            outputs.append(messages)

    return outputs


def _print_agent_framework_outputs(conversations: Sequence[Sequence[ChatMessage]]) -> None:
    if not conversations:
        print("No Agent Framework output.")
        return

    print("===== Agent Framework Concurrent =====")
    for index, messages in enumerate(conversations, start=1):
        print(f"--- Conversation {index} ---")
        for message in messages:
            name = message.author_name or Role.ASSISTANT
            print(f"[{name}] {message.text}")
        print()


# SRC: https://github.com/microsoft/agent-framework/blob/python-1.0.0b251007/python/samples/semantic-kernel-migration/orchestrations/concurrent_basic.py
async def run_async():
    agent_framework_outputs: Sequence[Sequence[ChatMessage]] = await run_agent_framework_example(PROMPT)
    _print_agent_framework_outputs(agent_framework_outputs)


if __name__ == "__main__":
    asyncio.run(run_async())
