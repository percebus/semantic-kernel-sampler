from dataclasses import dataclass, field
from pathlib import Path

from semantic_kernel_sampler.sk.plugins.mcp.base.stdio import StdioMCPPlugin


@dataclass
class BlogPostsStdioMCPPlugin(StdioMCPPlugin):
    def create_command_args(self) -> list[str]:
        current_working_directory = Path.cwd()
        self.logger.debug("Current working directory: %s", current_working_directory)
        projectPath = Path(current_working_directory).resolve()  # Resolve to handle symlinks and relative paths
        mcpPath: Path = projectPath.parent.parent.joinpath("node", "mcp-server.rest-app.posts")

        self.logger.info("Using MCP server path: %s", mcpPath)
        return [
            "start",  # stdio
            "--prefix",
            f"{mcpPath}",
        ]

    name: str = field(default="Demo Server")

    description: str = field(default="Demo Server for TypeScript SDK")

    command: str = field(default="npm")

    def __post_init__(self):
        self.args = self.create_command_args()
