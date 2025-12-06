from typing import Optional

from a2a.types import AgentSkill
from pydantic import BaseModel

from agent_framework_sampler.ai.modules.chemistry_expert.agent_framework.agent.v1 import ChemistryExpertChatAgent
from agent_framework_sampler.utils.lodash import noop

noop(BaseModel)


class ChemistryAgentSkill(AgentSkill):
    id: str = ChemistryExpertChatAgent.__class__.__name__  # pyright: ignore  # FIXME
    name: str = ChemistryExpertChatAgent.__class__.__name__    # pyright: ignore  # FIXME
    description: str = "Answers questions from a chemistry perspective."
    tags: list[str] = ["science", "chemistry"]

    examples: Optional[list[str]] = ["Explain the concept of temperature from scientific perspectives."]
