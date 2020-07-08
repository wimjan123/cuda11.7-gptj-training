ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.2-devel-centos7
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 8.0.1.13
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

# cuDNN license: https://developer.nvidia.com/cudnn/license_agreement
RUN CUDNN_DOWNLOAD_SUM=0e15a28b4bb1fb97370f406deb14af2deb3e1670d330b5c148cbf7d3c1ff7e0e && \
    curl -fsSL http://developer.download.nvidia.com/compute/redist/cudnn/v8.0.1/cudnn-10.2-linux-ppc64le-v8.0.1.13.tgz -O && \
    echo "$CUDNN_DOWNLOAD_SUM  cudnn-10.2-linux-ppc64le-v8.0.1.13.tgz" | sha256sum -c - && \
    tar --no-same-owner -xzf cudnn-10.2-linux-ppc64le-v8.0.1.13.tgz -C /usr/local && \
    rm cudnn-10.2-linux-ppc64le-v8.0.1.13.tgz && \
    ldconfig
