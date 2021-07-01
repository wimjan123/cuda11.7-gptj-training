ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.4.0-base-ubi8

LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

RUN yum install -y \
    cuda-libraries-11-4-11.4.0-1 \
    cuda-nvtx-11-4-11.4.43-1 \
    libnpp-11-4-11.4.0.33-1 \
    libcublas-11-4-11.5.2.43-1 \
    && yum clean all \
    && rm -rf /var/cache/yum/*

