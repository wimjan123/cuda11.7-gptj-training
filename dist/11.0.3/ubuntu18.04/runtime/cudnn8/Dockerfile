ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.0.3-runtime-ubuntu18.04 as base

FROM base as base-amd64

ENV CUDNN_VERSION 8.0.5.39

ENV NV_CUDNN_PACKAGE "libcudnn8=$CUDNN_VERSION-1+cuda11.0"
ENV NV_CUDNN_PACKAGE_NAME "libcudnn8"

FROM base as base-ppc64le

ENV CUDNN_VERSION 8.0.4.30

ENV NV_CUDNN_PACKAGE "libcudnn8=$CUDNN_VERSION-1+cuda11.0"
ENV NV_CUDNN_PACKAGE_NAME "libcudnn8"

FROM base-${TARGETARCH}

ARG TARGETARCH

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"





RUN apt-get update && apt-get install -y --no-install-recommends \
    ${NV_CUDNN_PACKAGE} \
    ${NV_CUDNN_PACKAGE_DEV} \
    && apt-mark hold ${NV_CUDNN_PACKAGE_NAME} && \
    rm -rf /var/lib/apt/lists/*
