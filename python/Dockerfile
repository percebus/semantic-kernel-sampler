FROM python:3.12.5 AS base
WORKDIR /usr/app
COPY . .

FROM base AS dev
RUN bash scripts/setup.ba.sh

FROM dev AS test
RUN pypyr ci stats=False

# TODO use light image. alpine?
FROM base AS release
RUN bash scripts/pip/install.ba.sh 'release'
CMD [ "python", "src/semantic-kernel-sampler/" ]
