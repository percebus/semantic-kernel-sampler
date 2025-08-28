import asyncio

from semantic_kernel.contents import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole

from semantic_kernel_sampler.dependency_injection.container import container
from semantic_kernel_sampler.sk.agents.builtin.orchestration.group import GroupChatBuiltinOrchestrationInvoker

# Simulate a conversation with the orchestrator
USER_INPUTS = [
    "Create a slogan for a new electric SUV that is affordable and fun to drive",
]


# SRC: https://github.com/microsoft/semantic-kernel/blob/python-1.35.2/python/samples/getting_started_with_agents/chat_completion/step03_chat_completion_agent_with_kernel.py
async def main():
    invoker = container[GroupChatBuiltinOrchestrationInvoker]

    for user_input in USER_INPUTS:
        print(f"# User: {user_input}")
        requestKernelContent = ChatMessageContent(role=AuthorRole.USER, content=user_input)
        messages: list[ChatMessageContent] = [requestKernelContent]

        invoker.runtime.start()
        messages: list[ChatMessageContent] = await invoker.invoke(messages)
        await invoker.runtime.stop_when_idle()


if __name__ == "__main__":
    asyncio.run(main())
