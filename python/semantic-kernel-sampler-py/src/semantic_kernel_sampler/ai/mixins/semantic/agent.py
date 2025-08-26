from abc import ABC
from dataclasses import dataclass, field

from semantic_kernel import Kernel

from semantic_kernel_sampler.a2a.agents.protocol import A2AgentProtocol
from semantic_kernel_sampler.rest.models.request import RequestModel
from semantic_kernel_sampler.rest.models.response import ResponseModel


@dataclass
class SemanticAgentMixin(ABC, A2AgentProtocol):
    kernel: Kernel = field()

    async def invoke(self, request: RequestModel) -> ResponseModel:
        raise NotImplementedError
