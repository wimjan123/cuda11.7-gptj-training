ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.0-devel-ubuntu18.04
LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

ENV CUDNN_VERSION 8.0.1.13

LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 curl ca-certificates

RUN CUDNN_DOWNLOAD_SUM=c58d41c2f6c82de1f7ad40eb1d7bd005f3b0658ca13962c166b1225669140760 && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.1/Ubuntu18_04-x64/libcudnn8_8.0.1.13-1+cuda11.0_amd64.deb -O && \
    echo "$CUDNN_DOWNLOAD_SUM  libcudnn8_8.0.1.13-1+cuda11.0_amd64.deb" | sha256sum -c - && \
    dpkg -i libcudnn8_8.0.1.13-1+cuda11.0_amd64.deb && \
    rm -f libcudnn8_8.0.1.13-1+cuda11.0_amd64.deb

RUN CUDNN_DEV_DOWNLOAD_SUM=b4fab13efbf8cdc2a2f29c8156144c5ccca6db030909e84598e085449c90310d && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.1/Ubuntu18_04-x64/libcudnn8-dev_8.0.1.13-1+cuda11.0_amd64.deb -O && \
    echo "$CUDNN_DEV_DOWNLOAD_SUM  libcudnn8-dev_8.0.1.13-1+cuda11.0_amd64.deb" | sha256sum -c - && \
    dpkg -i libcudnn8-dev_8.0.1.13-1+cuda11.0_amd64.deb && \
    rm -f libcudnn8-dev_8.0.1.13-1+cuda11.0_amd64.deb

RUN rm -rf /var/lib/apt/lists/*
