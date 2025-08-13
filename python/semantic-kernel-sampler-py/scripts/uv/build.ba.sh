#!/bin/bash

set -e
set -x

uv build --all-packages --wheel

set +x
set +x
