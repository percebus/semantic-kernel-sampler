from dataclasses import dataclass, field

from semantic_kernel.connectors.mcp import MCPStreamableHttpPlugin


@dataclass
class BlogPostsStreamableHttpMCPPlugin(MCPStreamableHttpPlugin):

    name: str = field(default="BlogPosts stdio MCP Client")

    description: str = field(default="stdio MCP Client for rest-app Blog Posts")

    # FIXME pass from config
    url: str = field(default="http://localhost:4001/mcp")
