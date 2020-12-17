ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.1-base-ubi7

LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV NCCL_VERSION 2.7.8

RUN /usr/bin/yum install -y \
    cuda-libraries-11-1-11.1.1-1 \
    cuda-nvtx-11-1-11.1.74-1 \
    libnpp-11-1-11.1.2.301-1 \
    libcublas-11-1-11.3.0.106-1 \
    libnccl-2.7.8-1+cuda11.1 \
    && /usr/bin/yum clean all \
    && rm -rf /var/cache/yum/*

