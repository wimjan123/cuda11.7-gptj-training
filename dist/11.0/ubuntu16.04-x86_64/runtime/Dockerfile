ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.0-base-ubuntu16.04-rc

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-libraries-11-0=11.0.1-1 \
    libnpp-11-0=11.0.0.191-1 \
    cuda-nvtx-11-0=11.0.167-1 \
    && rm -rf /var/lib/apt/lists/*

RUN apt update && apt install curl xz-utils -y --no-install-recommends && NCCL_DOWNLOAD_SUM=d112b722bf557cff96d571ac3386e4f539be7b3e9412561bde59b0ad6e59263d && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/nccl/v2.7/nccl_2.7.3-1+cuda11.0_x86_64.txz -O && \
    echo "$NCCL_DOWNLOAD_SUM  nccl_2.7.3-1+cuda11.0_x86_64.txz" | sha256sum -c - && \
    tar --no-same-owner --keep-old-files --lzma -xvf nccl_2.7.3-1+cuda11.0_x86_64.txz -C /usr/local/cuda/lib64/ --strip-components=2 --wildcards '*/lib/libnccl.so.*' && \
    tar --no-same-owner --keep-old-files --lzma -xvf  nccl_2.7.3-1+cuda11.0_x86_64.txz -C /usr/lib/pkgconfig/ --strip-components=3 --wildcards '*/lib/pkgconfig/*' && \
    rm nccl_2.7.3-1+cuda11.0_x86_64.txz && \
    ldconfig && rm -rf /var/lib/apt/lists/*
