#!/bin/bash

set -e

filename="requirements.uv.tool.txt"
echo "Installing ${filename}..."
if [[ -z $(grep '[^[:space:]]' $filename) ]]; then
  echo "${filename} is empty, skipping..."
  exit 0
fi

set -v

cat ${filename}
cat ${filename} | sed 's/.*/"&"/' | xargs -n 1 uv tool install --force
uv tool list

set +v
set +e
