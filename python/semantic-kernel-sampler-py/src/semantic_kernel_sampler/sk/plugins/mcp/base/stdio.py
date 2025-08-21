from dataclasses import dataclass, field
from logging import Logger

from semantic_kernel.connectors.mcp import MCPStdioPlugin
from semantic_kernel.utils.feature_stage_decorator import experimental

from semantic_kernel_sampler.sk.plugins.protocol import PluginProtocol


@dataclass
@experimental
class StdIOMCPPlugin(MCPStdioPlugin, PluginProtocol):
    logger: Logger = field()

    name: str = field()

    description: str = field()

    command: str = field()

    args: list[str] = field(default_factory=list)  # pyright: ignore[reportUnknownVariableType]
