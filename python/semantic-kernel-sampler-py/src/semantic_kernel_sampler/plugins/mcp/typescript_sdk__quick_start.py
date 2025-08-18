from dataclasses import dataclass, field

from semantic_kernel_sampler.plugins.mcp.base.stdio import MyMCPStdioPlugin


@dataclass
class DemoServerMCPStdioPlugin(MyMCPStdioPlugin):
    name: str = field(default="Demo Server")

    description: str = field(default="Demo Server for TypeScript SDK")

    command: str = field(default="npm")

    args: list[str] = field(default_factory=lambda: ["start", "--prefix", "../../node/modelcontextprotocol-typescript-sdk-example"])
