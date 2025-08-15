from dataclasses import dataclass
from textwrap import dedent
from typing import ClassVar

from semantic_kernel_sampler.agents.base import SemanticChatAgentBase
from semantic_kernel_sampler.agents.math.plugin import MathPlugin
from semantic_kernel_sampler.plugins.protocol import PluginProtocol


@dataclass
class MathAgent(SemanticChatAgentBase):
    plugins: ClassVar[list[PluginProtocol]] = [MathPlugin()]

    def __post_init__(self):
        # TODO
        # self.agent_card__public = public_agent_card
        # self.agent_card__authenticated = authenticated_agent_card

        # TODO read from file
        self.system_message = dedent("""
            You are a helpful Mathematician assistant.
            You will only use the registered plugin(s).
            If it's not in the plugins, say 'I cannot help with that.'""")

        super().__post_init__()
