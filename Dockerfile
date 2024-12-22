FROM node:22 AS base
ENTRYPOINT [ "npm", "run" ]

FROM base AS root
WORKDIR /usr/project
COPY . .
RUN ls -la
RUN npm run setup:docker --if-present && npm ci
CMD [ "test" ]

FROM base AS rest-app
WORKDIR /usr/project
COPY ./node/rest-app .
RUN ls -la
RUN npm run setup:docker --if-present && npm ci
CMD [ "test" ]
