ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.4.0-base-centos7 as base

ENV NV_CUDA_LIB_VERSION 11.4.0-1

FROM base as base-amd64

ENV NV_NVTX_VERSION 11.4.43-1
ENV NV_LIBNPP_VERSION 11.4.0.33-1
ENV NV_LIBCUBLAS_VERSION 11.5.2.43-1
FROM base-${TARGETARCH}

ARG TARGETARCH

LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

RUN yum install -y \
    cuda-libraries-11-4-${NV_CUDA_LIB_VERSION} \
    cuda-nvtx-11-4-${NV_NVTX_VERSION} \
    libnpp-11-4-${NV_LIBNPP_VERSION} \
    libcublas-11-4-${NV_LIBCUBLAS_VERSION} \
    ${NV_LIBNCCL_PACKAGE} \
    && yum clean all \
    && rm -rf /var/cache/yum/*

