import asyncio
from logging import Logger

from semantic_kernel.agents import HandoffOrchestration, OrchestrationHandoffs
from semantic_kernel.agents.runtime import InProcessRuntime
from semantic_kernel.contents import ChatMessageContent, FunctionCallContent, FunctionResultContent
from semantic_kernel.contents.utils.author_role import AuthorRole

from semantic_kernel_sampler.ai.modules.basic.sk.agent.v2 import BasicChatCompletionAgent
from semantic_kernel_sampler.ai.modules.light.sk.agent.v3 import LightChatCompletionAgent
from semantic_kernel_sampler.ai.modules.math.sk.agent.v3 import MathChatCompletionAgent
from semantic_kernel_sampler.ai.modules.triage.sk.agent.v1 import TriageChatCompletionAgent
from semantic_kernel_sampler.dependency_injection.container import container
from semantic_kernel_sampler.sk.invokers.builtin.agents.orchestration.handoff import HandoffBuiltinOrchestrationInvoker


def agent_response_callback(message: ChatMessageContent) -> None:
    """Observer function to print the messages from the agents.

    Please note that this function is called whenever the agent generates a response,
    including the internal processing messages (such as tool calls) that are not visible
    to other agents in the orchestration.
    """
    print(f"{message.name}: {message.content}")
    for item in message.items:
        if isinstance(item, FunctionCallContent):
            print(f"Calling '{item.name}' with arguments '{item.arguments}'")
        if isinstance(item, FunctionResultContent):
            print(f"Result from '{item.name}' is '{item.result}'")


def human_response_function() -> ChatMessageContent:
    user_input = input("User: ")
    return ChatMessageContent(role=AuthorRole.USER, content=user_input)


# SRC: https://github.com/microsoft/semantic-kernel/blob/python-1.35.2/python/samples/getting_started_with_agents/multi_agent_orchestration/step4_handoff.py
async def main():
    oOrchestration = HandoffOrchestration(
        agent_response_callback=agent_response_callback,  # pyright: ignore[reportArgumentType]
        human_response_function=human_response_function,
        handoffs=container[OrchestrationHandoffs],
        members=[
            container[TriageChatCompletionAgent],
            container[BasicChatCompletionAgent],
            container[LightChatCompletionAgent],
            container[MathChatCompletionAgent],
        ],
    )

    invoker = HandoffBuiltinOrchestrationInvoker(
        logger=container[Logger],
        runtime=container[InProcessRuntime],
        orchestration=oOrchestration,
    )

    requestKernelContent = human_response_function()
    messages: list[ChatMessageContent] = [requestKernelContent]

    invoker.runtime.start()
    messages: list[ChatMessageContent] = await invoker.invoke(messages)
    await invoker.runtime.stop_when_idle()


if __name__ == "__main__":
    asyncio.run(main())
