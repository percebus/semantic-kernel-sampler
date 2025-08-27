from semantic_kernel.connectors.mcp import MCPStreamableHttpPlugin


def createMCPStreamableHttpPlugin() -> MCPStreamableHttpPlugin:
    # SRC: https://github.com/microsoft/semantic-kernel/blob/python-1.35.2/python/samples/concepts/mcp/agent_with_http_mcp_plugin.py
    return MCPStreamableHttpPlugin(
        name="LearnSite",
        description="Learn Docs Plugin",
        url="https://learn.microsoft.com/api/mcp",
    )
