ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.4.0-base-ubuntu20.04

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

ENV NCCL_VERSION 2.10.3

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-libraries-11-4=11.4.0-1 \
    libnpp-11-4=11.4.0.33-1 \
    cuda-nvtx-11-4=11.4.43-1 \
    libcublas-11-4=11.5.2.43-1 \
    libcusparse-11-4=11.6.0.43-1 \
    libnccl2=$NCCL_VERSION-1+cuda11.4 \
    && rm -rf /var/lib/apt/lists/*

# apt from auto upgrading the cublas package. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN apt-mark hold libcublas-11-4 libnccl2
