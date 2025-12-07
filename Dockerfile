FROM node:22 AS base

FROM base AS project
WORKDIR /usr/project
COPY . .
RUN ls -la
ENTRYPOINT [ "npm", "run" ]

FROM project AS dev
RUN npm run setup:docker --if-present && npm ci
CMD [ "test" ]

FROM dev AS tested
RUN npm test

FROM dev AS modelcontextprotocol.inspector
CMD [ "modelcontextprotocol:inspector" ]
