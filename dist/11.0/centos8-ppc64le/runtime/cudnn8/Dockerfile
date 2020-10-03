ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.0-runtime-centos8
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 8.0.4.30
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN CUDNN_DOWNLOAD_SUM=55c6a64437a559eb1fdabcd1b176eb343030a9c18b92a0207328562a6b75e712 && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.4/RHEL8_1-ppc64le/libcudnn8-8.0.4.30-1.cuda11.0.ppc64le.rpm -O && \
    echo "$CUDNN_DOWNLOAD_SUM  libcudnn8-8.0.4.30-1.cuda11.0.ppc64le.rpm" | sha256sum -c - && \
    rpm -vih libcudnn8-8.0.4.30-1.cuda11.0.ppc64le.rpm && \
    rm -f libcudnn8-8.0.4.30-1.cuda11.0.ppc64le.rpm && \
    ldconfig
