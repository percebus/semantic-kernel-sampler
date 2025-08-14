from dataclasses import dataclass, field

from semantic_kernel_sampler.agents.base import ChatSemanticAgentBase
from semantic_kernel_sampler.agents.light.plugin import LightPlugin
from semantic_kernel_sampler.plugins.protocol import PluginProtocol


@dataclass
class LightAgent(ChatSemanticAgentBase):
    plugins: list[PluginProtocol] = field(default_factory=lambda: [LightPlugin()])  # type: ignore # FIXME
