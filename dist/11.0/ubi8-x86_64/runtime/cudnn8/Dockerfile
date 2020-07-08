ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.0-runtime-ubi8
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 8.0.1.13
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN CUDNN_DOWNLOAD_SUM=29c6dc2a4301689dfcb9ff1b25caa171d38ce4c9e26b0f3171265e7efa561d15 && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.1/RHEL8_1-x64/libcudnn8-8.0.1.13-1.cuda11.0.x86_64.rpm -O && \
    echo "$CUDNN_DOWNLOAD_SUM  libcudnn8-8.0.1.13-1.cuda11.0.x86_64.rpm" | sha256sum -c - && \
    rpm -vih libcudnn8-8.0.1.13-1.cuda11.0.x86_64.rpm && \
    rm -f libcudnn8-8.0.1.13-1.cuda11.0.x86_64.rpm && \
    ldconfig
