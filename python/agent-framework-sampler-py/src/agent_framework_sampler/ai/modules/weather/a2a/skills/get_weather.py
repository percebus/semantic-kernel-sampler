from typing import Optional

from a2a.types import AgentSkill
from pydantic import BaseModel

from agent_framework_sampler.ai.modules.weather.agent_framework.tools.weather.v2 import get_weather
from agent_framework_sampler.utils.lodash import noop

noop(BaseModel)
noop(get_weather)


class GetWeatherAgentSkill(AgentSkill):
    id: str = "get_weather"

    name: str = "get weather"

    description: str = "Get the weather for a given location."

    tags: list[str] = ["weather", "location"]

    examples: Optional[list[str]] = ["What's the weather like in New York?", "What's the weather in London?"]
