ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.3.1-runtime-centos8

LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV NCCL_VERSION 2.9.9

RUN yum install -y \
    make \
    cuda-command-line-tools-11-3-11.3.1-1 \
    cuda-libraries-devel-11-3-11.3.1-1 \
    cuda-minimal-build-11-3-11.3.1-1 \
    cuda-cudart-devel-11-3-11.3.109-1 \
    cuda-nvprof-11-3-11.3.111-1 \
    cuda-nvml-devel-11-3-11.3.58-1 \
    libcublas-devel-11-3-11.5.1.109-1 \
    libnpp-devel-11-3-11.3.3.95-1 \
    libnccl-devel-2.9.9-1+cuda11.3 \
    && yum clean all \
    && rm -rf /var/cache/yum/*

ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs