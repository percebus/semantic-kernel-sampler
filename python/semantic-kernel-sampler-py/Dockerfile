FROM python:3.12.8 AS base
WORKDIR /usr/app
COPY . .
RUN bash scripts/bash/clean.ba.sh

FROM base AS dev
RUN bash scripts/install.ba.sh

FROM dev AS test
RUN pypyr ci stats=False

# TODO use light image. alpine?
FROM base AS release
RUN bash scripts/pip/install.ba.sh 'release'
CMD [ "python", "src/semantic_kernel_sampler/" ]
