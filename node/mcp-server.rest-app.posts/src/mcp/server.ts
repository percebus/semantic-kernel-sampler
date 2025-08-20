import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";

import { registerAll as registerPostsModule } from "../posts/register.ts";

// Create an MCP server
const mcpServer = new McpServer({ name: "rest-app.posts", version: "1.0.0" });

registerPostsModule(mcpServer);

export { mcpServer };
``;
