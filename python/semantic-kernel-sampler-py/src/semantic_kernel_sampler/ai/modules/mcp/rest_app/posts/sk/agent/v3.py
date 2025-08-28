from textwrap import dedent
from typing import Any

from semantic_kernel.agents import ChatCompletionAgent


class BlogPostsMCPChatCompletionAgent(ChatCompletionAgent):
    def model_post_init(self, __context: Any) -> None:
        self.name = "BlogPostPublisher"

        self.description = "An agent that interfaces with an MCP server with tools to create, update, delete, find and get blog posts."

        # fmt: off
        self.instructions = dedent("""
            Use ONLY your MCP integrations to manage blog posts.
            You can use the following tools:
            - posts_find
            - post_get
            - post_create
            - post_update

            If you cannot find a suitable tool, respond with 'I cannot help you with that'.
        """)
        # fmt: on

        return super().model_post_init(__context)
