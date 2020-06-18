ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.0-runtime-ubuntu18.04-rc
LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

ENV CUDNN_VERSION 8.0.0.180

LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 curl ca-certificates

RUN CUDNN_DOWNLOAD_SUM=68558bfa5d1dd6d0300dacaea6ad66ed516ea7dfea01343bd552e6efa107b44c && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.0/Ubuntu18_04-x64/libcudnn8_8.0.0.180-1+cuda11.0_amd64.deb -O && \
    echo "$CUDNN_DOWNLOAD_SUM  libcudnn8_8.0.0.180-1+cuda11.0_amd64.deb" | sha256sum -c - && \
    dpkg -i libcudnn8_8.0.0.180-1+cuda11.0_amd64.deb && \
    rm -f libcudnn8_8.0.0.180-1+cuda11.0_amd64.deb

RUN rm -rf /var/lib/apt/lists/*
