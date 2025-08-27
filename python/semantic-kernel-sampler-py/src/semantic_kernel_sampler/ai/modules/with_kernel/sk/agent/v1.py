from dataclasses import dataclass, field
from typing import Optional

from semantic_kernel_sampler.sk.invokers.builtin.agents.threaded.chat.invoker import ChatCompletionBuiltinAgentInvoker


@dataclass
class AssistantBuiltinAgentInvoker(ChatCompletionBuiltinAgentInvoker):

    description: Optional[str] = field(default="An assistant that answers questions")

    instructions: str = field(default="Answer the user's questions.")
