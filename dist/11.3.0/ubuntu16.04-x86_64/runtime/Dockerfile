ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.3.0-base-ubuntu16.04

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"


RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-libraries-11-3=11.3.0-1 \
    libnpp-11-3=11.3.3.44-1 \
    cuda-nvtx-11-3=11.3.58-1 \
    libcublas-11-3=11.4.2.10064-1 \
    libcusparse-11-3=11.5.0.58-1 \
    && rm -rf /var/lib/apt/lists/*

# apt from auto upgrading the cublas package. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN apt-mark hold libcublas-11-3
