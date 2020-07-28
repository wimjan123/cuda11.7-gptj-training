ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.0-base-ubuntu18.04

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

ENV NCCL_VERSION 2.7.8

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-libraries-11-0=11.0.2-1 \
    libnpp-11-0=11.1.0.218-1 \
    cuda-nvtx-11-0=11.0.167-1 \
    libcublas-11-0=11.1.0.229-1 \
    libnccl2=$NCCL_VERSION-1+cuda11.0 \
    && apt-mark hold libnccl2 \
    && rm -rf /var/lib/apt/lists/*

