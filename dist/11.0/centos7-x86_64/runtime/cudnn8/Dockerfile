ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.0-runtime-centos7
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 8.0.1.13
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN CUDNN_DOWNLOAD_SUM=073ead51ecb78b073130dcc850029a6e1f43fb81da568d03ea47cdf84f31f3a1 && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.1/RHEL7_3-x64/libcudnn8-8.0.1.13-1.cuda11.0.x86_64.rpm -O && \
    echo "$CUDNN_DOWNLOAD_SUM  libcudnn8-8.0.1.13-1.cuda11.0.x86_64.rpm" | sha256sum -c - && \
    rpm -vih libcudnn8-8.0.1.13-1.cuda11.0.x86_64.rpm && \
    rm -f libcudnn8-8.0.1.13-1.cuda11.0.x86_64.rpm && \
    ldconfig
