ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.2-devel-centos7
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 8.0.0.180
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN CUDNN_DOWNLOAD_SUM=69e34d3ff38619392c61d3f1a6144ed2e7835d3b6c8c867b8a3f44eb0b20df94 && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.0/RHEL7_3-x64/libcudnn8-8.0.0.180-1.cuda10.2.x86_64.rpm -O && \
    echo "$CUDNN_DOWNLOAD_SUM  libcudnn8-8.0.0.180-1.cuda10.2.x86_64.rpm" | sha256sum -c - && \
    rpm -vih libcudnn8-8.0.0.180-1.cuda10.2.x86_64.rpm && \
    rm -f libcudnn8-8.0.0.180-1.cuda10.2.x86_64.rpm && \
    ldconfig
