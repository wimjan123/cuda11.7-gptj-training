ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.1-base-centos8

LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV NCCL_VERSION 2.7.8

RUN yum install -y \
    cuda-libraries-11-1-11.1.0-1 \
    cuda-nvtx-11-1-11.1.74-1 \
    libnpp-11-1-11.1.1.269-1 \
    libcublas-11-1-11.2.1.74-1 \
    libnccl-2.7.8-1+cuda11.1 \
    && yum clean all \
    && rm -rf /var/cache/yum/*

