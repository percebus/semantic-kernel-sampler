from dataclasses import dataclass, field
from textwrap import dedent
from typing import Optional

from semantic_kernel_sampler.sk.invokers.builtin.agents.threaded.chat.invoker import ChatCompletionBuiltinAgentInvoker


@dataclass
class BlogPostsMCPBuiltinAgentInvoker(ChatCompletionBuiltinAgentInvoker):
    name: Optional[str] = field(default="BlogPostPublisher")

    description: Optional[str] = field(
        default=dedent("""
            An agent that interfaces with an MCP server with tools to create, update, delete, find and get blog posts.""")
    )

    instructions: str = field(
        default=dedent("""
        Use your MCP integrations to manage blog posts.
        You can use the following tools:
        - posts_find
        - post_get
        - post_create
        - post_update

        If you cannot find a suitable tool, respond with 'I cannot help you with that'.
        """)
    )
