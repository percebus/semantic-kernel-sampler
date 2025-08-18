from abc import ABC
from dataclasses import dataclass, field
from typing import Optional

from a2a.types import AgentCard

from semantic_kernel_sampler.agents.a2a.protocol import AgentProtocol
from semantic_kernel_sampler.configuration.config import Config
from semantic_kernel_sampler.rest.models.request import RequestModel
from semantic_kernel_sampler.rest.models.response import ResponseModel


@dataclass
class AgentBase(ABC, AgentProtocol):
    config: Config = field()

    agent_card: AgentCard = field(init=False)

    extended_agent_card: Optional[AgentCard] = field(default=None)

    async def invoke(self, request: RequestModel) -> ResponseModel:
        raise NotImplementedError
