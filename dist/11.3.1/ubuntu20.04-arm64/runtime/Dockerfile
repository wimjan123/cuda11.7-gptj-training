ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.3.1-base-ubuntu20.04

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"


ENV NCCL_VERSION 2.9.9

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-libraries-11-3=11.3.1-1 \
    libnpp-11-3=11.3.3.95-1 \
    cuda-nvtx-11-3=11.3.109-1 \
    libcublas-11-3=11.5.1.109-1 \
    libcusparse-11-3=11.6.0.109-1 \
    libnccl2=$NCCL_VERSION-1+cuda11.3 \
    && rm -rf /var/lib/apt/lists/*

# apt from auto upgrading the cublas package. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN apt-mark hold libcublas-11-3 libnccl2
