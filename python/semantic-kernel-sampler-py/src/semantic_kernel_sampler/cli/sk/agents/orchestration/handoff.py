import asyncio

from semantic_kernel.contents import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole

from semantic_kernel_sampler.dependency_injection.container import container
from semantic_kernel_sampler.sk.invokers.builtin.agents.orchestration.handoff import HandoffBuiltinOrchestrationInvoker

USER_INPUTS = [
    # "I want to turn on the light",
    "I want to know what is 2 + 2",
    # "What is the closest planet to the sun?",
    # "Can you wible wable to wabliton?"
]


def human_response_callback() -> ChatMessageContent:
    user_input = input("User: ")
    return ChatMessageContent(role=AuthorRole.USER, content=user_input)

# SRC: https://github.com/microsoft/semantic-kernel/blob/python-1.35.2/python/samples/getting_started_with_agents/multi_agent_orchestration/step4_handoff.py
async def main():
    oHandoffBuiltinOrchestrationInvoker = container[HandoffBuiltinOrchestrationInvoker]
    oHandoffBuiltinOrchestrationInvoker.human_response_callback = human_response_callback

    for user_input in USER_INPUTS:
        print(f"# User: {user_input}")
        requestKernelContent = ChatMessageContent(role=AuthorRole.USER, content=user_input)
        messages: list[ChatMessageContent] = [requestKernelContent]

        oHandoffBuiltinOrchestrationInvoker.runtime.start()
        messages: list[ChatMessageContent] = await oHandoffBuiltinOrchestrationInvoker.invoke(messages)
        await oHandoffBuiltinOrchestrationInvoker.runtime.stop_when_idle()


if __name__ == "__main__":
    asyncio.run(main())
