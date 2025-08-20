import { baseURI } from '../config.ts'
import { PostSchema, type Post } from '../schema.ts'

async function putPostAsync ({ id, title, views }: Post): Promise<object> {
  const postData = {
    title,
    views
  }

  const response = await fetch(`${baseURI}/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(postData)
  })

  if (!response.ok) {
    throw new Error(
        `Failed to update post: ${response.status} ${response.statusText}`
    )
  }

  const updatedPost = await response.json()

  // Validate and parse the updated post using the schema
  const oPost = PostSchema.parse(updatedPost)

  const content = [
    {
      type: 'text' as const,
      text: JSON.stringify(oPost)
    }
  ]

  return {
    content
  }
}

putPostAsync.metadata = {
  title: 'Update post',
  description: 'Update an existing post with new data',
  inputSchema: PostSchema.shape,
  annotations: {
    readOnlyHint: false,
    idempotentHint: true,
    // destructiveHint: true, // TODO?
    openWorldHint: false
  }
}

export {
  putPostAsync
}
