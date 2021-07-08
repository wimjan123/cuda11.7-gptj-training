ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.4.0-base-centos7

LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV NCCL_VERSION 2.10.3

RUN yum install -y \
    cuda-libraries-11-4-11.4.0-1 \
    cuda-nvtx-11-4-11.4.43-1 \
    libnpp-11-4-11.4.0.33-1 \
    libcublas-11-4-11.5.2.43-1 \
    libnccl-2.10.3-1+cuda11.4 \
    && yum clean all \
    && rm -rf /var/cache/yum/*

