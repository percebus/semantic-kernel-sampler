from dataclasses import dataclass, field

from agent_framework import ChatAgent
from agent_framework._clients import ChatClientProtocol


# SRC: https://github.com/microsoft/agent-framework/blob/python-1.0.0b251007/python/samples/semantic-kernel-migration/orchestrations/concurrent_basic.py
@dataclass
class ChemistryExpertChatAgent(ChatAgent):
    chat_client: ChatClientProtocol = field()

    instructions: str = field(default="You are an expert in chemistry. Answer questions from a chemistry perspective.")

    def __post_init__(self) -> None:
        return super().__init__(
            chat_client=self.chat_client,
            name=self.__class__.__name__,
            instructions=self.instructions,
        )
