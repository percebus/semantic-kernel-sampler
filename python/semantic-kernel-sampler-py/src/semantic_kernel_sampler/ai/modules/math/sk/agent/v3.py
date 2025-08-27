from typing import Any

from semantic_kernel.agents import ChatCompletionAgent


class MathChatCompletionAgent(ChatCompletionAgent):
    def model_post_init(self, __context: Any) -> None:
        self.name = "MathTeacher"
        self.description = "A 3rd grade math teacher that answers questions about basic operations"
        self.instructions = " ".join(
            [
                "You are a helpful Mathematician assistant.",
                "You will only use the registered plugin(s).",
                "If it's not in the plugins, say 'I cannot help with that.'",
            ]
        )

        return super().model_post_init(__context)
