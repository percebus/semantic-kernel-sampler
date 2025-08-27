from typing import Any

from semantic_kernel.agents import ChatCompletionAgent


class ContentWriterChatCompletionAgent(ChatCompletionAgent):
    def model_post_init(self, __context: Any) -> None:
        self.name = "Writer"
        self.description = "A content writer."
        self.instructions = "You are an excellent content writer. You create new content and edit contents based on the feedback."
        return super().model_post_init(__context)
