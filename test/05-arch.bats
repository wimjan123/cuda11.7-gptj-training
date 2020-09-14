#!/usr/bin/env bats

load helpers

image="${IMAGE_NAME}:${CUDA_VERSION}-devel-${OS}${IMAGE_TAG_SUFFIX}"

function setup() {
    check_runtime
}

@test "check_architecture" {
    docker pull ${image}
    docker_run --rm --gpus 0 ${image} bash -c "[[ \$(uname -m) == ${ARCH} ]] || false"
    [ "$status" -eq 0 ]
}
