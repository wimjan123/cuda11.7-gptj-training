ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.0-runtime-centos7-rc
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 8.0.0.180
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN CUDNN_DOWNLOAD_SUM=b526e21b82ea4ba3fed4864d626ae3ce4474381c38bd733e3f1e869d8fc46f4b && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.0/RHEL7_3-x64/libcudnn8-8.0.0.180-1.cuda11.0.x86_64.rpm -O && \
    echo "$CUDNN_DOWNLOAD_SUM  libcudnn8-8.0.0.180-1.cuda11.0.x86_64.rpm" | sha256sum -c - && \
    rpm -vih libcudnn8-8.0.0.180-1.cuda11.0.x86_64.rpm && \
    rm -f libcudnn8-8.0.0.180-1.cuda11.0.x86_64.rpm && \
    ldconfig
