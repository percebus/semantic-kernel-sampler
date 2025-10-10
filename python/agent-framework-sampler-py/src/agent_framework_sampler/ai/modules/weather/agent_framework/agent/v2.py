from dataclasses import dataclass, field

from agent_framework import ChatAgent
from agent_framework._clients import ChatClientProtocol

from agent_framework_sampler.ai.modules.weather.agent_framework.tools.date_time.v1 import get_time
from agent_framework_sampler.ai.modules.weather.agent_framework.tools.weather.v2 import get_weather, get_weather_detail


# SRC: https://github.com/microsoft/agent-framework/blob/python-1.0.0b251007/python/samples/getting_started/tools/ai_tool_with_approval.py
@dataclass
class WeatherChatAgent_V2(ChatAgent):
    chat_client: ChatClientProtocol = field()

    instructions: str = field(default=("You are a helpful weather assistant. Use the get_weather tool to provide weather information."))

    def __post_init__(self) -> None:
        return super().__init__(
            chat_client=self.chat_client,
            name=self.__class__.__name__,
            instructions=self.instructions,
            tools=[get_weather, get_weather_detail, get_time],
        )
