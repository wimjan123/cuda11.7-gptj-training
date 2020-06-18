ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.2-runtime-ubuntu18.04
LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

ENV CUDNN_VERSION 8.0.0.180

LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 curl ca-certificates

RUN CUDNN_DOWNLOAD_SUM=9ae85c121c559ceab6f383420724c1c2b9c505ae1b418d4aa2709ae7feb4a4fc && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.0/Ubuntu18_04-ppc64le/libcudnn8_8.0.0.180-1+cuda10.2_ppc64el.deb -O && \
    echo "$CUDNN_DOWNLOAD_SUM  libcudnn8_8.0.0.180-1+cuda10.2_ppc64el.deb" | sha256sum -c - && \
    dpkg -i libcudnn8_8.0.0.180-1+cuda10.2_ppc64el.deb && \
    rm -f libcudnn8_8.0.0.180-1+cuda10.2_ppc64el.deb

RUN rm -rf /var/lib/apt/lists/*
