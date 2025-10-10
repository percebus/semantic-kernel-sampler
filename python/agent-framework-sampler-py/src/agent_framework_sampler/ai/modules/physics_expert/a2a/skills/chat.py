from typing import Optional

from a2a.types import AgentSkill
from pydantic import BaseModel

from agent_framework_sampler.ai.modules.physics_expert.agent_framework.agent.v1 import PhysicsExpertChatAgent
from agent_framework_sampler.utils.lodash import noop

noop(BaseModel)


class PhysicsAgentSkill(AgentSkill):
    id: str = PhysicsExpertChatAgent.__class__.__name__
    name: str = PhysicsExpertChatAgent.__class__.__name__
    description: str = "Answers questions from a physics perspective."
    tags: list[str] = ["science", "physics"]

    examples: Optional[list[str]] = ["Explain the concept of temperature from scientific perspectives."]
