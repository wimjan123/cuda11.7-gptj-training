#!/usr/bin/env bats

load helpers

image="${IMAGE_NAME}:${CUDA_VERSION}-devel-${OS}${IMAGE_TAG_SUFFIX}"

function setup() {
    docker pull ${image}
    check_runtime
}

@test "check_NVIDIA_REQUIRES_CUDA" {
    # The devel images for x86_64 should always contain "brand=tesla"
    if [ ${ARCH} != "x86_64" ]; then
       skip "Only needed on x86_64."
    fi
    unsupported=('8.0', '9.0', '9.1', '9.2')
    image_name=$(echo "${image}" | cut -d: -f3)
    if printf '%s' "${unsupported[@]}" | grep -q "${image_name}"; then
        skip "libnccl2 not supported for this platform"
    fi
    docker_run --rm --gpus 0 ${image} bash -c "printenv | grep -q 'brand=tesla'"
    [ "$status" -eq 0 ]
}
