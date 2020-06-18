ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.2-devel-centos7
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 8.0.0.180
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN CUDNN_DOWNLOAD_SUM=c1c918e022bd9da19d0d74a773c4f4e57552b9cd128d2639020e01c68a7a2e4e && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.0/RHEL7_3-ppc64le/libcudnn8-8.0.0.180-1.cuda10.2.ppc64le.rpm -O && \
    echo "$CUDNN_DOWNLOAD_SUM  libcudnn8-8.0.0.180-1.cuda10.2.ppc64le.rpm" | sha256sum -c - && \
    rpm -vih libcudnn8-8.0.0.180-1.cuda10.2.ppc64le.rpm && \
    rm -f libcudnn8-8.0.0.180-1.cuda10.2.ppc64le.rpm && \
    ldconfig
