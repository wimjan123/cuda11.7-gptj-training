
ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.2.2-runtime-ubuntu20.04

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

ENV NCCL_VERSION 2.8.4

RUN apt-get update && apt-get install -y --no-install-recommends \
    libtinfo5 libncursesw5 \
    cuda-cudart-dev-11-2=11.2.152-1 \
    cuda-command-line-tools-11-2=11.2.2-1 \
    cuda-minimal-build-11-2=11.2.2-1 \
    cuda-libraries-dev-11-2=11.2.2-1 \
    cuda-nvml-dev-11-2=11.2.152-1 \
    libnpp-dev-11-2=11.3.2.152-1 \
    libnccl-dev=2.8.4-1+cuda11.2 \
    libcublas-dev-11-2=11.4.1.1043-1 \
    libcusparse-dev-11-2=11.4.1.1152-1 \
    && rm -rf /var/lib/apt/lists/*

# apt from auto upgrading the cublas package. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN apt-mark hold libcublas-dev-11-2 libnccl-dev
ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs