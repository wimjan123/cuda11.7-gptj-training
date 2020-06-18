ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.2-devel-centos8
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 8.0.0.180
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN CUDNN_DOWNLOAD_SUM=2ea2e2d302814d8661c6dbf3dc102a874ac1829071eb5503aa0206bfb763cc8d && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.0/RHEL8_1-x64/libcudnn8-8.0.0.180-1.cuda10.2.x86_64.rpm -O && \
    echo "$CUDNN_DOWNLOAD_SUM  libcudnn8-8.0.0.180-1.cuda10.2.x86_64.rpm" | sha256sum -c - && \
    rpm -vih libcudnn8-8.0.0.180-1.cuda10.2.x86_64.rpm && \
    rm -f libcudnn8-8.0.0.180-1.cuda10.2.x86_64.rpm && \
    ldconfig
