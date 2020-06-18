ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.2-runtime-ubuntu18.04

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-nvml-dev-$CUDA_PKG_VERSION \
    cuda-command-line-tools-$CUDA_PKG_VERSION \
    cuda-nvcc-$CUDA_PKG_VERSION \
    cuda-nvprof-$CUDA_PKG_VERSION \
    cuda-npp-dev-$CUDA_PKG_VERSION \
    cuda-libraries-dev-$CUDA_PKG_VERSION \
    cuda-minimal-build-$CUDA_PKG_VERSION \
    libcublas-dev=10.2.2.89-1 \
    && rm -rf /var/lib/apt/lists/*

RUN apt update && apt install curl xz-utils -y --no-install-recommends && NCCL_DOWNLOAD_SUM=a9ee790c3fc64b0ecbb00db92eddc1525552eda10a8656ff4b7380f66d81bda1 && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/nccl/v2.7/nccl_2.7.3-1+cuda10.2_x86_64.txz -O && \
    echo "$NCCL_DOWNLOAD_SUM  nccl_2.7.3-1+cuda10.2_x86_64.txz" | sha256sum -c - && \
    tar --no-same-owner --keep-old-files --lzma -xvf  nccl_2.7.3-1+cuda10.2_x86_64.txz -C /usr/local/cuda/include/ --strip-components=2 --wildcards '*/include/*' && \
    tar --no-same-owner --keep-old-files --lzma -xvf  nccl_2.7.3-1+cuda10.2_x86_64.txz -C /usr/local/cuda/lib64/ --strip-components=2 --wildcards '*/lib/libnccl.so' && \
    rm nccl_2.7.3-1+cuda10.2_x86_64.txz && \
    ldconfig && rm -rf /var/lib/apt/lists/*

ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs