from dataclasses import dataclass, field
from logging import Logger

from semantic_kernel.connectors.mcp import MCPStreamableHttpPlugin
from semantic_kernel.utils.feature_stage_decorator import experimental

from semantic_kernel_sampler.sk.plugins.protocol import PluginProtocol


@dataclass
@experimental
class StreamableHttpMCPPlugin(MCPStreamableHttpPlugin, PluginProtocol):

    name: str = field()

    description: str = field()

    url: str = field()
