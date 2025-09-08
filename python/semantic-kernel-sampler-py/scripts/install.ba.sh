#!/bin/bash

set -e

target_config=$1
echo "target_config:'${target_config}'"

scripts_path="$(dirname "$(readlink -f "$0")")"
echo "Script directory: ${scripts_path}"

set -x

# Upgrades top-level dependencies, like pipx
bash ${scripts_path}/pip/upgrade.ba.sh
pipx ensurepath

# pipx installs CLI executables, like poetry
bash ${scripts_path}/pipx/install.ba.sh

# uv tool install
bash ${scripts_path}/uv/tool/install.ba.sh ${target_config}

# uv sync
# uv build
uv run -- pypyr build

set +x
set +e
