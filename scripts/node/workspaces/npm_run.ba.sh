#!/bin/bash

set -e

cmd=${1}
if [ -z ${cmd} ]; then
  cmd="test"
fi

set -x

# TODO for each package
npm run ${cmd} --prefix ./node/mcp-server.examples.quick-start
npm run ${cmd} --prefix ./node/rest-app
npm run ${cmd} --prefix ./node/mcp-server.rest-app.posts

set +x
set +e
