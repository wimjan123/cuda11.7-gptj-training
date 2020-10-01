ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.1-devel-centos8
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 8.0.4.30
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN CUDNN_DOWNLOAD_SUM=387db4f67b7bd41c81644bbbedaf5f5c5453fa4c0876ffabaade75e5c2e0da80 && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.4/RHEL8_1-ppc64le/libcudnn8-8.0.4.30-1.cuda11.1.ppc64le.rpm -O && \
    echo "$CUDNN_DOWNLOAD_SUM  libcudnn8-8.0.4.30-1.cuda11.1.ppc64le.rpm" | sha256sum -c - && \
    rpm -vih libcudnn8-8.0.4.30-1.cuda11.1.ppc64le.rpm && \
    rm -f libcudnn8-8.0.4.30-1.cuda11.1.ppc64le.rpm && \
    ldconfig

RUN CUDNN_DOWNLOAD_SUM=9626e2cd27e9fa878ce549b61af91dadc6a8a96e76f1202b8e229beac9f207b2 && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.4/RHEL8_1-ppc64le/libcudnn8-devel-8.0.4.30-1.cuda11.1.ppc64le.rpm -O && \
    echo "$CUDNN_DOWNLOAD_SUM  libcudnn8-devel-8.0.4.30-1.cuda11.1.ppc64le.rpm" | sha256sum -c - && \
    rpm -vih libcudnn8-devel-8.0.4.30-1.cuda11.1.ppc64le.rpm && \
    rm -f libcudnn8-devel-8.0.4.30-1.cuda11.1.ppc64le.rpm && \
    ldconfig
