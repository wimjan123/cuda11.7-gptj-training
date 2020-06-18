ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.2-devel-ubuntu18.04
LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

ENV CUDNN_VERSION 8.0.0.180

LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 curl ca-certificates

RUN CUDNN_DOWNLOAD_SUM=a03ebe74e0d3b73b96cb0f7814befa4d5a15af87488b1e947086136670032723 && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.0/Ubuntu18_04-x64/libcudnn8_8.0.0.180-1+cuda10.2_amd64.deb -O && \
    echo "$CUDNN_DOWNLOAD_SUM  libcudnn8_8.0.0.180-1+cuda10.2_amd64.deb" | sha256sum -c - && \
    dpkg -i libcudnn8_8.0.0.180-1+cuda10.2_amd64.deb && \
    rm -f libcudnn8_8.0.0.180-1+cuda10.2_amd64.deb

RUN CUDNN_DEV_DOWNLOAD_SUM=0ee2e9aa60f0e1301b28f9fb826bb8c1cc75b1d90410933169b36ba394f9e9c5 && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.0/Ubuntu18_04-x64/libcudnn8-dev_8.0.0.180-1+cuda10.2_amd64.deb -O && \
    echo "$CUDNN_DEV_DOWNLOAD_SUM  libcudnn8-dev_8.0.0.180-1+cuda10.2_amd64.deb" | sha256sum -c - && \
    dpkg -i libcudnn8-dev_8.0.0.180-1+cuda10.2_amd64.deb && \
    rm -f libcudnn8-dev_8.0.0.180-1+cuda10.2_amd64.deb

RUN rm -rf /var/lib/apt/lists/*
