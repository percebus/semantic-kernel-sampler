import {
  McpServer,
  ResourceTemplate,
} from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

import type { Post, NewPost } from "./schema/post.ts";
import {
  PostSchema,
  NewPostSchema,
  PostIdentifierSchema,
} from "./schema/post.ts";

// TODO pass from .environment
// TODO convert to ResourceTemplate
const baseURI = "http://localhost:3000/posts";

// Create an MCP server
const oMcpServer = new McpServer({
  name: "rest-app-posts",
  version: "1.0.0",
});

const postResourceTemplate = new ResourceTemplate("posts://{id}", { list: undefined})
oMcpServer.registerResource(
  "post",
  postResourceTemplate,
  {
    title: "Post",
    description: "A single blog post",
  },
  async (uri , {id}) => {
    const responsePromise = await fetch(`${baseURI}/${id}`);
    const rawPost = await responsePromise.json();

    // Validate and parse the posts using the schema
    const post = PostSchema.parse(rawPost);
    const content = {
      mime: "application/json",
      text: JSON.stringify(post),
      uri: uri.href
    }
    return {
      contents: [
        content
      ]
    };
  }
);

oMcpServer.registerTool(
  "posts_find",
  {
    title: "Find posts",
    description: "Find posts by a certain criteria",
    inputSchema: PostSchema.shape,
    annotations: {
      readOnlyHint: true,
      openWorldHint: false,
    }
  },
  async (postSchema) => {
    const responsePromise = await fetch(`${baseURI}`);
    const rawPosts = await responsePromise.json();

    // Validate and parse the posts using the schema
    const posts = rawPosts.map((post: any) => PostSchema.parse(post));

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

oMcpServer.registerTool(
  "posts_get",
  {
    title: "Get post by ID",
    description: "Retrieve a single post by its ID",
    inputSchema: PostIdentifierSchema.shape,
    annotations: {
      readOnlyHint: true,
      openWorldHint: false,
    }
  },
  async ({ id }) => {
    const responsePromise = await fetch(`${baseURI}/${id}`);
    const rawPost = await responsePromise.json();

    // Validate and parse the posts using the schema
    const post = PostSchema.parse(rawPost);

    const content = [
      {
        type: "text" as const,
        text: JSON.stringify(post),
      },
    ];

    return {
      content,
    };
  },
);

oMcpServer.registerTool(
  "posts_create",
  {
    title: "Create a new post",
    description: "Create a new post with the provided data",
    inputSchema: NewPostSchema.shape,
    annotations: {
      readOnlyHint: false,
      idempotentHint: false,
      openWorldHint: false,
    }
  },
  async ({ title }: NewPost) => {
    const postData = {
      title,
      views: 0,
    };

    const response = await fetch(`${baseURI}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(postData),
    });

    if (!response.ok) {
      throw new Error(
        `Failed to create post: ${response.status} ${response.statusText}`,
      );
    }

    const createdPost = await response.json();

    // Validate and parse the created post using the schema
    const oPost = PostSchema.parse(createdPost);

    const content = [
      {
        type: "text" as const,
        text: JSON.stringify(oPost),
      },
    ];

    return {
      content,
    };
  },
);

oMcpServer.registerTool(
  "posts_update",
  {
    title: "Update post",
    description: "Update an existing post with new data",
    inputSchema: PostSchema.shape,
    annotations: {
      readOnlyHint: false,
      idempotentHint: true,
      // destructiveHint: true, // TODO?
      openWorldHint: false,
    }
  },
  async ({ id, title, views }: Post) => {
    const postData = {
      title,
      views,
    };

    const response = await fetch(`${baseURI}/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(postData),
    });

    if (!response.ok) {
      throw new Error(
        `Failed to update post: ${response.status} ${response.statusText}`,
      );
    }

    const updatedPost = await response.json();

    // Validate and parse the updated post using the schema
    const oPost = PostSchema.parse(updatedPost);

    const content = [
      {
        type: "text" as const,
        text: JSON.stringify(oPost),
      },
    ];

    return {
      content,
    };
  },
);

oMcpServer.registerTool(
  "posts_delete",
  {
    title: "Delete post by ID",
    description: "Delete a post by its ID",
    inputSchema: PostIdentifierSchema.shape,
    annotations: {
      readOnlyHint: false,
      idempotentHint: true,
      destructiveHint: true,
      openWorldHint: false,
    }
  },
  async ({ id }) => {
    const response = await fetch(`${baseURI}/${id}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error(
        `Failed to delete post: ${response.status} ${response.statusText}`,
      );
    }

    const content = [
      {
        type: "text" as const,
        text: `Post with ID ${id} has been successfully deleted`,
      },
    ];

    return {
      content,
    };
  },
);

// Start receiving messages on stdin and sending messages on stdout
const stdioServerTransport = new StdioServerTransport();
await oMcpServer.connect(stdioServerTransport);
