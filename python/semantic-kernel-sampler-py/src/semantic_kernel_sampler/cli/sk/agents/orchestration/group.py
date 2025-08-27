import asyncio

from semantic_kernel.contents import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole

from semantic_kernel_sampler.dependency_injection.container import container
from semantic_kernel_sampler.sk.invokers.builtin.agents.orchestration.group import GroupChatOrchestrationBuiltinAgentInvoker

# Simulate a conversation with the orchestrator
USER_INPUTS = [
    "Is the light on?",
    # "Turn on the light",
    # "What is 2 + 2?",
    # "Divide 14 by 9",
]


# pylint: disable-next=line-too-long
# SRC: https://github.com/microsoft/semantic-kernel/blob/python-1.35.2/python/samples/getting_started_with_agents/chat_completion/step03_chat_completion_agent_with_kernel.py
async def main():
    oGroupChatOrchestrationBuiltinAgentInvoker = container[GroupChatOrchestrationBuiltinAgentInvoker]

    for user_input in USER_INPUTS:
        print(f"# User: {user_input}")
        requestKernelContent = ChatMessageContent(role=AuthorRole.USER, content=user_input)
        messages: list[ChatMessageContent] = [requestKernelContent]

        oGroupChatOrchestrationBuiltinAgentInvoker.runtime.start()
        messages: list[ChatMessageContent] = await oGroupChatOrchestrationBuiltinAgentInvoker.invoke(messages)
        await oGroupChatOrchestrationBuiltinAgentInvoker.runtime.stop_when_idle()


if __name__ == "__main__":
    asyncio.run(main())
