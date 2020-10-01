ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.0-devel-centos8
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 8.0.4.30
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN CUDNN_DOWNLOAD_SUM=caf0364d1a2466eb47028992aa12f9f119bf94e4e6da3a997e781b6e03106f99 && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.4/RHEL8_1-ppc64le/libcudnn8-8.0.4.30-1.cuda11.0.x86_64.rpm -O && \
    echo "$CUDNN_DOWNLOAD_SUM  libcudnn8-8.0.4.30-1.cuda11.0.x86_64.rpm" | sha256sum -c - && \
    rpm -vih libcudnn8-8.0.4.30-1.cuda11.0.x86_64.rpm && \
    rm -f libcudnn8-8.0.4.30-1.cuda11.0.x86_64.rpm && \
    ldconfig

RUN CUDNN_DOWNLOAD_SUM=d1287669c2a777b49da1a7610c584cdb23c41680e7b76296002bcde0b79fde52 && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.4/RHEL8_1-ppc64le/libcudnn8-devel-8.0.4.30-1.cuda11.0.x86_64.rpm -O && \
    echo "$CUDNN_DOWNLOAD_SUM  libcudnn8-devel-8.0.4.30-1.cuda11.0.x86_64.rpm" | sha256sum -c - && \
    rpm -vih libcudnn8-devel-8.0.4.30-1.cuda11.0.x86_64.rpm && \
    rm -f libcudnn8-devel-8.0.4.30-1.cuda11.0.x86_64.rpm && \
    ldconfig
