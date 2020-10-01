ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.1-runtime-ubuntu20.04

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

ENV NCCL_VERSION 2.7.8

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-nvml-dev-11-1=11.1.74-1 \
    cuda-command-line-tools-11-1=11.1.0-1 \
    cuda-nvprof-11-1=11.1.69-1 \
    libnpp-dev-11-1=11.1.1.269-1 \
    cuda-libraries-dev-11-1=11.1.0-1 \
    cuda-minimal-build-11-1=11.1.0-1 \
    libnccl-dev=2.7.8-1+cuda11.1 \
    libcublas-dev-11-1=11.2.1.74-1 \
    libcusparse-11-1=11.2.0.275-1 \
    libcusparse-dev-11-1=11.2.0.275-1 \
    && apt-mark hold libnccl-dev \
    && rm -rf /var/lib/apt/lists/*

ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs