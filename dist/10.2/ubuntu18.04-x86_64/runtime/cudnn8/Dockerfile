ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.2-runtime-ubuntu18.04
LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

ENV CUDNN_VERSION 8.0.1.13

LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 curl ca-certificates

RUN CUDNN_DOWNLOAD_SUM=3400e91a063b25f7b693f223a2662728a80a83ff32684c9024df28cd80199c4d && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.1/Ubuntu18_04-x64/libcudnn8_8.0.1.13-1+cuda10.2_amd64.deb -O && \
    echo "$CUDNN_DOWNLOAD_SUM  libcudnn8_8.0.1.13-1+cuda10.2_amd64.deb" | sha256sum -c - && \
    dpkg -i libcudnn8_8.0.1.13-1+cuda10.2_amd64.deb && \
    rm -f libcudnn8_8.0.1.13-1+cuda10.2_amd64.deb

RUN rm -rf /var/lib/apt/lists/*
