import {
  McpServer
} from '@modelcontextprotocol/sdk/server/mcp.js'

import { getPostResourceByIdAsync, postResourceMetadata, postResourceTemplate } from './resources/post.ts'

import { getPostByIdAsync } from './tools/get.ts'
import { findPostsAsync } from './tools/find.ts'
import { createPostAsync } from './tools/create.ts'
import { putPostAsync } from './tools/put.ts'
import { deletePostByIdAsync } from './tools/delete.ts'

function registerAll (mcpServer: McpServer) {
  // Create an MCP server
  const oMcpServer = new McpServer({
    name: 'rest-app-posts',
    version: '1.0.0'
  })

  oMcpServer.registerResource(
    'post',
    postResourceTemplate,
    postResourceMetadata,
    getPostResourceByIdAsync
  )

  oMcpServer.registerTool(
    'posts_find',
    findPostsAsync.metadata,
    findPostsAsync
  )

  oMcpServer.registerTool(
    'posts_get',
    getPostByIdAsync.metadata,
    getPostByIdAsync
  )

  oMcpServer.registerTool(
    'posts_create',
    createPostAsync.metadata,
    createPostAsync
  )

  oMcpServer.registerTool(
    'posts_update',
    putPostAsync.metadata,
    putPostAsync
  )

  oMcpServer.registerTool(
    'posts_delete',
    deletePostByIdAsync.metadata,
    deletePostByIdAsync
  )
}

export {
  registerAll
}
