ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.3.1-devel-centos8
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 8.2.0.53
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN yum install -y \
    libcudnn8-devel-${CUDNN_VERSION}-1.cuda11.3 \
    && yum clean all \
    && rm -rf /var/cache/yum/*
