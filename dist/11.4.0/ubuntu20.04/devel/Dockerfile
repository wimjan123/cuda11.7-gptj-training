ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.4.0-runtime-ubuntu20.04 as base

ENV NV_CUDA_LIB_VERSION "11.4.0-1"
ENV NV_LIBCUBLAS_PACKAGE_NAME_DEV "libcublas-dev-11-4"

FROM base as base-amd64

ENV NV_CUDA_CUDART_DEV_VERSION "11.4.43-1"
ENV NV_NVML_DEV_VERSION "11.4.43-1"
ENV NV_LIBCUSPARSE_DEV_VERSION "11.6.0.43-1"
ENV NV_LIBNPP_DEV_VERSION "11.4.0.33-1"
ENV NV_LIBCUBLAS_DEV_VERSION "11.5.2.43-1"

ENV NCCL_VERSION 2.10.3
ENV NV_LIBNCCL_PACKAGE_DEV "libnccl-dev=2.10.3-1+cuda11.4"
ENV NV_LIBNCCL_PACKAGE_NAME_DEV "libnccl-dev"

FROM base as base-arm64


ENV NV_CUDA_CUDART_DEV_VERSION "11.4.43-1"
ENV NV_NVML_DEV_VERSION "11.4.43-1"
ENV NV_LIBCUSPARSE_DEV_VERSION "11.6.0.43-1"
ENV NV_LIBNPP_DEV_VERSION "11.4.0.33-1"
ENV NV_LIBCUBLAS_DEV_VERSION "11.5.2.43-1"

ENV NCCL_VERSION 2.10.3
ENV NV_LIBNCCL_PACKAGE_DEV "libnccl-dev=2.10.3-1+cuda11.4"
ENV NV_LIBNCCL_PACKAGE_NAME_DEV "libnccl-dev"

FROM base-${TARGETARCH}

ARG TARGETARCH

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

RUN apt-get update && apt-get install -y --no-install-recommends \
    libtinfo5 libncursesw5 \
    cuda-cudart-dev-11-4=${NV_CUDA_CUDART_DEV_VERSION} \
    cuda-command-line-tools-11-4=${NV_CUDA_LIB_VERSION} \
    cuda-minimal-build-11-4=${NV_CUDA_LIB_VERSION} \
    cuda-libraries-dev-11-4=${NV_CUDA_LIB_VERSION} \
    cuda-nvml-dev-11-4=${NV_NVML_DEV_VERSION} \
    libnpp-dev-11-4=${NV_LIBNPP_DEV_VERSION} \
    libcusparse-dev-11-4=${NV_LIBCUSPARSE_DEV_VERSION} \
    ${NV_LIBNCCL_PACKAGE_DEV} \
    ${NV_LIBCUBLAS_PACKAGE_NAME_DEV}=${NV_LIBCUBLAS_DEV_VERSION} \
    && rm -rf /var/lib/apt/lists/*

# apt from auto upgrading the cublas package. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN apt-mark hold ${NV_LIBCUBLAS_PACKAGE_NAME_DEV} ${NV_LIBNCCL_PACKAGE_NAME_DEV}


ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs