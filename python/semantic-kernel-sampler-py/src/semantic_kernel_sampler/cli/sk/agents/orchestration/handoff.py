import asyncio
from typing import TYPE_CHECKING

from semantic_kernel_sampler.dependency_injection.container import container
from semantic_kernel_sampler.sk.agents.builtin.contents.human.protocol import HumanResponseProtocol
from semantic_kernel_sampler.sk.agents.builtin.orchestration.handoff import HandoffBuiltinOrchestrationInvoker

if TYPE_CHECKING:
    from semantic_kernel.contents import ChatMessageContent

    from semantic_kernel_sampler.sk.agents.builtin.contents.human.cli import InputHumanResponse


# SRC: https://github.com/microsoft/semantic-kernel/blob/python-1.35.2/python/samples/getting_started_with_agents/multi_agent_orchestration/step4_handoff.py
async def main():
    invoker = container[HandoffBuiltinOrchestrationInvoker]

    oInputHumanResponse: InputHumanResponse = container[HumanResponseProtocol]  # pyright: ignore[reportAssignmentType]
    requestKernelContent = oInputHumanResponse.human_response_function()
    messages: list[ChatMessageContent] = [requestKernelContent]

    invoker.runtime.start()
    messages: list[ChatMessageContent] = await invoker.invoke(messages)
    await invoker.runtime.stop_when_idle()


if __name__ == "__main__":
    asyncio.run(main())
