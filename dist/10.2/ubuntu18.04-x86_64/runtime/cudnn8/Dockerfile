ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.2-runtime-ubuntu18.04
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

RUN rm -rf /var/lib/apt/lists/*
