#!/bin/bash

set -e
set -x

uv run -- poe ci

set +x
set +e
