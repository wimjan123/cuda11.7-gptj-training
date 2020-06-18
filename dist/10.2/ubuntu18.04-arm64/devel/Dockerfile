ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.2-runtime-ubuntu18.04

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-nvml-dev-$CUDA_PKG_VERSION \
    cuda-command-line-tools-10-2=10.2.20200604-1 \
    libnpp-dev-10-2=10.2.1.184-1 \
    cuda-libraries-dev-10-2=10.2.20200604-1 \
    cuda-minimal-build-10-2=10.2.20200604-1 \
    && rm -rf /var/lib/apt/lists/*


ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs