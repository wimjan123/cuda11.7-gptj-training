ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.0-devel-ubuntu16.04
LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

ENV CUDNN_VERSION 8.0.1.13

LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 curl ca-certificates

RUN CUDNN_DOWNLOAD_SUM=37735460519b1df1041cc2742e7058206dfcb6299319f621d085f13ed46a75eb && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.1/Ubuntu16_04-x64/libcudnn8_8.0.1.13-1+cuda11.0_amd64.deb -O && \
    echo "$CUDNN_DOWNLOAD_SUM  libcudnn8_8.0.1.13-1+cuda11.0_amd64.deb" | sha256sum -c - && \
    dpkg -i libcudnn8_8.0.1.13-1+cuda11.0_amd64.deb && \
    rm -f libcudnn8_8.0.1.13-1+cuda11.0_amd64.deb

RUN CUDNN_DEV_DOWNLOAD_SUM=98cb98f22d0efba6d19af4e7029e5f063fb8d9f99692965059f0d9f7485b7867 && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.1/Ubuntu16_04-x64/libcudnn8-dev_8.0.1.13-1+cuda11.0_amd64.deb -O && \
    echo "$CUDNN_DEV_DOWNLOAD_SUM  libcudnn8-dev_8.0.1.13-1+cuda11.0_amd64.deb" | sha256sum -c - && \
    dpkg -i libcudnn8-dev_8.0.1.13-1+cuda11.0_amd64.deb && \
    rm -f libcudnn8-dev_8.0.1.13-1+cuda11.0_amd64.deb

RUN rm -rf /var/lib/apt/lists/*
