#!/usr/bin/env bats

load helpers

BASE_IMAGE="base"
if [[ "${CUDA_VERSION:0}" == "8" ]]; then
  BASE_IMAGE="runtime"
fi

image="${IMAGE_NAME}:${CUDA_VERSION}-${BASE_IMAGE}-${OS}${IMAGE_TAG_SUFFIX}"

function setup() {
    check_runtime
}

function teardown() {
    cleanup
}

@test "nvidia-smi" {
    docker_run --rm --gpus 0 ${image} nvidia-smi
    [ "$status" -eq 0 ]
}
