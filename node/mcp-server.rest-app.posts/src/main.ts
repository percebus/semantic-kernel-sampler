import {
  McpServer,
  // ResourceTemplate, // TODO
} from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

import type { Post } from "./schema/post.ts";
import { PostSchema } from "./schema/post.ts";


// TODO pass from .environment
// TODO convert to ResourceTemplate
const baseURI = "http://localhost:3000/posts"

// Create an MCP server
const server = new McpServer({
  name: "rest-app-posts",
  version: "1.0.0",
});

server.registerTool(
  "find",
  {
    title: "Find posts",
    description: "Find posts by a certain criteria",
    inputSchema: PostSchema.shape,
  },
  async (postSchema) => {
    const responsePromise = await fetch(`${baseURI}`);
    const rawPosts = await responsePromise.json();

    // Validate and parse the posts using the schema
    const posts = rawPosts.map((post: any) =>
      PostSchema.parse(post));

    const content = posts
      // TODO .filter
      .map((post: Post) => ({
        type: "text" as const,
        text: JSON.stringify(post),
      }));

    return {
      content,
    };
  },
);

server.registerTool(
  "get",
  {
    title: "Get post by ID",
    description: "Retrieve a single post by its ID",
    inputSchema: { id: z.string() }, // TODO PostSchema.id
  },
  async ({ id }) => {
    const responsePromise = await fetch(`${baseURI}/${id}`);
    const rawPost = await responsePromise.json();

    // Validate and parse the posts using the schema
    const post = PostSchema.parse(rawPost);

    const content = [{
      type: "text" as const,
      text: JSON.stringify(post),
    }];

    return {
      content,
    };
  },
);

server.registerTool(
  "create",
  {
    title: "Create a new post",
    description: "Create a new post with the provided data",
    inputSchema: {
      title: z.string().describe("The title of the post"),
      views: z.number().describe("The number of views for the post"),
      id: z.string().optional().describe("Optional ID for the post (will be auto-generated if not provided)")
    },
  },
  async ({ title, views, id }: { title: string; views: number; id?: string | undefined }) => {
    const postData = {
      ...(id && { id }),
      title,
      views,
    };

    const response = await fetch(`${baseURI}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(postData),
    });

    if (!response.ok) {
      throw new Error(`Failed to create post: ${response.status} ${response.statusText}`);
    }

    const createdPost = await response.json();

    // Validate and parse the created post using the schema
    const post = PostSchema.parse(createdPost);

    const content = [{
      type: "text" as const,
      text: JSON.stringify(post),
    }];

    return {
      content,
    };
  },
);

// TODO ADD
// 1. PUT
// 2. DELETE

// Start receiving messages on stdin and sending messages on stdout
const transport = new StdioServerTransport();
await server.connect(transport);
