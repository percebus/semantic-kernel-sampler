import asyncio
from typing import TYPE_CHECKING

from agent_framework import ChatMessage, Role

from agent_framework_sampler.agent_framework.builtin.agent.chat.runner.threaded import ThreadedChatAgentRunner
from agent_framework_sampler.ai.modules.weather.agent_framework.agent.v2 import WeatherChatAgent_V2
from agent_framework_sampler.dependency_injection.container import container

if TYPE_CHECKING:
    from agent_framework import AgentRunResponse


# SRC: https://github.com/microsoft/agent-framework/blob/python-1.0.0b251007/python/samples/getting_started/agents/azure_ai/azure_ai_with_function_tools.py
async def tools_on_agent_level():
    async with (
        container[WeatherChatAgent_V2] as oWeatherChatAgent,
    ):
        oThreadedChatAgentRunner = ThreadedChatAgentRunner(
            chat_agent=oWeatherChatAgent,
        )

        # First query - agent can use weather tool
        firstChatMessage = ChatMessage(role=Role.USER, text="What's the weather like in New York?")
        print(f"User: {firstChatMessage.text}")
        firstAgentRunResponse: AgentRunResponse = await oThreadedChatAgentRunner.run_async([firstChatMessage])
        print(f"Agent: {firstAgentRunResponse}\n")

        # Second query - agent can use time tool
        secondChatMessage = ChatMessage(role=Role.USER, text="What's the current UTC time?")
        print(f"User: {secondChatMessage.text}")
        secondAgentRunResponse: AgentRunResponse = await oThreadedChatAgentRunner.run_async([secondChatMessage])
        print(f"Agent: {secondAgentRunResponse}\n")

        # Third query - agent can use both tools if needed
        thirdChatMessage = ChatMessage(role=Role.USER, text="What's the weather in London and what's the current UTC time?")
        print(f"User: {thirdChatMessage.text}")
        thirdAgentRunResponse: AgentRunResponse = await oThreadedChatAgentRunner.run_async([thirdChatMessage])
        print(f"Agent: {thirdAgentRunResponse}\n")


async def run_weather_agent():
    async with (
        container[WeatherChatAgent_V2] as oWeatherChatAgent,
    ):
        oThreadedChatAgentRunner = ThreadedChatAgentRunner(
            chat_agent=oWeatherChatAgent,
        )
        firstChatMessage = ChatMessage(
            role=Role.USER, text="Can you give me an update of the weather in LA and Portland and detailed weather for Seattle?"
        )
        print(f"User: {firstChatMessage.text}")
        oAgentRunResponse: AgentRunResponse = await oThreadedChatAgentRunner.run_async([firstChatMessage])
        print(f"Agent: {oAgentRunResponse}\n")

        secondChatMessage = ChatMessage(role=Role.USER, text="Can you give me **detailed** weather for Seattle?")
        print(f"User: {secondChatMessage.text}")
        oAgentRunResponse: AgentRunResponse = await oThreadedChatAgentRunner.run_async([secondChatMessage])
        print(f"Agent: {oAgentRunResponse}\n")


async def run_async():
    await tools_on_agent_level()
    await run_weather_agent()


if __name__ == "__main__":
    asyncio.run(run_async())
