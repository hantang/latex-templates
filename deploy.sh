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
mkdocs build -f wiki/mkdocs.yml >/dev/null 2>&1

echo "Done"
