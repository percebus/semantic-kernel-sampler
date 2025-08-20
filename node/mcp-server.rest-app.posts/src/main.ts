import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";

import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

import { registerAll as registerPostsModule } from "./posts/register.ts";

// Create an MCP server
const oMcpServer = new McpServer({ name: "rest-app-posts", version: "1.0.0" });

registerPostsModule(oMcpServer);

// Start receiving messages on stdin and sending messages on stdout
const stdioServerTransport = new StdioServerTransport();
await oMcpServer.connect(stdioServerTransport);
