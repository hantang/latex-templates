#!/usr/bin/env bash
set -eu

SRC_DIR="latex-data"
WIKI_DIR="wiki"

echo "Update doc"
pushd ${SRC_DIR}
bash ./update-wiki.sh
popd

echo "Build site"
pushd ${WIKI_DIR}
mkdocs build
popd

echo "Doc structs"
echo "PWD: $(pwd)"
ls -l ${WIKI_DIR}/
ls -l ${WIKI_DIR}/**/*.md
tail ${WIKI_DIR}/mkdocs.yml
