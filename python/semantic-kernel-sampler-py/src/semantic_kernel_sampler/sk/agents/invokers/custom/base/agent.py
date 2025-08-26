from abc import ABC
from dataclasses import dataclass, field

from semantic_kernel import Kernel

from semantic_kernel_sampler.rest.models.request import RequestModel
from semantic_kernel_sampler.rest.models.response import ResponseModel
from semantic_kernel_sampler.sk.agents.invokers.custom.protocol import CustomSemanticAgentInvokerProtocol


@dataclass
class CustomSemanticAgentInvokerBase(ABC, CustomSemanticAgentInvokerProtocol):
    kernel: Kernel = field()

    async def invoke(self, request: RequestModel) -> ResponseModel:
        raise NotImplementedError
