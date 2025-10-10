from typing import Optional

from a2a.types import AgentSkill
from pydantic import BaseModel

from agent_framework_sampler.ai.modules.weather.agent_framework.tools.date_time.v1 import get_time
from agent_framework_sampler.utils.lodash import noop

noop(BaseModel)
noop(get_time)


class GetTimeAgentSkill(AgentSkill):
    id: str = "get_time"
    name: str = "get time"
    description: str = "Get the current UTC time."
    tags: list[str] = ["time", "utc"]

    examples: Optional[list[str]] = [
        "What's the current UTC time?",
    ]
