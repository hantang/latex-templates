#!/usr/bin/env bash
set -eu

# SRC_DIR="latex-data"
WIKI_DIR="wiki"
echo "SRC_DIR = ${SRC_DIR}"

echo "Update doc"
pushd ${SRC_DIR}
bash ./update-wiki.sh
popd

echo "Build site"
pushd ${WIKI_DIR}
mkdocs build
popd
