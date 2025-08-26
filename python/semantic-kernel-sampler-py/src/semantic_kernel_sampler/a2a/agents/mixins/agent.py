from abc import ABC
from dataclasses import dataclass, field
from typing import Optional

from a2a.types import AgentCard

from semantic_kernel_sampler.a2a.agents.protocol import A2AgentProtocol
from semantic_kernel_sampler.rest.models.request import RequestModel
from semantic_kernel_sampler.rest.models.response import ResponseModel
from semantic_kernel_sampler.utils.lodash import noop

noop(A2AgentProtocol)


@dataclass
class A2AgentMixin(ABC, A2AgentProtocol):
    agent_card: AgentCard = field(init=False)

    extended_agent_card: Optional[AgentCard] = field(default=None)

    async def invoke(self, request: RequestModel) -> ResponseModel:
        raise NotImplementedError
