from typing import Protocol

from semantic_kernel.contents import ChatMessageContent


class HumanResponseProtocol(Protocol):
    def human_response_function(self) -> ChatMessageContent: ...
