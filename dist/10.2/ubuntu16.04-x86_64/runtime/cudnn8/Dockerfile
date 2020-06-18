ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.2-runtime-ubuntu16.04
LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

ENV CUDNN_VERSION 8.0.0.180

LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 curl ca-certificates

RUN CUDNN_DOWNLOAD_SUM=089ef933634e5f6a76b0de3deb27e700c4de5784d275563c56b3ce275aeb3985 && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.0/Ubuntu16_04-x64/libcudnn8_8.0.0.180-1+cuda10.2_amd64.deb -O && \
    echo "$CUDNN_DOWNLOAD_SUM  libcudnn8_8.0.0.180-1+cuda10.2_amd64.deb" | sha256sum -c - && \
    dpkg -i libcudnn8_8.0.0.180-1+cuda10.2_amd64.deb && \
    rm -f libcudnn8_8.0.0.180-1+cuda10.2_amd64.deb

RUN rm -rf /var/lib/apt/lists/*
