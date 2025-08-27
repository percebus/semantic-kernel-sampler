from typing import Any

from semantic_kernel.agents import ChatCompletionAgent


class LightChatCompletionAgent(ChatCompletionAgent):
    def model_post_init(self, __context: Any) -> None:
        self.name = "LigthSwitchAgent"
        self.description = "A light switch operator that turns on/off the light"
        self.instructions = " ".join(
            [
                "You are a helpful Light Switch assistant.",
                "You will only use the registered plugin(s).",
                "If it's not in the plugins, say 'I cannot help with that.'",
            ]
        )

        return super().model_post_init(__context)
