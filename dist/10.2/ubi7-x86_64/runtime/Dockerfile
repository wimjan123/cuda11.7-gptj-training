ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.2-base-ubi7

LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV NCCL_VERSION 2.7.6

RUN yum install -y \
    cuda-libraries-$CUDA_PKG_VERSION \
    cuda-nvtx-$CUDA_PKG_VERSION \
    cuda-npp-$CUDA_PKG_VERSION \
    libcublas10-10.2.2.89-1 \
    libnccl-2.7.6-1+cuda10.2 \
    && rm -rf /var/cache/yum/*

