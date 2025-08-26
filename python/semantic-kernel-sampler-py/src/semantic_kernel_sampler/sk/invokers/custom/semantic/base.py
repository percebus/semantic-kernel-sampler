from abc import ABC
from dataclasses import dataclass, field
from typing import Optional

from semantic_kernel import Kernel
from semantic_kernel.contents.kernel_content import KernelContent

from semantic_kernel_sampler.sk.invokers.custom.semantic.protocol import CustomSemanticInvokerProtocol


@dataclass
class CustomSemanticInvokerBase(ABC, CustomSemanticInvokerProtocol):
    kernel: Kernel = field()

    async def invoke(self, message: KernelContent) -> Optional[KernelContent]:
        raise NotImplementedError
