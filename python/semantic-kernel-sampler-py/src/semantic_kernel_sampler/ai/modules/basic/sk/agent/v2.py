from typing import Any

from semantic_kernel.agents import ChatCompletionAgent  # pylint: disable=no-name-in-module


class BasicChatCompletionAgent(ChatCompletionAgent):
    def model_post_init(self, __context: Any) -> None:
        self.name = "Assistant"
        self.description = "An assistant that answers questions"
        self.instructions = "Answer the user's questions."
        return super().model_post_init(__context)
