from dataclasses import dataclass, field
from datetime import datetime, timezone
from random import randint
from typing import Annotated

from agent_framework import ChatAgent
from agent_framework._clients import ChatClientProtocol
from pydantic import Field


# SRC: https://github.com/microsoft/agent-framework/blob/python-1.0.0b251007/python/samples/getting_started/agents/azure_openai/azure_chat_client_with_function_tools.py
@dataclass
class WeatherAgent(ChatAgent):
    chat_client: ChatClientProtocol = field()

    instructions: str = field(default="You are a helpful assistant that can provide weather and time information.")

    def get_weather(
        self,
        location: Annotated[str, Field(description="The location to get the weather for.")],
    ) -> str:
        """Get the weather for a given location."""
        conditions = ["sunny", "cloudy", "rainy", "stormy"]
        return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."

    def get_time(self) -> str:
        """Get the current UTC time."""
        current_time = datetime.now(timezone.utc)
        return f"The current UTC time is {current_time.strftime('%Y-%m-%d %H:%M:%S')}."

    def __post_init__(self) -> None:
        return super().__init__(
            chat_client=self.chat_client,
            name=self.__class__.__name__,
            instructions=self.instructions,
            tools=[self.get_weather, self.get_time],
        )
