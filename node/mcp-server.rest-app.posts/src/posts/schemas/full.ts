import { NewPostSchema } from "./new.ts";
import { PostIdentifierSchema } from "./id.ts";

import { z } from "zod";

// Define the Post schema by extending NewPostSchema with an ID
const PostSchema = NewPostSchema.extend(PostIdentifierSchema.shape).extend({
  views: z.number(),
});

// Type inference from the schemas
type Post = z.infer<typeof PostSchema>;

export { PostSchema };
export type { Post };
