from dataclasses import dataclass, field
from typing import Optional

from semantic_kernel_sampler.sk.invokers.builtin.agents.threaded.chat.invoker import ChatCompletionBuiltinAgentInvoker


# SRC: https://github.com/microsoft/semantic-kernel/blob/main/python/samples/getting_started_with_agents/multi_agent_orchestration/step3_group_chat.py
@dataclass
class ContentWriterBuiltinAgentInvoker(ChatCompletionBuiltinAgentInvoker):
    name: Optional[str] = field(default="Writer")

    description: Optional[str] = field(default="A content writer.")

    instructions: str = field(default="You are an excellent content writer. You create new content and edit contents based on the feedback.")
