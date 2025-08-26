from typing import Optional, Protocol

from semantic_kernel import Kernel
from semantic_kernel.contents.kernel_content import KernelContent


class CustomSemanticInvokerProtocol(Protocol):
    kernel: Kernel

    async def invoke(self, message: KernelContent) -> Optional[KernelContent]: ...
