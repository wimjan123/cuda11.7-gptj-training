ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.1.1-base-ubuntu20.04 as base

ENV NV_LIBCUBLAS_PACKAGE_NAME "libcublas-11-1"
ENV NV_CUDA_LIB_VERSION "11.1.1-1"

FROM base as base-amd64

ENV NV_NVTX_VERSION "11.1.74-1"
ENV NV_LIBNPP_VERSION "11.1.2.301-1"
ENV NV_LIBCUSPARSE_VERSION "11.3.0.10-1"
ENV NV_LIBCUBLAS_VERSION "11.3.0.106-1"


ENV NCCL_VERSION 2.8.4
ENV NV_LIBNCCL_PACKAGE "libnccl2=2.8.4-1+cuda11.1"
ENV NV_LIBNCCL_PACKAGE_NAME "libnccl2"

FROM base-${TARGETARCH}

ARG TARGETARCH

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-libraries-11-1=${NV_CUDA_LIB_VERSION} \
    libnpp-11-1=${NV_LIBNPP_VERSION} \
    cuda-nvtx-11-1=${NV_NVTX_VERSION} \
    ${NV_LIBCUBLAS_PACKAGE_NAME}=${NV_LIBCUBLAS_VERSION} \
    libcusparse-11-1=${NV_LIBCUSPARSE_VERSION} \
    ${NV_LIBNCCL_PACKAGE} \
    && rm -rf /var/lib/apt/lists/*

# apt from auto upgrading the cublas package. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN apt-mark hold libcublas-11-1 ${NV_LIBNCCL_PACKAGE_NAME}

