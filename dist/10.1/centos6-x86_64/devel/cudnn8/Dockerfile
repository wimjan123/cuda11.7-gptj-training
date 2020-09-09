ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.1-devel-centos6
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 8.0.3.33
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

# cuDNN license: https://developer.nvidia.com/cudnn/license_agreement
RUN CUDNN_DOWNLOAD_SUM=4752ac6aea4e4d2226061610d6843da6338ef75a93518aa9ce50d0f58df5fb07 && \
    curl -fsSL http://developer.download.nvidia.com/compute/redist/cudnn/v8.0.3/cudnn-10.1-linux-x64-v8.0.3.33.tgz -O && \
    echo "$CUDNN_DOWNLOAD_SUM  cudnn-10.1-linux-x64-v8.0.3.33.tgz" | sha256sum -c - && \
    tar --no-same-owner -xzf cudnn-10.1-linux-x64-v8.0.3.33.tgz -C /usr/local && \
    rm cudnn-10.1-linux-x64-v8.0.3.33.tgz && \
    ldconfig
