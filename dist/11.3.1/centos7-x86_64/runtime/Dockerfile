ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.3.1-base-centos7

LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV NCCL_VERSION 2.9.9

RUN yum install -y \
    cuda-libraries-11-3-11.3.1-1 \
    cuda-nvtx-11-3-11.3.109-1 \
    libnpp-11-3-11.3.3.95-1 \
    libcublas-11-3-11.5.1.109-1 \
    libnccl-2.9.9-1+cuda11.3 \
    && yum clean all \
    && rm -rf /var/cache/yum/*

