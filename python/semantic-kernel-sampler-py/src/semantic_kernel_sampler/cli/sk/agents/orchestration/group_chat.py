import asyncio
from logging import Logger

from semantic_kernel.agents import GroupChatManager, GroupChatOrchestration  # pylint: disable=no-name-in-module
from semantic_kernel.agents.runtime import InProcessRuntime
from semantic_kernel.contents import ChatMessageContent, FunctionCallContent, FunctionResultContent
from semantic_kernel.contents.utils.author_role import AuthorRole

from semantic_kernel_sampler.ai.modules.content_reviewer.sk.agent.v2 import ContentReviewerChatCompletionAgent
from semantic_kernel_sampler.ai.modules.content_writer.sk.agent.v2 import ContentWriterChatCompletionAgent
from semantic_kernel_sampler.dependency_injection.container import container
from semantic_kernel_sampler.sk.invokers.builtin.agents.orchestration.group import GroupChatBuiltinOrchestrationInvoker

# Simulate a conversation with the orchestrator
USER_INPUTS = [
    "Create a slogan for a new electric SUV that is affordable and fun to drive",
]


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


# SRC: https://github.com/microsoft/semantic-kernel/blob/python-1.35.2/python/samples/getting_started_with_agents/chat_completion/step03_chat_completion_agent_with_kernel.py
async def main():
    oOrchestration = GroupChatOrchestration(
        manager=container[GroupChatManager],
        agent_response_callback=agent_response_callback,  # pyright: ignore[reportArgumentType]
        members=[
            container[ContentWriterChatCompletionAgent],
            container[ContentReviewerChatCompletionAgent],
            # c[BlogPostsMCPChatCompletionAgent],   # TODO? or XXX? the 2 other agents are VERY chatty
        ],
    )

    invoker = GroupChatBuiltinOrchestrationInvoker(logger=container[Logger], runtime=container[InProcessRuntime], orchestration=oOrchestration)

    for user_input in USER_INPUTS:
        print(f"# User: {user_input}")
        requestKernelContent = ChatMessageContent(role=AuthorRole.USER, content=user_input)
        messages: list[ChatMessageContent] = [requestKernelContent]

        invoker.runtime.start()
        messages: list[ChatMessageContent] = await invoker.invoke(messages)
        await invoker.runtime.stop_when_idle()


if __name__ == "__main__":
    asyncio.run(main())
