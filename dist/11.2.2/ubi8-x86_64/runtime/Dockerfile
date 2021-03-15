ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.2.2-base-ubi8

LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV NCCL_VERSION 2.8.4

RUN yum install -y \
    cuda-libraries-11-2-11.2.2-1 \
    cuda-nvtx-11-2-11.2.152-1 \
    libnpp-11-2-11.3.2.152-1 \
    libcublas-11-2-11.4.1.1043-1 \
    libnccl-2.8.4-1+cuda11.2 \
    && yum clean all \
    && rm -rf /var/cache/yum/*

