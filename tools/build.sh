#!/bin/sh
# usage: tools/build.sh <video-folder>   -> regenerates architecture.svg + architecture.png
set -e
cd "$(dirname "$0")/.."
PY=${PY:-python3}
$PY "$1/architecture.py"
$PY tools/render.py "$1/architecture.svg" "$1/architecture.png"
