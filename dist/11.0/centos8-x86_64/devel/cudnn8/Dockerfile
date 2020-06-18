ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.0-devel-centos8-rc
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 8.0.0.180
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN CUDNN_DOWNLOAD_SUM=f9c9741619a54b1b01e858906dfcc9f58e653e713621c22bab3507dc6c1111e9 && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.0/RHEL8_1-x64/libcudnn8-8.0.0.180-1.cuda11.0.x86_64.rpm -O && \
    echo "$CUDNN_DOWNLOAD_SUM  libcudnn8-8.0.0.180-1.cuda11.0.x86_64.rpm" | sha256sum -c - && \
    rpm -vih libcudnn8-8.0.0.180-1.cuda11.0.x86_64.rpm && \
    rm -f libcudnn8-8.0.0.180-1.cuda11.0.x86_64.rpm && \
    ldconfig
