ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.2-runtime-centos7
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 8.0.1.13
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN CUDNN_DOWNLOAD_SUM=8eb2eb2b84fe970dd44194c76d6c9208ca971c13e07e48a755af11cb8a52be93 && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.1/RHEL7_3-x64/libcudnn8-8.0.1.13-1.cuda10.2.x86_64.rpm -O && \
    echo "$CUDNN_DOWNLOAD_SUM  libcudnn8-8.0.1.13-1.cuda10.2.x86_64.rpm" | sha256sum -c - && \
    rpm -vih libcudnn8-8.0.1.13-1.cuda10.2.x86_64.rpm && \
    rm -f libcudnn8-8.0.1.13-1.cuda10.2.x86_64.rpm && \
    ldconfig
