ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.2-base-ubuntu18.04

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-libraries-10-2=10.2.20200624-1 \
    libnpp-10-2=10.2.1.195-1 \
    cuda-nvtx-$CUDA_PKG_VERSION \
    libcublas-10-2=10.2.2.195-1 \
    && rm -rf /var/lib/apt/lists/*

