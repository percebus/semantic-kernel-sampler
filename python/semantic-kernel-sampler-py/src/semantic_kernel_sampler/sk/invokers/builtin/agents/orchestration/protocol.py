from typing import Protocol

from semantic_kernel.contents import ChatMessageContent
from semantic_kernel.agents.runtime import InProcessRuntime


class BuiltinOrchestrationInvokerProtocol(Protocol):
    runtime: InProcessRuntime

    async def invoke(self, messages: list[ChatMessageContent]) -> list[ChatMessageContent]:
        ...
