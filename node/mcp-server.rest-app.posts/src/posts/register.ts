import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";

import {
  getPostResourceByIdAsync,
  postResourceMetadata,
  postResourceTemplate,
} from "./resources/post.ts";

import { getPostByIdAsync } from "./tools/get.ts";
import { findPostsAsync } from "./tools/find.ts";
import { createPostAsync } from "./tools/create.ts";
import { putPostAsync } from "./tools/put.ts";
import { deletePostByIdAsync } from "./tools/delete.ts";
import { createPromptPayloadCreatePost } from "./prompts/create.ts";
import { createPromptPayloadViewsPerPost } from "./prompts/views.ts";

function registerAll(mcpServer: McpServer): McpServer {
  mcpServer.registerResource(
    "post",
    postResourceTemplate,
    postResourceMetadata,
    getPostResourceByIdAsync,
  );

  mcpServer.registerTool("posts_find", findPostsAsync.config, findPostsAsync);

  mcpServer.registerTool(
    "posts_get",
    getPostByIdAsync.config,
    getPostByIdAsync,
  );

  mcpServer.registerTool(
    "posts_create",
    createPostAsync.config,
    createPostAsync,
  );

  mcpServer.registerTool("posts_update", putPostAsync.config, putPostAsync);

  mcpServer.registerTool(
    "posts_delete",
    deletePostByIdAsync.config,
    deletePostByIdAsync,
  );

  mcpServer.registerPrompt(
    "posts_create",
    createPromptPayloadCreatePost.config,
    createPromptPayloadCreatePost,
  );

  mcpServer.registerPrompt(
    "post_how_many_views",
    createPromptPayloadViewsPerPost.config,
    createPromptPayloadViewsPerPost,
  );

  return mcpServer;
}

export { registerAll };
