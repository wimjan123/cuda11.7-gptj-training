ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.4.0-runtime-ubuntu20.04

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

RUN apt-get update && apt-get install -y --no-install-recommends \
    libtinfo5 libncursesw5 \
    cuda-cudart-dev-11-4=11.4.43-1 \
    cuda-command-line-tools-11-4=11.4.0-1 \
    cuda-minimal-build-11-4=11.4.0-1 \
    cuda-libraries-dev-11-4=11.4.0-1 \
    cuda-nvml-dev-11-4=11.4.43-1 \
    libnpp-dev-11-4=11.4.0.33-1 \
    libcublas-dev-11-4=11.5.2.43-1 \
    libcusparse-dev-11-4=11.6.0.43-1 \
    && rm -rf /var/lib/apt/lists/*

# apt from auto upgrading the cublas package. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN apt-mark hold libcublas-dev-11-4
ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs