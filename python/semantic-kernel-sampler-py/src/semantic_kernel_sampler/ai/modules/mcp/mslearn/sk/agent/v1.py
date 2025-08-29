from typing import Any

from semantic_kernel.agents import ChatCompletionAgent


# SRC: https://github.com/microsoft/semantic-kernel/blob/python-1.35.2/python/samples/concepts/mcp/agent_with_http_mcp_plugin.py
class MsLearnMCPChatCompletionAgent(ChatCompletionAgent):
    def model_post_init(self, __context: Any) -> None:
        self.name = "DocsAgent"

        self.description = "Learn Docs Plugin"

        self.instructions = "Answer questions about the Microsoft's Semantic Kernel SDK."

        return super().model_post_init(__context)
