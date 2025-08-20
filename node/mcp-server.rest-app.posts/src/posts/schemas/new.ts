import { z } from "zod";

const NewPostSchema = z.object({ title: z.string() });

// Type inference from the schemas
type NewPost = z.infer<typeof NewPostSchema>;

export { NewPostSchema };
export type { NewPost };
