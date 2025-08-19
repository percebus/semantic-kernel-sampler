import { z } from "zod";

// Define the Post schema based on the JSON structure
const PostSchema = z.object({
  id: z.string(),
  title: z.string(),
  views: z.number(),
});


// Type inference from the schema
type Post = z.infer<typeof PostSchema>;

export { PostSchema };
export type { Post };
