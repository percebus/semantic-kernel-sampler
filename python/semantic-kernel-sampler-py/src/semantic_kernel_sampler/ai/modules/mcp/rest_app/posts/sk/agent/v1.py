from dataclasses import dataclass, field
from textwrap import dedent
from typing import Optional

from semantic_kernel_sampler.sk.invokers.builtin.agents.threaded.chat.invoker import ChatCompletionBuiltinAgentInvoker


@dataclass
class BlogPostsMCPBuiltinAgentInvoker(ChatCompletionBuiltinAgentInvoker):
    description: Optional[str] = field(
        default=dedent("""
            An agent that interfaces with an MCP server with tools to create, update, delete, find and get blog posts.""")
    )

    instructions: str = field(
        default=dedent("""
        You are a helpful assistant that leverages MCP services.
        You will only use the registered plugin(s).
        If it's not in the plugins, say 'I cannot help with that.'""")
    )
