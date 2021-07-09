ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.2.1-runtime-ubuntu16.04 as base

ENV NV_CUDA_LIB_VERSION "11.2.1-1"
ENV NV_LIBCUBLAS_PACKAGE_NAME_DEV "libcublas-dev-11-2"

FROM base as base-amd64

ENV NV_CUDA_RUNTIME_VERSION_DEV "11.2.146-1"
ENV NV_NVML_VERSION_DEV "11.2.67-1"
ENV NV_LIBCUSPARSE_VERSION_DEV "11.4.0.135-1"
ENV NV_LIBNPP_VERSION_DEV "11.3.2.139-1"
ENV NV_LIBCUBLAS_VERSION_DEV "11.4.1.1026-1"

FROM base-${TARGETARCH}

ARG TARGETARCH

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-cudart-dev-11-2=${NV_CUDA_RUNTIME_VERSION_DEV} \
    cuda-command-line-tools-11-2=${NV_CUDA_LIB_VERSION} \
    cuda-minimal-build-11-2=${NV_CUDA_LIB_VERSION} \
    cuda-libraries-dev-11-2=${NV_CUDA_LIB_VERSION} \
    cuda-nvml-dev-11-2=${NV_NVML_VERSION_DEV} \
    libnpp-dev-11-2=${NV_LIBNPP_VERSION_DEV} \
    libcusparse-dev-11-2=${NV_LIBCUSPARSE_VERSION_DEV} \
    ${NV_LIBNCCL_PACKAGE_DEV} \
    ${NV_LIBCUBLAS_PACKAGE_NAME_DEV}=${NV_LIBCUBLAS_VERSION_DEV} \
    && rm -rf /var/lib/apt/lists/*

# apt from auto upgrading the cublas package. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN apt-mark hold ${NV_LIBCUBLAS_PACKAGE_NAME_DEV} ${NV_LIBNCCL_PACKAGE_NAME_DEV}


ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs