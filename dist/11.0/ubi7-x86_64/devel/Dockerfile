ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.0-runtime-ubi7

LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV NCCL_VERSION 2.7.8

RUN yum install -y \
    cuda-nvml-devel-11-0-11.0.167-1 \
    cuda-command-line-tools-11-0-11.0.2-1 \
    cuda-cudart-devel-11-0-11.0.194-1 \
    cuda-libraries-devel-11-0-11.0.2-1 \
    cuda-minimal-build-11-0-11.0.2-1 \
    cuda-nvprof-11-0-11.0.194-1 \
    libnpp-devel-11-0-11.1.0.218-1 \
    libcublas-devel-11-0-11.1.0.229-1 \
    libnccl-devel-2.7.8-1+cuda11.0 \
    && yum clean all \
    && rm -rf /var/cache/yum/*

ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs