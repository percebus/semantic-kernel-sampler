from dataclasses import dataclass, field
from typing import Optional

from semantic_kernel_sampler.sk.invokers.builtin.agents.threaded.chat.invoker import ChatCompletionBuiltinAgentInvoker


# SRC: https://github.com/microsoft/semantic-kernel/blob/main/python/samples/getting_started_with_agents/multi_agent_orchestration/step3_group_chat.py
@dataclass
class ContentReviewerBuiltinAgentInvoker(ChatCompletionBuiltinAgentInvoker):
    name: Optional[str] = field(default="Reviewer")

    description: Optional[str] = field(default="A content reviewer.")

    instructions: str = field(default="You are an excellent content reviewer. You review the content and provide feedback to the writer.")
