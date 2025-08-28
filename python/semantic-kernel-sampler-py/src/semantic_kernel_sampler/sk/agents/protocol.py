from typing import Optional, Protocol

from semantic_kernel.contents.kernel_content import KernelContent


class InvokerProtocol(Protocol):
    async def invoke(self, messages: list[KernelContent]) -> Optional[KernelContent]: ...
