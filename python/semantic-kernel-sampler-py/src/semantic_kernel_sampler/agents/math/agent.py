from dataclasses import dataclass, field

from semantic_kernel_sampler.agents.base import ChatSemanticAgentBase
from semantic_kernel_sampler.agents.math.plugin import MathPlugin
from semantic_kernel_sampler.plugins.protocol import PluginProtocol


@dataclass
class MathAgent(ChatSemanticAgentBase):
    plugins: list[PluginProtocol] = field(default_factory=lambda: [MathPlugin()])  # type: ignore # FIXME
