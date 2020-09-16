#!/usr/bin/env bats

load helpers

image="${IMAGE_NAME}:${CUDA_VERSION}-devel-${OS}${IMAGE_TAG_SUFFIX}"

function setup() {
    check_runtime
}

function teardown() {
    cleanup
}

function dq_ubuntu() {
    printf "%s\n" "RUN apt-get update && apt-get install -y make g++ git" >> Dockerfile
    if [[ "${CUDA_VERSION}" == "8.0" ]]; then
		printf "%s\n" "RUN apt-get install -y cuda-samples-8-0" >> Dockerfile
	fi
}

function dq_rhel() {
    pkgmgr="yum"
    pkgcomp="gcc-c++"
    if [[ "${OS_VERSION}" == "8" ]]; then
        pkgmgr="dnf"
    fi
    if [[ "${ARCH}" != "x86_64" ]]; then
        pkgcomp="gcc.${ARCH}"
    fi
    printf "%s\n" "RUN ${pkgmgr} install -y make ${pkgcomp} git" >> Dockerfile
    if [[ "${CUDA_VERSION}" == "8.0" ]]; then
		if [[ "${OS}" == "ubi7" ]]; then
			# Dependencies are broken for cuda 8.0 samples on ubi7
			printf "%s\n" "RUN rpm -Uvh --nodeps \$(repoquery --location cuda-samples-8-0)" >> Dockerfile
			printf "%s\n" "RUN ${pkgmgr} install -y make" >> Dockerfile
		else
			printf "%s\n" "RUN ${pkgmgr} install -y cuda-samples-8-0" >> Dockerfile
		fi
	fi
}

@test "deviceQuery" {
    printf "%s\n" "FROM ${image}" > Dockerfile
    [[ "${OS_NAME}" == "ubuntu" ]] && dq_ubuntu
    [[ "${OS_NAME}" == "centos" ]] || [[ "${OS_NAME}" == "ubi" ]] && dq_rhel
    if [[ "${CUDA_VERSION}" == "8.0" ]]; then
		printf "%s\n" "WORKDIR /usr/local/cuda/samples/1_Utilities/deviceQuery" >> Dockerfile
		printf "%s\n" "RUN make " >> Dockerfile
		printf "%s\n" "CMD ./deviceQuery" >> Dockerfile
    else
		printf "%s\n" "RUN git clone https://github.com/NVIDIA/cuda-samples.git" >> Dockerfile
		printf "%s\n" "WORKDIR cuda-samples/Samples/deviceQuery/" >> Dockerfile
		if [ $(echo $CUDA_VERSION | cut -f1 -d.) -lt 10 ]; then
			printf "%s\n" "RUN git checkout tags/v9.2" >> Dockerfile
		fi
		# SMS 3.5 for Tesla K40 and Geforce GT 710
		printf "%s\n" "RUN make TARGET_ARCH='${ARCH}' SMS='35' " >> Dockerfile
		printf "%s\n" "CMD ./deviceQuery" >> Dockerfile
	fi
    docker_build -t "${image}-${BATS_TEST_NAME}" .
    docker_run --rm --gpus 0 ${image}-${BATS_TEST_NAME}
    docker rmi -f ${image}-${BATS_TEST_NAME}
    [ "$status" -eq 0 ]
}

@test "vectorAdd {
    printf "%s\n" "FROM $image" > Dockerfile
    [[ "${OS_NAME}" == "ubuntu" ]] && dq_ubuntu
    [[ "${OS_NAME}" == "centos" ]] || [[ "${OS_NAME}" == "ubi" ]] && dq_rhel
    printf "%s\n" "RUN git clone https://github.com/NVIDIA/cuda-samples.git" >> Dockerfile
    printf "%s\n" "WORKDIR cuda-samples/Samples/vectorAdd_nvrtc" >> Dockerfile
    if [ $(echo $CUDA_VERSION | cut -f1 -d.) -lt 10 ]; then
        printf "%s\n" "RUN git checkout tags/v9.2" >> Dockerfile
    fi
    # SMS 3.5 for Tesla K40 and Geforce GT 710
    printf "%s\n" "RUN make TARGET_ARCH='${ARCH}' SMS='35'" >> Dockerfile
    printf "%s\n" "CMD ./vectorAdd_nvrtc" >> Dockerfile
    docker_build -t "${image}-${BATS_TEST_NAME}" .
    docker_run --rm --gpus 0 ${image}-${BATS_TEST_NAME}
    docker rmi -f ${image}-${BATS_TEST_NAME}
    [ "$status" -eq 0 ]
}

@test "matrixMulDrv {
    printf "%s\n" "FROM ${image}" > Dockerfile
    [[ "${OS_NAME}" == "ubuntu" ]] && dq_ubuntu
    [[ "${OS_NAME}" == "centos" ]] || [[ "${OS_NAME}" == "ubi" ]] && dq_rhel
    printf "%s\n" "RUN git clone https://github.com/NVIDIA/cuda-samples.git" >> Dockerfile
    printf "%s\n" "WORKDIR cuda-samples/Samples/matrixMulDrv/" >> Dockerfile
    if [ $(echo $CUDA_VERSION | cut -f1 -d.) -lt 10 ]; then
        printf "%s\n" "RUN git checkout tags/v9.2" >> Dockerfile
    fi
    # SMS 3.5 for Tesla K40 and Geforce GT 710
    printf "%s\n" "RUN make TARGET_ARCH='${ARCH}' SMS='35'" >> Dockerfile
    printf "%s\n" "CMD ./matrixMulDrv" >> Dockerfile
    docker_build -t "${image}-${BATS_TEST_NAME}" .
    docker_run --rm --gpus 0 ${image}-${BATS_TEST_NAME}
    docker rmi -f ${image}-${BATS_TEST_NAME}
    [ "$status" -eq 0 ]
}
