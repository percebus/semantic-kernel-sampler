import asyncio

from semantic_kernel.contents import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole

from semantic_kernel_sampler.ai.modules.light.sk.agent.v3 import LightChatCompletionAgent
from semantic_kernel_sampler.dependency_injection.container import container
from semantic_kernel_sampler.sk.invokers.builtin.agents.threaded.invoker import ThreadedBuiltinAgentInvoker

# Simulate a conversation with the agent
USER_INPUTS = [
    "Is the light on?",
    "Turn on the light",
    "Is the light on?",
    "Toggle the light",
    "Is the light off?",
]


# SRC: https://github.com/microsoft/semantic-kernel/blob/python-1.35.2/python/samples/getting_started_with_agents/chat_completion/step03_chat_completion_agent_with_kernel.py
async def main():
    oAgent = container[LightChatCompletionAgent]
    oThreadedBuiltinAgentInvoker = ThreadedBuiltinAgentInvoker(agent=oAgent)

    for user_input in USER_INPUTS:
        print(f"# User: {user_input}")
        # Invoke the agent for a response
        oChatMessageContent = ChatMessageContent(role=AuthorRole.USER, content=user_input)
        response = await oThreadedBuiltinAgentInvoker.invoke(messages=[oChatMessageContent])
        print(f"# {response.name}: {response}")

    # Cleanup: Clear the thread
    await oThreadedBuiltinAgentInvoker.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
