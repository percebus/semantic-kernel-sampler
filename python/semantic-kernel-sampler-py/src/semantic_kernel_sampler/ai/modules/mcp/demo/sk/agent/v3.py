from textwrap import dedent
from typing import Any

from semantic_kernel.agents import ChatCompletionAgent


class DemoMCPChatCompletionAgent(ChatCompletionAgent):
    def model_post_init(self, __context: Any) -> None:
        self.name = "DemoMCPAgent"

        self.description = "An agent that interfaces with an MCP server with tools like 'greeting resource', and 'Add 2 numbers'."

        # fmt: off
        self.instructions = dedent("""
            Use your MCP integrations.
            You can use tools like:
            - add: Adds two numbers

            If you cannot find a suitable tool, respond with 'I cannot help you with that'.
        """)
        # fmt: on

        return super().model_post_init(__context)
