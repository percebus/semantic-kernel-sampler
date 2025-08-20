import { z } from "zod";

const PostIdentifierSchema = z.object({ id: z.string() });

// Type inference from the schemas
type PostIdentifier = z.infer<typeof PostIdentifierSchema>;

export { PostIdentifierSchema };
export type { PostIdentifier };
