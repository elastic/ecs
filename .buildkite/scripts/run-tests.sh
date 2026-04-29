#!/bin/bash
set -euo pipefail

git config --global --add safe.directory "$PWD"
git fetch --prune --unshallow --tags || true

make check yamllint
