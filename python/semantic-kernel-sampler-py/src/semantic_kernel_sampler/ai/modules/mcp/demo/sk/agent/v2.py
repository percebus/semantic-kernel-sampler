from dataclasses import dataclass, field
from textwrap import dedent
from typing import Optional

from semantic_kernel_sampler.sk.invokers.builtin.agents.threaded.chat.invoker import ChatCompletionBuiltinAgentInvoker


@dataclass
class DemoMCPBuiltinAgentInvoker(ChatCompletionBuiltinAgentInvoker):
    description: Optional[str] = field(
        default="An agent that interfaces with an MCP server with tools like 'greeting resource', and 'Add 2 numbers'."
    )

    instructions: str = field(
        default=dedent("""
        You can use tools like:
        - add: Adds two numbers

        If you cannot find a suitable tool, respond with 'I cannot help you with that'.
        """)
    )
