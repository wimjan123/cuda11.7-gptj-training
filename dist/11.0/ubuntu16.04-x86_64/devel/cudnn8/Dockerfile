ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.0-devel-ubuntu16.04-rc
LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

ENV CUDNN_VERSION 8.0.0.180

LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 curl ca-certificates

RUN CUDNN_DOWNLOAD_SUM=fe73570450ae4061d7946d28d3653b32357d72b110a768dc7ed36b6ccfcfbce7 && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.0/Ubuntu16_04-x64/libcudnn8_8.0.0.180-1+cuda11.0_amd64.deb -O && \
    echo "$CUDNN_DOWNLOAD_SUM  libcudnn8_8.0.0.180-1+cuda11.0_amd64.deb" | sha256sum -c - && \
    dpkg -i libcudnn8_8.0.0.180-1+cuda11.0_amd64.deb && \
    rm -f libcudnn8_8.0.0.180-1+cuda11.0_amd64.deb

RUN CUDNN_DEV_DOWNLOAD_SUM=2d3d81e11804eea3f3423a6289f2bb25e9545c2ca2b5502be0d912236ddb613d && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.0/Ubuntu16_04-x64/libcudnn8-dev_8.0.0.180-1+cuda11.0_amd64.deb -O && \
    echo "$CUDNN_DEV_DOWNLOAD_SUM  libcudnn8-dev_8.0.0.180-1+cuda11.0_amd64.deb" | sha256sum -c - && \
    dpkg -i libcudnn8-dev_8.0.0.180-1+cuda11.0_amd64.deb && \
    rm -f libcudnn8-dev_8.0.0.180-1+cuda11.0_amd64.deb

RUN rm -rf /var/lib/apt/lists/*
