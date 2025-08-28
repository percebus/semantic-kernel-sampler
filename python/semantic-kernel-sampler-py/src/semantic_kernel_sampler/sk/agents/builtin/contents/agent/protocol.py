from typing import Protocol

from semantic_kernel.contents import ChatMessageContent


class AgentResponseProtocol(Protocol):
    def agent_response_callback(self, message: ChatMessageContent) -> None: ...
