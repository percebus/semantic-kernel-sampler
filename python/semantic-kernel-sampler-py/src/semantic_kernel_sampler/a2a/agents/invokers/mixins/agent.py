from abc import ABC
from dataclasses import dataclass, field
from typing import Optional

from a2a.types import AgentCard

from semantic_kernel_sampler.a2a.agents.invokers.protocol import A2AgentInvokerProtocol
from semantic_kernel_sampler.rest.models.request import RequestModel
from semantic_kernel_sampler.rest.models.response import ResponseModel


@dataclass
class A2AgentMixin(ABC, A2AgentInvokerProtocol):
    agent_card: AgentCard = field(init=False)

    extended_agent_card: Optional[AgentCard] = field(default=None)

    async def invoke(self, request: RequestModel) -> ResponseModel:
        raise NotImplementedError
