import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { createMcpServer } from "../mcp/server.ts";

const oStdioServerTransport = new StdioServerTransport();

async function runAsync() {
  // Start receiving messages on stdin and sending messages on stdout
  const singleMcpServer = createMcpServer();
  await singleMcpServer.connect(oStdioServerTransport);
  console.log("MCP server is running...");
}

export { runAsync };
