import { app } from "../transport/http/streamable/stateless.ts";

// Start the server
const PORT = 3000;
app.listen(PORT, (error) => {
  if (error) {
    console.error("Failed to start server:", error);
    process.exit(1);
  }
  console.log(`MCP Stateless Streamable HTTP Server listening on port ${PORT}`);
});
