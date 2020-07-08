ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.0-devel-ubuntu18.04
LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

ENV CUDNN_VERSION 8.0.1.13

LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 curl ca-certificates

RUN CUDNN_DOWNLOAD_SUM=744c1c518e80ffad4a269021bdb84387fd43581246cf094d9c4a483a87afcc30 && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.1/Ubuntu18_04-ppc64le/libcudnn8_8.0.1.13-1+cuda10.2_ppc64el.deb -O && \
    echo "$CUDNN_DOWNLOAD_SUM  libcudnn8_8.0.1.13-1+cuda10.2_ppc64el.deb" | sha256sum -c - && \
    dpkg -i libcudnn8_8.0.1.13-1+cuda10.2_ppc64el.deb && \
    rm -f libcudnn8_8.0.1.13-1+cuda10.2_ppc64el.deb

RUN CUDNN_DEV_DOWNLOAD_SUM=34a8d098ccd83847f9c18c69bde60d021bd59b18419756bbb2925230ec2d41c0 && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.1/Ubuntu18_04-ppc64le/libcudnn8-dev_8.0.1.13-1+cuda10.2_ppc64el.deb -O && \
    echo "$CUDNN_DEV_DOWNLOAD_SUM  libcudnn8-dev_8.0.1.13-1+cuda10.2_ppc64el.deb" | sha256sum -c - && \
    dpkg -i libcudnn8-dev_8.0.1.13-1+cuda10.2_ppc64el.deb && \
    rm -f libcudnn8-dev_8.0.1.13-1+cuda10.2_ppc64el.deb

RUN rm -rf /var/lib/apt/lists/*
