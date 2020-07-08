ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.0-runtime-ubuntu20.04

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-nvml-dev-11-0=11.0.167-1 \
    cuda-command-line-tools-11-0=11.0.2-1 \
    cuda-nvprof-11-0=11.0.194-1 \
    libnpp-dev-11-0=11.1.0.218-1 \
    cuda-libraries-dev-11-0=11.0.2-1 \
    cuda-minimal-build-11-0=11.0.2-1 \
    libcublas-dev-11-0=11.1.0.229-1 \
    libcusparse-11-0=11.1.0.218-1 \
    libcusparse-dev-11-0=11.1.0.218-1 \
    && rm -rf /var/lib/apt/lists/*

RUN apt update && apt install curl xz-utils -y --no-install-recommends && NCCL_DOWNLOAD_SUM=847521ede6b4af4ec66caef51014e15600be418d1689787baaa015722686cab7 && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/nccl/v2.7/nccl_2.7.6-1+cuda11.0_x86_64.txz -O && \
    echo "$NCCL_DOWNLOAD_SUM  nccl_2.7.6-1+cuda11.0_x86_64.txz" | sha256sum -c - && \
    tar --no-same-owner --keep-old-files --lzma -xvf  nccl_2.7.6-1+cuda11.0_x86_64.txz -C /usr/local/cuda/include/ --strip-components=2 --wildcards '*/include/*' && \
    tar --no-same-owner --keep-old-files --lzma -xvf  nccl_2.7.6-1+cuda11.0_x86_64.txz -C /usr/local/cuda/lib64/ --strip-components=2 --wildcards '*/lib/libnccl.so' && \
    rm nccl_2.7.6-1+cuda11.0_x86_64.txz && \
    ldconfig && rm -rf /var/lib/apt/lists/*

ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs