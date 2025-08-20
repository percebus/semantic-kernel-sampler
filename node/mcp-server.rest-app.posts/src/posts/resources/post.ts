import {
  ResourceTemplate
} from '@modelcontextprotocol/sdk/server/mcp.js'

import type { ResourceMetadata } from '@modelcontextprotocol/sdk/server/mcp.js'

import { baseURI } from '../config.ts'
import { PostSchema } from '../schema.ts'

const postResourceTemplate = new ResourceTemplate('posts://{id}', { list: undefined })

const postResourceMetadata: ResourceMetadata = {
  title: 'Post',
  description: 'A single blog post',
  schema: PostSchema.shape
}

async function getPostResourceByIdAsync (uri, { id }: { id: string }): Promise<object> {
  const responsePromise: Promise<Response> = fetch(`${baseURI}/${id}`)
  const rawPost = await (await responsePromise).json()

  // Validate and parse the posts using the schema
  const post = PostSchema.parse(rawPost)
  const content = {
    mime: 'application/json',
    text: JSON.stringify(post),
    uri: uri.href
  }
  return {
    contents: [
      content
    ]
  }
}

export {
  postResourceTemplate,
  getPostResourceByIdAsync,
  postResourceMetadata
}
