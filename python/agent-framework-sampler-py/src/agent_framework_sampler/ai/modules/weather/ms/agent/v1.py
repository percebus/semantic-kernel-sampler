from dataclasses import dataclass, field

from agent_framework import ChatAgent
from agent_framework._clients import ChatClientProtocol

from agent_framework_sampler.ai.modules.weather.tools.date_time.v1 import get_time
from agent_framework_sampler.ai.modules.weather.tools.weather.v1 import get_weather


# SRC: https://github.com/microsoft/agent-framework/blob/python-1.0.0b251007/python/samples/getting_started/agents/azure_openai/azure_chat_client_with_function_tools.py
@dataclass
class WeatherChatAgent(ChatAgent):
    chat_client: ChatClientProtocol = field()

    instructions: str = field(default="You are a helpful assistant that can provide weather and time information.")

    def __post_init__(self) -> None:
        return super().__init__(
            chat_client=self.chat_client,
            name=self.__class__.__name__,
            instructions=self.instructions,
            tools=[get_weather, get_time],
        )
