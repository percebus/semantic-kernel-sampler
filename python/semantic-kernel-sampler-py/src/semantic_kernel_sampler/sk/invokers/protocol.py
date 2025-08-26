from typing import Generic, Optional, Protocol, TypeVar

from semantic_kernel.contents.kernel_content import KernelContent

TKernelContent = TypeVar("TKernelContent", bound=KernelContent)


# NOTE:
# ChatMessageContent inherits from KernelContent
# But ChatMessageAgent uses directly TMessage, which is specifically ChatMessageContent
# And does NOT like when we try to pass KernelContent
class InvokerProtocol(Generic[TKernelContent], Protocol):
    async def invoke(self, messages: list[TKernelContent]) -> Optional[TKernelContent]: ...
