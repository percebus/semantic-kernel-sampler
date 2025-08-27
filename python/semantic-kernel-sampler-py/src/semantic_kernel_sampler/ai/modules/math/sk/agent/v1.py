from dataclasses import dataclass, field
from textwrap import dedent
from typing import Optional

from semantic_kernel_sampler.sk.invokers.builtin.agents.threaded.chat.invoker import ChatCompletionBuiltinAgentInvoker


@dataclass
class MathBuiltinAgentInvoker(ChatCompletionBuiltinAgentInvoker):
    description: Optional[str] = field(default="A 3rd grade math teacher that answers questions about basic operations")

    # TODO get from a file
    instructions: str = field(
        default=dedent("""
        You are a helpful Mathematician assistant.
        You will only use the registered plugin(s).
        If it's not in the plugins, say 'I cannot help with that.'""")
    )
