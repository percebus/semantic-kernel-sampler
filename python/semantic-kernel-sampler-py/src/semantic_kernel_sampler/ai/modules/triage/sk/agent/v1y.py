from dataclasses import dataclass, field
from typing import Optional

from semantic_kernel_sampler.sk.invokers.builtin.agents.threaded.chat.invoker import ChatCompletionBuiltinAgentInvoker


# SRC: https://github.com/microsoft/semantic-kernel/python-1.35.2/main/python/samples/getting_started_with_agents/multi_agent_orchestration/step4_handoff.py
@dataclass
class TriageBuiltinAgentInvoker(ChatCompletionBuiltinAgentInvoker):
    name: Optional[str] = field(default="Triage")

    description: Optional[str] = field(default="A customer support agent that triages issues.")

    instructions: str = field(default="Handle customer requests.")
