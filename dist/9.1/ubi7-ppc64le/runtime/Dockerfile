ARG IMAGE_NAME
FROM ${IMAGE_NAME}:9.1-base-ubi7

LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

RUN /usr/bin/yum install -y \
    cuda-libraries-$CUDA_PKG_VERSION \
    && /usr/bin/yum clean all \
    && rm -rf /var/cache/yum/*

