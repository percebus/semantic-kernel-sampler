import asyncio
from typing import TYPE_CHECKING

from agent_framework import ChatMessage, Role

from agent_framework_sampler.agent_framework.agents.builtin.chat.runner.threaded import ThreadedChatAgentRunner
from agent_framework_sampler.ai.modules.weather.agent_framework.agent.v1 import WeatherChatAgent
from agent_framework_sampler.dependency_injection.container import container

if TYPE_CHECKING:
    from agent_framework import AgentRunResponse


# SRC: https://github.com/microsoft/agent-framework/blob/python-1.0.0b251007/python/samples/getting_started/agents/azure_ai/azure_ai_with_function_tools.py
async def run_async():
    async with (
        container[WeatherChatAgent] as oWeatherChatAgent,
    ):
        oThreadedChatAgentRunner = ThreadedChatAgentRunner(
            chat_agent=oWeatherChatAgent,
        )

        # First query - agent can use weather tool
        query1 = ChatMessage(role=Role.USER, text="What's the weather like in New York?")
        print(f"User: {query1}")
        firstAgentRunResponse: AgentRunResponse = await oThreadedChatAgentRunner.run_async([query1])
        print(f"Agent: {firstAgentRunResponse}\n")

        # Second query - agent can use time tool
        query2 = ChatMessage(role=Role.USER, text="What's the current UTC time?")
        print(f"User: {query2}")
        secondAgentRunResponse: AgentRunResponse = await oThreadedChatAgentRunner.run_async([query2])
        print(f"Agent: {secondAgentRunResponse}\n")

        # Third query - agent can use both tools if needed
        query3 = ChatMessage(role=Role.USER, text="What's the weather in London and what's the current UTC time?")
        print(f"User: {query3}")
        thirdAgentRunResponse: AgentRunResponse = await oThreadedChatAgentRunner.run_async([query3])
        print(f"Agent: {thirdAgentRunResponse}\n")


if __name__ == "__main__":
    asyncio.run(run_async())
