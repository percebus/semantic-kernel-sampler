from semantic_kernel.connectors.mcp import MCPStdioPlugin
from semantic_kernel.utils.feature_stage_decorator import experimental


@experimental
def createMCPStdioPlugin() -> MCPStdioPlugin:
    # SRC: https://github.com/microsoft/semantic-kernel/blob/main/python/samples/concepts/mcp/mcp_as_plugin.py
    return MCPStdioPlugin(
        name="Demo Server",
        description="modelcontextprotocol/typescript-sdk example",
        command="npm",
        args=["start", "--prefix", "../../node/mcp-server.examples.quick-start"],
    )
