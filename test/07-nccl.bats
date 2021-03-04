#!/usr/bin/env bats

load helpers

image="${IMAGE_NAME}:${CUDA_VERSION}-devel-${OS}${IMAGE_TAG_SUFFIX}"

function setup() {
    docker pull ${image}
    check_runtime
}

@test "check_libnccl_installed" {
    local CMD="dpkg --get-selections | grep nccl"
    if [[ "${OS_NAME}" == "centos" ]] || [[ "${OS_NAME}" == "centos" ]]; then
        local CMD="rpm -qa | grep nccl"
    fi
    docker_run --rm --gpus 0 ${image} bash -c "$CMD"
    [ "$status" -eq 0 ]
}
