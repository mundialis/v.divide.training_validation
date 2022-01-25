#!/usr/bin/env bash

# fail on non-zero return code from a subprocess
set -e

FILENAME=$(basename "$(find . -name *.html -maxdepth 1)")
ADDON="${FILENAME%%.html}"

CURRENTDIR=$(pwd)
g.extension extension=${ADDON} url=. && \
for file in $(find . -type f -name test*.py) ; \
do  \
  echo ${file}
  BASENAME=$(basename "${file}") ; \
  DIR=$(dirname "${file}") ; \
  cd ${CURRENTDIR}/${DIR} && python3 -m unittest ${BASENAME}
done
