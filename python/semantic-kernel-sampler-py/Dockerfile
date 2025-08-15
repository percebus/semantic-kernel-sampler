FROM python:3.12.8 AS base
WORKDIR /usr/app
COPY . .
# RUN bash scripts/bash/clean.ba.sh  # TODO

# SRC: https://docs.astral.sh/uv/guides/integration/docker/
FROM base AS uv
RUN curl -LsSf https://astral.sh/uv/0.8.9/install.sh | sh
ENV PATH="/root/.local/bin/:$PATH"
RUN uv --version
# RUN uv python install  # TODO

FROM uv AS dev
RUN bash scripts/uv/tool/install.ba.sh
RUN uvx -- pypyr build release=False

FROM dev AS tested
RUN uvx -- pypyr ci stats=False

FROM uv AS built
RUN uvx -- pypyr build release=True

# TODO use light image. alpine?
FROM built AS release
CMD [ "python", "src/semantic_kernel_sampler" ]
