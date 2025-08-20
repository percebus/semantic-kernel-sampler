import { baseURI } from '../config.ts'
import { PostIdentifierSchema } from '../schema.ts'

async function deletePostByIdAsync ({ id }: { id: string }): Promise<object> {
  const response = await fetch(`${baseURI}/${id}`, {
    method: 'DELETE'
  })

  if (!response.ok) {
    throw new Error(
        `Failed to delete post: ${response.status} ${response.statusText}`
    )
  }

  const content = [
    {
      type: 'text' as const,
      text: `Post with ID ${id} has been successfully deleted`
    }
  ]

  return {
    content
  }
}

deletePostByIdAsync.metadata = {
  title: 'Delete post by ID',
  description: 'Delete a post by its ID',
  inputSchema: PostIdentifierSchema.shape,
  annotations: {
    readOnlyHint: false,
    idempotentHint: true,
    destructiveHint: true,
    openWorldHint: false
  }
}

export {
  deletePostByIdAsync
}
