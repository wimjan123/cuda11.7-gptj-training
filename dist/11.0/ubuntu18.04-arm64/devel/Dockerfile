ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.0-runtime-ubuntu18.04

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

ENV NCCL_VERSION 2.7.8

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-nvml-dev-11-0=11.0.167-1 \
    cuda-command-line-tools-11-0=11.0.2-1 \
    cuda-nvprof-11-0=11.0.194-1 \
    libnpp-dev-11-0=11.1.0.218-1 \
    cuda-libraries-dev-11-0=11.0.2-1 \
    cuda-minimal-build-11-0=11.0.2-1 \
    libnccl-dev=2.7.8-1+cuda11.0 \
    libcublas-dev-11-0=11.1.0.229-1 \
    libcusparse-11-0=11.1.0.218-1 \
    libcusparse-dev-11-0=11.1.0.218-1 \
    && apt-mark hold libnccl-dev \
    && rm -rf /var/lib/apt/lists/*

ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs