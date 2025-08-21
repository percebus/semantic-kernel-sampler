from typing import Optional, Protocol

from a2a.types import AgentCard

from semantic_kernel_sampler.rest.models.request import RequestModel
from semantic_kernel_sampler.rest.models.response import ResponseModel


class A2AgentProtocol(Protocol):
    agent_card: AgentCard

    extended_agent_card: Optional[AgentCard]

    # TODOs?
    # - Replace RequestModel for a2a.types.RequestContext
    # - Replace ResponseModel for a2a.types.Message
    async def invoke(self, request: RequestModel) -> ResponseModel: ...
