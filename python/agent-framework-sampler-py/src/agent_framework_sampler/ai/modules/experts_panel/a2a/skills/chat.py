from typing import Optional

from a2a.types import AgentSkill
from pydantic import BaseModel

from agent_framework_sampler.utils.lodash import noop

noop(BaseModel)


class MultiExpertPanelAgentSkill(AgentSkill):
    id: str = "multi-expert-science-panel"
    name: str = "MultiExpertSciencePanel"
    description: str = "Provides a single answer to a question from multiple scientific perspectives."
    tags: list[str] = ["science", "chemistry", "physics"]
    examples: Optional[list[str]] = ["Explain the concept of temperature from multiple scientific perspectives."]
