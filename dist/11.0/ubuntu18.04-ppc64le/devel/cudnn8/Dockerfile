ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.0-devel-ubuntu18.04-rc
LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

ENV CUDNN_VERSION 8.0.0.180

LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 curl ca-certificates

RUN CUDNN_DOWNLOAD_SUM=183b750f59cb3eec960dbaf61b9cde1e88621771058a13ce93d5f609d995206d && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.0/Ubuntu18_04-ppc64le/libcudnn8_8.0.0.180-1+cuda11.0_ppc64el.deb -O && \
    echo "$CUDNN_DOWNLOAD_SUM  libcudnn8_8.0.0.180-1+cuda11.0_ppc64el.deb" | sha256sum -c - && \
    dpkg -i libcudnn8_8.0.0.180-1+cuda11.0_ppc64el.deb && \
    rm -f libcudnn8_8.0.0.180-1+cuda11.0_ppc64el.deb

RUN CUDNN_DEV_DOWNLOAD_SUM=7f8f8fd0d320899db03494585f60b22e08f792cf46a1c2e6834e493e2fd004fc && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.0/Ubuntu18_04-ppc64le/libcudnn8-dev_8.0.0.180-1+cuda11.0_ppc64el.deb -O && \
    echo "$CUDNN_DEV_DOWNLOAD_SUM  libcudnn8-dev_8.0.0.180-1+cuda11.0_ppc64el.deb" | sha256sum -c - && \
    dpkg -i libcudnn8-dev_8.0.0.180-1+cuda11.0_ppc64el.deb && \
    rm -f libcudnn8-dev_8.0.0.180-1+cuda11.0_ppc64el.deb

RUN rm -rf /var/lib/apt/lists/*
