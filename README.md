# agent-framework-sampler

- [![[C]ontinuous [I]ntegration: PR](https://github.com/percebus/semantic-kernel-sampler/actions/workflows/branch.yml/badge.svg?event=pull_request)](https://github.com/percebus/semantic-kernel-sampler/actions/workflows/branch.yml)
- [![[C]ontinuous [I]ntegration @ main](https://github.com/percebus/semantic-kernel-sampler/actions/workflows/main.yml/badge.svg)](https://github.com/percebus/semantic-kernel-sampler/actions/workflows/main.yml)

~~Semantic-Kernel~~ `agent-framework` monorepo sampler

## Sub-Projecs/Repos

| Folder          | Project                                                                     | Type         | CI                                                                                                                                                                                                                                                                                           |
| --------------- | --------------------------------------------------------------------------- | ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `repositories/` | [`a2a-inspector`](./repositories/a2a-inspector)                             | A2A Client   | N/A                                                                                                                                                                                                                                                                                          |
| `repositories/` | [`@modelcontextprotocol/inspector`](./package.json)                         | MCP CLient   | N/A                                                                                                                                                                                                                                                                                          |
| `node/`         | `*`                                                                         | `node`       | [![node/*](https://github.com/percebus/semantic-kernel-sampler/actions/workflows/branch.node.yml/badge.svg)](https://github.com/percebus/semantic-kernel-sampler/actions/workflows/branch.node.yml)                                                                                          |
| `node/`         | [`rest-app`](./node/rest-app)                                               | RESTful API  | [![rest-app](https://github.com/percebus/semantic-kernel-sampler/actions/workflows/branch.node.rest-app.yml/badge.svg)](https://github.com/percebus/semantic-kernel-sampler/actions/workflows/branch.node.rest-app.yml)                                                                      |
| `node/`         | [`mcp-server.examples.quick-start`](./node/mcp-server.examples.quick-start) | MCP          | [![mcp-server.examples.quick-start](https://github.com/percebus/semantic-kernel-sampler/actions/workflows/branch.node.mcp-server.examples.quick-start.yml/badge.svg)](https://github.com/percebus/semantic-kernel-sampler/actions/workflows/branch.node.mcp-server.examples.quick-start.yml) |
| `node/`         | [`mcp-server.rest-app.posts`](./node/mcp-server.rest-app.posts)             | MCP          | [![mcp-server.rest-app.posts](https://github.com/percebus/semantic-kernel-sampler/actions/workflows/branch.node.mcp-server.rest-app.posts.yml/badge.svg)](https://github.com/percebus/semantic-kernel-sampler/actions/workflows/branch.node.mcp-server.rest-app.posts.yml)                   |
| `dotnet/`       | [`SemanticKernelSampler.DotNet`](./dotnet/SemanticKernelSampler.DotNet)     | Agent        | [![SemanticKernelSampler.DotNet](https://github.com/percebus/semantic-kernel-sampler/actions/workflows/branch.dotnet.SemanticKernelSampler.yml/badge.svg)](https://github.com/percebus/semantic-kernel-sampler/actions/workflows/branch.dotnet.SemanticKernelSampler.yml)                    |
| `dotnet/`       | [`AgentFrameworkSampler.DotNet`](./dotnet/AgentFrameworkSampler.DotNet)     | Agent        | [![AgentFrameworkSampler.DotNet](https://github.com/percebus/semantic-kernel-sampler/actions/workflows/branch.dotnet.AgentFrameworkSampler.yml/badge.svg)](https://github.com/percebus/semantic-kernel-sampler/actions/workflows/branch.dotnet.AgentFrameworkSampler.yml)                    |
| `java/`         | TODO                                                                        | Agent        | [![SemanticKernelSampler.Java](https://github.com/percebus/semantic-kernel-sampler/actions/workflows/branch.java.yml/badge.svg)](https://github.com/percebus/semantic-kernel-sampler/actions/workflows/branch.java.yml)                                                                      |
| `python/`       | [`semantic-kernel-sampler-py`](./python/semantic-kernel-sampler-py)         | Agent        | [![ai-evaluator-py](https://github.com/percebus/semantic-kernel-sampler/actions/workflows/branch.python.ai-evaluator-py.yml/badge.svg)](https://github.com/percebus/semantic-kernel-sampler/actions/workflows/branch.python.ai-evaluator-py.yml)                                             |
| `python/`       | [`agent-framework-sampler-py`](./python/agent-framework-sampler-py)         | Agent        | [![agent-framework-sampler-py](https://github.com/percebus/semantic-kernel-sampler/actions/workflows/branch.python.agent-framework-sampler-py.yml/badge.svg)](https://github.com/percebus/semantic-kernel-sampler/actions/workflows/branch.python.agent-framework-sampler-py.yml)            |
| `python/`       | [`ai-evaluator-py`](./python/ai-evaluator-py)                               | AI Evaluator | [![semantic-kernel-sampler-py](https://github.com/percebus/semantic-kernel-sampler/actions/workflows/branch.python.semantic-kernel-sampler-py.yml/badge.svg)](https://github.com/percebus/semantic-kernel-sampler/actions/workflows/branch.python.semantic-kernel-sampler-py.yml)            |

## R&D

### npm (global)

1. `$> npm run setup`
1. `$> npm install`

### External `repositories/`

1. `bower install`: [Installs `bower.json`](./bower.json) [under `repositories/`](./repositories/)

### @modelcontextprotcol/inspector

#### Start

1. `$> npm run start:mcp:inspector`

#### Usage

TODO

### a2a-inspector

#### Setup

```bash
# git clone a2a-instpector ./repositories
$> bower install

$> cd repositories/a2a-inspector
```

##### python

```bash
$> uv venv
```

- Windows: `$> source .venv/Scripts/activate`
- linux: `$> source .venv/bin/activate`

```bash
$> uv sync
```

Then see [Setup and Running the Application](https://github.com/a2aproject/a2a-inspector?tab=readme-ov-file#setup-and-running-the-application)

##### frontend

```bash
$> npm install
```

#### Run

See [Run the Application](https://github.com/a2aproject/a2a-inspector?tab=readme-ov-file#3-run-the-application)

```bash
$> bash ./run.sh
```

#### Usage

**Connect**:

![Connect](./assets/img/a2a-inspector/Connect.png)

**Chat**:

![Chat](./assets/img/semantic-kernel/plugins/light/Turn_on_the_light.png)

### Everything (docker-compose)

[See `docker-compose.yml`](./docker-compose.yml) for more details

1. `$> docker-compose up`

## Resources

- [Introducing Microsoft Agent Framework](https://azure.microsoft.com/en-us/blog/introducing-microsoft-agent-framework/)

### Examples

- [`semantic-kernel`](https://github.com/microsoft/semantic-kernel)
- [`a2a-samples`](https://github.com/a2aproject/a2a-samples)

### GitHub

- [`microsoft`](https://github.com/microsoft)
  - ~~[`semantic-kernel`](https://github.com/microsoft/semantic-kernel)~~
  - [`agent-framework`](https://github.com/microsoft/agent-framework)
  - [`Agents`](https://github.com/microsoft/Agents)
    - [`/samples`](https://github.com/microsoft/Agents/tree/main/samples)
- [`a2aproject`](https://github.com/a2aproject) /
  - [`A2A`](https://github.com/a2aproject/A2A)
  - [`a2a-samples`](https://github.com/a2aproject/a2a-samples)
  - [`a2a-inspector`](https://github.com/a2aproject/a2a-inspector)

### Java

- [Java Frameworks You Must Know in 2024](https://blog.jetbrains.com/idea/2024/04/java-frameworks-you-must-know-in-2024/)

### Medium

- [Setting Up ESLint and Prettier for a TypeScript Project](https://medium.com/@robinviktorsson/setting-up-eslint-and-prettier-for-a-typescript-project-aa2434417b8f)
