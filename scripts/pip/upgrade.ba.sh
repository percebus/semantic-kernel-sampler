#!/bin/bash

set -e
set -x

pip install --upgrade pip
pip install --upgrade --requirement requirements.upgrade.txt

set +x
set +e
