from dataclasses import dataclass, field
from textwrap import dedent
from typing import Optional

from semantic_kernel_sampler.sk.invokers.builtin.agents.threaded.chat.invoker import ChatCompletionBuiltinAgentInvoker


@dataclass
class LightBuiltinAgentInvoker(ChatCompletionBuiltinAgentInvoker):
    description: Optional[str] = field(default="A light switch operator that turns on/off the light")

    instructions: str = field(
        default=dedent("""
        You are a helpful Light Switch assistant.
        You will only use the registered plugin(s).
        If it's not in the plugins, say 'I cannot help with that.'""")
    )
