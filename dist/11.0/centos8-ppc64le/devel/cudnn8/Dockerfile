ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.0-devel-centos8-rc
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 8.0.0.180
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN CUDNN_DOWNLOAD_SUM=d870ec75857f9ae123fefb966a5d28d0468fbf3150f62a97d7af2dffea6f9d98 && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.0/RHEL8_1-ppc64le/libcudnn8-8.0.0.180-1.cuda11.0.ppc64le.rpm -O && \
    echo "$CUDNN_DOWNLOAD_SUM  libcudnn8-8.0.0.180-1.cuda11.0.ppc64le.rpm" | sha256sum -c - && \
    rpm -vih libcudnn8-8.0.0.180-1.cuda11.0.ppc64le.rpm && \
    rm -f libcudnn8-8.0.0.180-1.cuda11.0.ppc64le.rpm && \
    ldconfig
