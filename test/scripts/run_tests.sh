#!/bin/bash

set -x
set -e

for test in $(find test/ -iname "*.bats"); do
  if [[ "${test}" == *nvidia-smi* ]] && [[ "${ARCH}" != "x86_64" ]]; then
      # We are running tests on an x86_64 machine for multi-arch and nvidia-smi is passed to the
      # container from the host so it won't work on anything but x86_64.
      echo "Skipping test '${test}' on architecture ${ARCH}"
      continue
  fi
  if [[ "${test}" == *samples* ]]; then
      # Samples repo is not working with 11.0, need to get internal repo for this
      echo "Skipping test '${test}' on architecture ${ARCH}"
      continue
  fi
  dir=$(dirname ${test})
  name=$(basename ${test})
  curDir=${PWD}
  cd ${dir}
  echo "# Running test script '${test}'"
  /usr/local/bin/bats --tap ${name}
  cd ${curDir}
done
