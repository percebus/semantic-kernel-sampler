import { baseURI } from "../config.ts";
import { PostSchema } from "../schema.ts";
import type { Post } from "../schema.ts";

async function findPostsAsync(/* postSchema */): Promise<object> {
  const responsePromise = await fetch(`${baseURI}`);
  const rawPosts = await responsePromise.json();

  // Validate and parse the posts using the schema
  const posts = rawPosts.map((post: unknown) => PostSchema.parse(post));

  const content = posts
    // TODO .filter
    .map((post: Post) => ({
      type: "text" as const,
      text: JSON.stringify(post),
    }));

  return {
    content,
  };
}

findPostsAsync.metadata = {
  title: "Find posts",
  description: "Find posts by a certain criteria",
  inputSchema: PostSchema.shape,
  annotations: {
    readOnlyHint: true,
    openWorldHint: false,
  },
};

export { findPostsAsync };
