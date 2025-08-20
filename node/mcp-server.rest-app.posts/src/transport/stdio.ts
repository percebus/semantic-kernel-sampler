import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { mcpServer } from "../mcp/server.ts";

const stdioServerTransport = new StdioServerTransport();

async function runAsync() {
  // Start receiving messages on stdin and sending messages on stdout
  await mcpServer.connect(stdioServerTransport);
  console.log("MCP server is running...");
}

export { runAsync };
