from dataclasses import dataclass, field

from agent_framework import ChatAgent
from agent_framework._clients import ChatClientProtocol


# SRC: https://github.com/microsoft/agent-framework/blob/python-1.0.0b251007/python/samples/semantic-kernel-migration/orchestrations/concurrent_basic.py
@dataclass
class PhysicsExpertChatAgent(ChatAgent):
    chat_client: ChatClientProtocol = field()

    instructions: str = field(default="You are an expert in physics. Answer questions from a physics perspective.")

    def __post_init__(self) -> None:
        return super().__init__(
            chat_client=self.chat_client,
            name=self.__class__.__name__,
            instructions=self.instructions,
        )
