import asyncio

from agent_framework_sampler.dependency_injection.container import container
from agent_framework_sampler.ai.modules.weather.ms.agent.v1 import WeatherAgent


# SRC: https://github.com/microsoft/agent-framework/blob/python-1.0.0b251007/python/samples/getting_started/agents/azure_ai/azure_ai_with_function_tools.py
async def run_async():
    async with (
        container[WeatherAgent] as oWeatherAgent,
    ):
        # First query - agent can use weather tool
        query1 = "What's the weather like in New York?"
        print(f"User: {query1}")
        result1 = await oWeatherAgent.run(query1)
        print(f"Agent: {result1}\n")

        # Second query - agent can use time tool
        query2 = "What's the current UTC time?"
        print(f"User: {query2}")
        result2 = await oWeatherAgent.run(query2)
        print(f"Agent: {result2}\n")

        # Third query - agent can use both tools if needed
        query3 = "What's the weather in London and what's the current UTC time?"
        print(f"User: {query3}")
        result3 = await oWeatherAgent.run(query3)
        print(f"Agent: {result3}\n")


if __name__ == "__main__":
    asyncio.run(run_async())
