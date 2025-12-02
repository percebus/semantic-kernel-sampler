import asyncio

from agent_framework_sampler.ai.modules.ms_learn.agent_framework.agent.v1 import MSLearnChatAgent
from agent_framework_sampler.ai.modules.ms_learn.agent_framework.tools.mcp.v1 import MSLearnMCPStreamableHttpTool
from agent_framework_sampler.dependency_injection.container import container


async def run_async() -> None:
    ms_learn_tool = container[MSLearnMCPStreamableHttpTool]
    chat_agent = container[MSLearnChatAgent]
    async with (
        ms_learn_tool,
        chat_agent,
    ):
        query = "What tools are available to you?"
        print(f"User: {query}")
        result = await chat_agent.run(query)
        print(f"Agent: {result.text}")


if __name__ == "__main__":
    asyncio.run(run_async())
