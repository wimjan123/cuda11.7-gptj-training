ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.0.3-runtime-ubuntu20.04 as base

ENV NV_CUDA_LIB_VERSION "11.0.3-1"
ENV NV_LIBCUBLAS_PACKAGE_NAME_DEV "libcublas-dev-11-0"

FROM base as base-amd64

ENV NV_CUDA_RUNTIME_VERSION_DEV "11.0.221-1"
ENV NV_NVML_VERSION_DEV "11.0.167-1"
ENV NV_LIBCUSPARSE_VERSION_DEV "11.1.1.245-1"
ENV NV_LIBNPP_VERSION_DEV "11.1.0.245-1"
ENV NV_LIBCUBLAS_VERSION_DEV "11.2.0.252-1"

ENV NCCL_VERSION 2.10.3
ENV NV_LIBNCCL_PACKAGE_DEV "libnccl-dev=2.10.3-1+cuda11.0"
ENV NV_LIBNCCL_PACKAGE_NAME_DEV "libnccl-dev"

FROM base-${TARGETARCH}

ARG TARGETARCH

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

RUN apt-get update && apt-get install -y --no-install-recommends \
    libtinfo5 libncursesw5 \
    cuda-cudart-dev-11-0=${NV_CUDA_RUNTIME_VERSION_DEV} \
    cuda-command-line-tools-11-0=${NV_CUDA_LIB_VERSION} \
    cuda-minimal-build-11-0=${NV_CUDA_LIB_VERSION} \
    cuda-libraries-dev-11-0=${NV_CUDA_LIB_VERSION} \
    cuda-nvml-dev-11-0=${NV_NVML_VERSION_DEV} \
    libnpp-dev-11-0=${NV_LIBNPP_VERSION_DEV} \
    libcusparse-dev-11-0=${NV_LIBCUSPARSE_VERSION_DEV} \
    ${NV_LIBNCCL_PACKAGE_DEV} \
    ${NV_LIBCUBLAS_PACKAGE_NAME_DEV}=${NV_LIBCUBLAS_VERSION_DEV} \
    && rm -rf /var/lib/apt/lists/*

# apt from auto upgrading the cublas package. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN apt-mark hold ${NV_LIBCUBLAS_PACKAGE_NAME_DEV} ${NV_LIBNCCL_PACKAGE_NAME_DEV}


ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs