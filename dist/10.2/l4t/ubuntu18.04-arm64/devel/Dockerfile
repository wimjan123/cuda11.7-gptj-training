ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.2-runtime-ubuntu18.04

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-nvml-dev-$CUDA_PKG_VERSION \
    cuda-command-line-tools-10-2=10.2.20200708-1 \
    cuda-nvprof-$CUDA_PKG_VERSION \
    libnpp-dev-10-2=10.2.1.201-1 \
    cuda-libraries-dev-10-2=10.2.20200708-1 \
    cuda-minimal-build-10-2=10.2.20200708-1 \
    libcublas-dev-10-2=10.2.2.201-1 \
    && rm -rf /var/lib/apt/lists/*

ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs