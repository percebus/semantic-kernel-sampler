import asyncio

from semantic_kernel.contents import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole

from semantic_kernel_sampler.ai.modules.mcp.mslearn.sk.agent.v1 import MsLearnMCPChatCompletionAgent
from semantic_kernel_sampler.dependency_injection.container import container
from semantic_kernel_sampler.sk.agents.builtin.threaded.invoker import ThreadedBuiltinAgentInvoker
from semantic_kernel_sampler.third_party.microsoft.learn.api.mcp import LearnSiteMCPStreamableHttpPlugin

# Simulate a conversation with the agent
USER_INPUTS = [
    "How do I make a Python chat completion request in Semantic Kernel using Azure OpenAI?",
]


# SRC: https://github.com/microsoft/semantic-kernel/blob/python-1.35.2/python/samples/concepts/mcp/agent_with_http_mcp_plugin.py
async def main():
    oAgent = container[MsLearnMCPChatCompletionAgent]
    oThreadedBuiltinAgentInvoker = ThreadedBuiltinAgentInvoker(agent=oAgent)

    async with container[LearnSiteMCPStreamableHttpPlugin]:
        for user_input in USER_INPUTS:
            # Invoke the agent for a response
            oChatMessageContent = ChatMessageContent(role=AuthorRole.USER, content=user_input)
            response = await oThreadedBuiltinAgentInvoker.invoke(messages=[oChatMessageContent])
            print(f"# {response.name}: {response}")

    # Cleanup: Clear the thread
    await oThreadedBuiltinAgentInvoker.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
