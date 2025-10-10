from random import randrange
from typing import Annotated

from agent_framework import ai_function

conditions = ["sunny", "cloudy", "raining", "snowing", "clear"]


# SRC: https://github.com/microsoft/agent-framework/blob/python-1.0.0b251007/python/samples/getting_started/tools/ai_tool_with_approval.py
@ai_function
def get_weather(location: Annotated[str, "The city and state, e.g. San Francisco, CA"]) -> str:
    print(f"get_weather({location}) called")  # TODO logging
    """Get the current weather for a given location."""
    # Simulate weather data
    return f"The weather in {location} is {conditions[randrange(0, len(conditions))]} and {randrange(-10, 30)}°C."


# Define a simple weather tool that requires approval
@ai_function  # (approval_mode="always_require")  # TODO?
def get_weather_detail(location: Annotated[str, "The city and state, e.g. San Francisco, CA"]) -> str:
    """Get the current weather for a given location."""
    print(f"get_weather_detail({location}) called")  # TODO logging
    # Simulate weather data
    return (
        f"The weather in {location} is {conditions[randrange(0, len(conditions))]} and {randrange(-10, 30)}°C, "
        "with a humidity of 88%. "
        f"Tomorrow will be {conditions[randrange(0, len(conditions))]} with a high of {randrange(-10, 30)}°C."
    )
