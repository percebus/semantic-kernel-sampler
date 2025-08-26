from abc import ABC
from dataclasses import dataclass, field
from typing import Optional

from semantic_kernel import Kernel
from semantic_kernel.contents.kernel_content import KernelContent

from semantic_kernel_sampler.sk.invokers.protocol import InvokerProtocol


@dataclass
class CustomSemanticInvokerBase(ABC, InvokerProtocol[KernelContent]):
    kernel: Kernel = field()

    async def invoke(self, messages: list[KernelContent]) -> Optional[KernelContent]:
        raise NotImplementedError
