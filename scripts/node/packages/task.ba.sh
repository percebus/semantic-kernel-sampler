# !/bin/bash

set -e

cmd=${1}
if [ -z ${cmd} ]; then
  cmd="test"
fi

set -x

npm run sub:rest-app:${cmd}

set +x
set +e
