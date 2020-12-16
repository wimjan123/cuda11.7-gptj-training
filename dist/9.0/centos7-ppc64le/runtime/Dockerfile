ARG IMAGE_NAME
FROM ${IMAGE_NAME}:9.0-base-centos7

LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

RUN /usr/bin/yum install -y \
    cuda-libraries-$CUDA_PKG_VERSION \
    cuda-cublas-9-0=9.0.176.4-1 \
    && /usr/bin/yum clean all \
    && rm -rf /var/cache/yum/*

