import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";

import { registerAll as registerPostsModule } from "../posts/register.ts";

function createMcpServer() {
  // Create an MCP server
  const oMcpServer = new McpServer({
    name: "rest-app.posts",
    version: "1.0.0",
  });

  registerPostsModule(oMcpServer);
  return oMcpServer;
}

export { createMcpServer };
