ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.2-base-ubuntu18.04

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-libraries-$CUDA_PKG_VERSION \
    cuda-npp-$CUDA_PKG_VERSION \
    cuda-nvtx-$CUDA_PKG_VERSION \
    libcublas10=10.2.2.89-1 \
    && rm -rf /var/lib/apt/lists/*

RUN apt update && apt install curl xz-utils -y --no-install-recommends && NCCL_DOWNLOAD_SUM=ccd4960ef3eb22f0ed8fcb91d3b8ae71e7c88cf8fb6eca8f5c039d0acf1bdac8 && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/nccl/v2.7/nccl_2.7.3-1+cuda10.2_ppc64le.txz -O && \
    echo "$NCCL_DOWNLOAD_SUM  nccl_2.7.3-1+cuda10.2_ppc64le.txz" | sha256sum -c - && \
    tar --no-same-owner --keep-old-files --lzma -xvf nccl_2.7.3-1+cuda10.2_ppc64le.txz -C /usr/local/cuda/lib64/ --strip-components=2 --wildcards '*/lib/libnccl.so.*' && \
    tar --no-same-owner --keep-old-files --lzma -xvf  nccl_2.7.3-1+cuda10.2_ppc64le.txz -C /usr/lib/pkgconfig/ --strip-components=3 --wildcards '*/lib/pkgconfig/*' && \
    rm nccl_2.7.3-1+cuda10.2_ppc64le.txz && \
    ldconfig && rm -rf /var/lib/apt/lists/*
