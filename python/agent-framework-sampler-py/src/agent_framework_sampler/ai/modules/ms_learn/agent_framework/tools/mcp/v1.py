from dataclasses import dataclass, field

from agent_framework import MCPStreamableHTTPTool

from agent_framework_sampler.config.configuration import Configuration


@dataclass
class MSLearnMCPStreamableHttpTool(MCPStreamableHTTPTool):
    configuration: Configuration = field()

    description: str = field(default="MCP tool description")

    # TODO? move to Settings?
    url: str = field(
        default="https://learn.microsoft.com/api/mcp"
        # default="https://apim-rnd-eastus2-apim.azure-api.net/mcp-mslearn/api/mcp"
    )

    # TODO add headers
    def __post_init__(self) -> None:
        return super().__init__(
            name=self.__class__.__name__,
            description=self.description,
            url=self.url,
        )
