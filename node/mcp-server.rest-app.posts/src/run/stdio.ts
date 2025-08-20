import { runAsync } from "../transport/stdio.ts";

runAsync().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
