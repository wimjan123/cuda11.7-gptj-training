ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.2-devel-ubuntu18.04
LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

ENV CUDNN_VERSION 8.0.0.180

LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 curl ca-certificates

RUN CUDNN_DOWNLOAD_SUM=899405cf41d55e11b9000a25ac70c5523307b06eaad90ef603468bc08c7e0ddb && \
    curl -fsSL http://cuda-repo/release-candidates/Libraries/cuDNN/v8.0/8.0.0.180_20200523_28443629/10.2.89-r440/Installer/Ubuntu18_04-aarch64/libcudnn8_8.0.0.180-1+cuda10.2_arm64.deb -O && \
    echo "$CUDNN_DOWNLOAD_SUM  libcudnn8_8.0.0.180-1+cuda10.2_arm64.deb" | sha256sum -c - && \
    dpkg -i libcudnn8_8.0.0.180-1+cuda10.2_arm64.deb && \
    rm -f libcudnn8_8.0.0.180-1+cuda10.2_arm64.deb

RUN CUDNN_DEV_DOWNLOAD_SUM=4b581303d1515d9a204b6639dd0bfee3b27571602f289abe707350abbe3a268d && \
    curl -fsSL http://cuda-repo/release-candidates/Libraries/cuDNN/v8.0/8.0.0.180_20200523_28443629/10.2.89-r440/Installer/Ubuntu18_04-aarch64/libcudnn8-dev_8.0.0.180-1+cuda10.2_arm64.deb -O && \
    echo "$CUDNN_DEV_DOWNLOAD_SUM  libcudnn8-dev_8.0.0.180-1+cuda10.2_arm64.deb" | sha256sum -c - && \
    dpkg -i libcudnn8-dev_8.0.0.180-1+cuda10.2_arm64.deb && \
    rm -f libcudnn8-dev_8.0.0.180-1+cuda10.2_arm64.deb

RUN rm -rf /var/lib/apt/lists/*
