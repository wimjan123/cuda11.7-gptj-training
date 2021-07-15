ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.0.3-devel-ubi8 as base

FROM base as base-amd64

ENV CUDNN_VERSION 8.0.5.39-1
ENV NV_CUDNN_PACKAGE libcudnn8-devel-${CUDNN_VERSION}.cuda11.0

FROM base as base-ppc64le

ENV CUDNN_VERSION 8.0.5.39-1
ENV NV_CUDNN_PACKAGE libcudnn8-devel-${CUDNN_VERSION}.cuda11.0

FROM base-${TARGETARCH}

ARG TARGETARCH

LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"




RUN yum install -y ${NV_CUDNN_PACKAGE} \
    && yum clean all \
    && rm -rf /var/cache/yum/*

