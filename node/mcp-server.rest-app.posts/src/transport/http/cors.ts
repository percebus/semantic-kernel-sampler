import cors from "cors";

const corsMiddleware = cors({
  origin: "*", // Configure appropriately for production, for example:
  // origin: ['https://your-remote-domain.com', 'https://your-other-remote-domain.com'],
  exposedHeaders: ["Mcp-Session-Id"],
  allowedHeaders: ["Content-Type", "mcp-session-id"],
});

export { corsMiddleware };
