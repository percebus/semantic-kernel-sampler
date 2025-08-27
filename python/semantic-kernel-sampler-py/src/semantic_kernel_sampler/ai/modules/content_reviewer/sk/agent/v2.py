from typing import Any

from semantic_kernel.agents import ChatCompletionAgent


class ContentReviewerChatCompletionAgent(ChatCompletionAgent):
    def model_post_init(self, __context: Any) -> None:
        self.name = "Reviewer"
        self.description = "A content reviewer."
        self.instructions = "You are an excellent content reviewer. You review the content and provide feedback to the writer."
        return super().model_post_init(__context)
