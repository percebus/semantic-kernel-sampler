import { z } from "zod";

const createPromptPayloadViewsPerPost = ({ id }: { id: string }) => ({
  messages: [
    {
      role: "user",
      content: {
        type: "text",
        text: `How many views does the post with id "${id}" have?`,
      },
    },
  ],
});

createPromptPayloadViewsPerPost.config = {
  title: "How many views does the post with id: {id} have?",
  argsSchema: { id: z.string() },
};

export { createPromptPayloadViewsPerPost };
