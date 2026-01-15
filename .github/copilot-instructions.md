# Semantic Kernel Sampler

Semantic Kernel Sampler is a multi-language monorepo showcasing semantic kernel implementations across Node.js, Python, .NET, and Java. It includes REST APIs, MCP (Model Context Protocol) servers, AI evaluation tools, and comprehensive integration examples.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Quick Start - Repository Setup

- Bootstrap the repository:
  - `npm run setup` -- installs global dependencies (1 second). NEVER CANCEL.
  - `npm install` -- installs all Node.js dependencies (25 seconds). NEVER CANCEL. Set timeout to 60+ seconds. Expect Node.js version warnings for @modelcontextprotocol/inspector.
  - `bower install` -- clones external repositories (6 seconds). NEVER CANCEL. Set timeout to 60+ seconds.

### Language-Specific Builds

- **Node.js projects**: `npm test` -- runs linting and tests for all workspaces (7 seconds). NEVER CANCEL. Set timeout to 60+ seconds.
- **.NET projects**:
  - `cd dotnet && dotnet restore` -- restores packages (16 seconds). NEVER CANCEL. Set timeout to 60+ seconds.
  - `cd dotnet && dotnet build --no-restore --configuration Release` -- builds project (8 seconds). NEVER CANCEL. Set timeout to 60+ seconds.
- **Java projects**: `cd java && mvn --batch-mode --update-snapshots verify` -- builds and tests (18 seconds). NEVER CANCEL. Set timeout to 60+ seconds.
- **Python projects**: Python installs may timeout due to network limitations in CI environments. Use `uv` if available, or document timeouts as expected.

### Running Applications

- **REST API**:
  - `cd node/rest-app && npm start` -- starts JSON server on port 3000 (5-10 seconds)
  - Test with: `curl http://localhost:3000/posts`
- **MCP Inspector**:
  - `npm run start:mcp:inspector` -- starts MCP inspector on port 6274 with web interface
  - Opens browser automatically with authentication token
- **.NET WebApp**: Available in `dotnet/WebApp/bin/Release/net8.0/` after build
- **Docker Compose**:
  - First setup: `cd node/mcp-server.rest-app.posts/src/config && cp docker.windows.ts active.ts`
  - Then: `docker compose up --build` -- builds and starts all services

## Validation

### Manual Testing Requirements

- ALWAYS test REST API functionality by starting the server and making actual HTTP requests: `curl http://localhost:3000/posts`
- ALWAYS test MCP inspector by starting it and verifying the web interface loads at the provided URL
- For any Node.js changes: Run `npm test` to ensure all workspace tests pass
- For Docker changes: Test `docker compose build` completes successfully
- Integration tests (`npm run validate`) require running services - failures are expected when services aren't running

### Pre-commit Validation

- ALWAYS run `npm run lint` before committing (2 seconds) - uses Prettier for code formatting
- ALWAYS run `npm test` to ensure no regressions (7 seconds)
- For .NET changes: Run `dotnet build` in dotnet/ directory
- For Java changes: Run `mvn verify` in java/ directory

## Common Issues and Solutions

### Missing Configuration

- If REST validation tests fail with "Cannot find module '../../config/environments/environment'":
  - Run: `cd __tests__/config/environments && cp local.js environment.js`

### Node.js Version Warnings

- @modelcontextprotocol/inspector requires Node.js >=22.7.5 but still works with 20.x
- These warnings are expected and non-blocking

### Docker Compose Setup

- Must configure MCP server before running docker compose: `cd node/mcp-server.rest-app.posts/src/config && cp docker.windows.ts active.ts`

## Architecture Overview

### Project Structure

```
├── node/                     # Node.js projects (workspaces)
│   ├── rest-app/            # JSON server REST API
│   ├── mcp-server.examples.quick-start/  # Basic MCP server
│   └── mcp-server.rest-app.posts/        # MCP server for REST API
├── python/                  # Python projects
│   ├── semantic-kernel-sampler-py/       # Main Python implementation
│   └── ai-evaluator-py/                  # AI evaluation tools
├── dotnet/                  # .NET projects
│   └── WebApp/              # ASP.NET Core web application
├── java/                    # Java projects
│   └── src/                 # Maven-based web application
├── repositories/            # External repositories (via bower)
│   ├── a2a-samples/         # A2A samples
│   └── semantic-kernel/     # Microsoft Semantic Kernel
├── submodules
│   └── a2a-inspector/       # A2A inspection tool
└── __tests__/               # Integration tests
    └── config/environments/ # Test environment configurations
```

### Key Services and Ports

- REST API (json-server): http://localhost:3000
- MCP Inspector: http://localhost:6274
- MCP Server Quick Start: http://localhost:4001
- MCP Server Posts: http://localhost:4002
- Python Semantic App: http://localhost:8082
- .NET Semantic App: http://localhost:8083
- A2A Inspector: http://localhost:5001

### External Dependencies

- bower: For managing external git repositories
- @modelcontextprotocol/inspector: Web-based MCP debugging tool
- json-server: Provides REST API endpoints
- Docker & Docker Compose: For full-stack orchestration

## Development Workflow

1. **Initial Setup**: Run bootstrap commands (npm setup, npm install, bower installn)
2. **Language-specific Build**: Build the component you're working on
3. **Make Changes**: Edit code with your IDE
4. **Local Testing**: Start relevant services and test manually
5. **Validation**: Run linting, building, and testing commands
6. **Integration**: Test with docker compose if making cross-service changes

Always validate your changes by running the actual applications and exercising user scenarios, not just running automated tests.
