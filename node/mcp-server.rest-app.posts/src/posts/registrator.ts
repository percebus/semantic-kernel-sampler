import {
  McpServer
} from '@modelcontextprotocol/sdk/server/mcp.js'

import { getPostResourceByIdAsync, postResourceMetadata, postResourceTemplate } from './resources/post.ts'

import { getPostByIdAsync } from './tools/get.ts'
import { findPostsAsync } from './tools/find.ts'
import { createPostAsync } from './tools/create.ts'
import { putPostAsync } from './tools/put.ts'
import { deletePostByIdAsync } from './tools/delete.ts'

function registerAll (mcpServer: McpServer): McpServer {
  mcpServer.registerResource(
    'post',
    postResourceTemplate,
    postResourceMetadata,
    getPostResourceByIdAsync
  )

  mcpServer.registerTool(
    'posts_find',
    findPostsAsync.metadata,
    findPostsAsync
  )

  mcpServer.registerTool(
    'posts_get',
    getPostByIdAsync.metadata,
    getPostByIdAsync
  )

  mcpServer.registerTool(
    'posts_create',
    createPostAsync.metadata,
    createPostAsync
  )

  mcpServer.registerTool(
    'posts_update',
    putPostAsync.metadata,
    putPostAsync
  )

  mcpServer.registerTool(
    'posts_delete',
    deletePostByIdAsync.metadata,
    deletePostByIdAsync
  )

  return mcpServer
}

export {
  registerAll
}
