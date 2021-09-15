ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.4.1-base-centos7 as base

ENV NV_CUDA_LIB_VERSION 11.4.1-1

FROM base as base-amd64

ENV NV_NVTX_VERSION 11.4.100-1
ENV NV_LIBNPP_VERSION 11.4.0.90-1
ENV NV_LIBNPP_PACKAGE libnpp-11-4-${NV_LIBNPP_VERSION}
ENV NV_LIBCUBLAS_VERSION 11.5.4.8-1
FROM base-${TARGETARCH}

ARG TARGETARCH

LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

RUN yum install -y \
    cuda-libraries-11-4-${NV_CUDA_LIB_VERSION} \
    cuda-nvtx-11-4-${NV_NVTX_VERSION} \
    ${NV_LIBNPP_PACKAGE} \
    libcublas-11-4-${NV_LIBCUBLAS_VERSION} \
    && yum clean all \
    && rm -rf /var/cache/yum/*