#!/bin/bash

set -e
set -x

uv run -- pypyr ci

set +x
set +e
