#!/usr/bin/env bats

load helpers

image="${IMAGE_NAME}:${CUDA_VERSION}-devel-${OS}${IMAGE_TAG_SUFFIX}"

@test "remove_test_image" {
    run docker rmi -f ${image}
    [ "$status" -eq 0 ]
}
