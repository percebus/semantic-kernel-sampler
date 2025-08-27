from typing import Any

from semantic_kernel.agents import ChatCompletionAgent


class TriageChatCompletionAgent(ChatCompletionAgent):
    def model_post_init(self, __context: Any) -> None:
        self.name = "TriageAgent"
        self.description = "A customer support agent that triages issues."
        self.instructions = "Handle customer requests."

        return super().model_post_init(__context)
