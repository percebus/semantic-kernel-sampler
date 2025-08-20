import { baseURI } from "../config.ts";
import { PostIdentifierSchema } from "../schemas/id.ts";
import { PostSchema } from "../schemas/full.ts";

async function getPostByIdAsync({ id }: { id: string }): Promise<object> {
  const response: Response = await fetch(`${baseURI}/${id}`);
  const rawPost = await response.json();

  // Validate and parse the posts using the schema
  const post = PostSchema.parse(rawPost);

  const content = [{ type: "text" as const, text: JSON.stringify(post) }];

  return { content };
}

getPostByIdAsync.config = {
  title: "Get post by ID",
  description: "Retrieve a single post by its ID",
  inputSchema: PostIdentifierSchema.shape,
  annotations: { readOnlyHint: true, openWorldHint: false },
};

export { getPostByIdAsync };
