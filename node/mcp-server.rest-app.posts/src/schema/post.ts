import { z } from "zod";

const NewPostSchema = z.object({
  title: z.string(),
  views: z.number(),
});


// Define the Post schema by extending NewPostSchema with an ID
const PostSchema = NewPostSchema.extend({
  id: z.string(),
});


// Type inference from the schemas
type NewPost = z.infer<typeof NewPostSchema>;
type Post = z.infer<typeof PostSchema>;

export { NewPostSchema, PostSchema };
export type { NewPost, Post };
