import { z } from "zod";

const createPromptPayloadCreatePost = ({ title }: { title: string }) => ({
  messages: [
    {
      role: "user",
      content: {
        type: "text",
        text: `Create a new post with the title: "${title}"`,
      },
    },
  ],
});

createPromptPayloadCreatePost.config = {
  title: "Create a new post with the title: {title}",
  argSchema: { title: z.string() },
};

export { createPromptPayloadCreatePost };
