import uvicorn
from lagom import Container
from starlette.applications import Starlette

from agent_framework_sampler.config.os_environ.a2a import A2ASettings
from agent_framework_sampler.dependency_injection.container import container


def run(ctr: Container) -> None:
    oStarlette = ctr[Starlette]
    oA2ASettings = ctr[A2ASettings]
    uvicorn.run(oStarlette, host=oA2ASettings.host, port=oA2ASettings.port)


def main() -> None:
    run(container)


if __name__ == "__main__":
    main()
