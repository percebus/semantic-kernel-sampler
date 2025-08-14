import uvicorn
from lagom import Container
from starlette.applications import Starlette

from semantic_kernel_sampler.dependency_injection.container import container


def run(ctr: Container) -> None:
    starlette_app = container[Starlette]
    uvicorn.run(starlette_app, host="0.0.0.0", port=9999)


def main() -> None:
    run(container)


if __name__ == "__main__":
    main()
