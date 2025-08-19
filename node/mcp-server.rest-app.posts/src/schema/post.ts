import { z } from "zod";

const NewPostSchema = z.object({
  title: z.string(),
});


const PostIdentifierSchema = z.object({
  id: z.string(),
});

// Define the Post schema by extending NewPostSchema with an ID
const PostSchema = NewPostSchema
  .extend(PostIdentifierSchema.shape)
  .extend({
    views: z.number(),
  });


// Type inference from the schemas
type NewPost = z.infer<typeof NewPostSchema>;
type PostIdentifier = z.infer<typeof PostIdentifierSchema>;
type Post = z.infer<typeof PostSchema>;

export { NewPostSchema, PostIdentifierSchema, PostSchema };
export type { NewPost, PostIdentifier, Post };
