import { baseURI } from "../../config/active.ts";
import { NewPostSchema, type NewPost } from "../schemas/new.ts";
import { PostSchema } from "../schemas/full.ts";

async function createPostAsync({ title }: NewPost): Promise<object> {
  const postData = { title, views: 0 };

  const response = await fetch(`${baseURI}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
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

  const content = [{ type: "text" as const, text: JSON.stringify(oPost) }];

  return { content };
}

createPostAsync.config = {
  title: "Create a new post",
  description: "Create a new post with the provided data",
  inputSchema: NewPostSchema.shape,
  annotations: {
    readOnlyHint: false,
    idempotentHint: false,
    openWorldHint: false,
  },
};

export { createPostAsync };
