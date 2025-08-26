# Copyright (c) Microsoft. All rights reserved.

import asyncio

from semantic_kernel.contents import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole

from semantic_kernel_sampler.ai.modules.with_kernel.sk.agent import AssistantAgentInvoker
from semantic_kernel_sampler.dependency_injection.container import container

"""
The following sample demonstrates how to create a chat completion agent that
answers user questions using the Azure Chat Completion service. The Chat Completion
Service is first added to the kernel, and the kernel is passed in to the
ChatCompletionAgent constructor. This sample demonstrates the basic steps to
create an agent and simulate a conversation with the agent.

Note: if both a service and a kernel are provided, the service will be used.

The interaction with the agent is via the `get_response` method, which sends a
user input to the agent and receives a response from the agent. The conversation
history needs to be maintained by the caller in the chat history object.
"""

# Simulate a conversation with the agent
USER_INPUTS = [
    "Hello, I am John Doe.",
    "What is your name?",
    "What is my name?",
]


# pylint: disable-next=line-too-long
# SRC: https://github.com/microsoft/semantic-kernel/blob/python-1.35.2/python/samples/getting_started_with_agents/chat_completion/step03_chat_completion_agent_with_kernel.py
async def main():
    oThreadedBuiltinAgentInvoker = container[AssistantAgentInvoker]

    for user_input in USER_INPUTS:
        print(f"# User: {user_input}")
        # Invoke the agent for a response
        oChatMessageContent = ChatMessageContent(role=AuthorRole.USER, content=user_input)
        response = await oThreadedBuiltinAgentInvoker.invoke(messages=[oChatMessageContent])
        print(f"# {response.name}: {response}")

    # Cleanup: Clear the thread
    await oThreadedBuiltinAgentInvoker.cleanup()

    """
    Sample output:
    # User: Hello, I am John Doe.
    # Assistant: Hello, John Doe! How can I assist you today?
    # User: What is your name?
    # Assistant: I don't have a personal name like a human does, but you can call me Assistant.?
    # User: What is my name?
    # Assistant: You mentioned that your name is John Doe. How can I assist you further, John?
    """


if __name__ == "__main__":
    asyncio.run(main())
