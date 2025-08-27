import asyncio

from semantic_kernel.contents import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole

from semantic_kernel_sampler.ai.modules.mcp.demo.sk.agent.v2 import DemoMCPBuiltinAgentInvoker
from semantic_kernel_sampler.dependency_injection.container import container

# Simulate a conversation with the agent
USER_INPUTS = [
    "Add 2 and 3",
]


# pylint: disable-next=line-too-long
# SRC: https://github.com/microsoft/semantic-kernel/blob/python-1.35.2/python/samples/getting_started_with_agents/chat_completion/step03_chat_completion_agent_with_kernel.py
async def main():
    oThreadedBuiltinAgentInvoker = container[DemoMCPBuiltinAgentInvoker]

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
