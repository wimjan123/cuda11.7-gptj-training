ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.3.0-base-centos8

LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV NCCL_VERSION 2.9.6

RUN yum install -y \
    cuda-libraries-11-3-11.3.0-1 \
    cuda-nvtx-11-3-11.3.58-1 \
    libnpp-11-3-11.3.3.44-1 \
    libcublas-11-3-11.4.2.10064-1 \
    libnccl-2.9.6-1+cuda11.3 \
    && yum clean all \
    && rm -rf /var/cache/yum/*

