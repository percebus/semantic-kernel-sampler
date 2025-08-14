from typing import Protocol

from semantic_kernel_sampler.rest.models.request import RequestModel
from semantic_kernel_sampler.rest.models.response import ResponseModel


class AgentProtocol(Protocol):
    async def invoke(self, request: RequestModel) -> ResponseModel: ...
