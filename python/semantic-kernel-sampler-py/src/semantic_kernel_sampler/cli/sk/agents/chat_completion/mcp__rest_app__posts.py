import asyncio
from calendar import c

from semantic_kernel.contents import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole

from semantic_kernel_sampler.ai.modules.mcp.rest_app.posts.sk.agent.v3 import BlogPostsMCPChatCompletionAgent
from semantic_kernel_sampler.ai.modules.mcp.rest_app.posts.sk.plugin.http import BlogPostsStreamableHttpMCPPlugin
from semantic_kernel_sampler.dependency_injection.container import container
from semantic_kernel_sampler.sk.agents.builtin.threaded.invoker import ThreadedBuiltinAgentInvoker


# SRC: https://github.com/microsoft/semantic-kernel/blob/python-1.35.2/python/samples/concepts/mcp/agent_with_http_mcp_plugin.py
async def main():
    oAgent = container[BlogPostsMCPChatCompletionAgent]
    oThreadedBuiltinAgentInvoker = ThreadedBuiltinAgentInvoker(agent=oAgent)

    async with container[BlogPostsStreamableHttpMCPPlugin]:
        while True:
            user_input = input("User: ")
            # Invoke the agent for a response
            oChatMessageContent = ChatMessageContent(role=AuthorRole.USER, content=user_input)
            response = await oThreadedBuiltinAgentInvoker.invoke(messages=[oChatMessageContent])
            print(f"# {response.name}: {response}")

    # Cleanup: Clear the thread
    # await oThreadedBuiltinAgentInvoker.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
