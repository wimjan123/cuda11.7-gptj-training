ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.0.3-runtime-centos7 as base

FROM base as base-amd64

ENV NV_CUDA_LIB_VERSION "11.0.3-1"
ENV NV_NVPROF_VERSION "11.0.221-1"
ENV NV_CUDA_RUNTIME_VERSION_DEV "11.0.221-1"
ENV NV_NVML_VERSION_DEV "11.0.167-1"
ENV NV_CUBLAS_VERSION_DEV "11.2.0.252-1"
ENV NV_LIBNPP_VERSION_DEV "11.1.0.245-1"
ENV NCCL_VERSION 2.10.3
ENV NV_LIBNCCL_PACKAGE_DEV "libnccl-devel-2.10.3-1+cuda11.0"



FROM base-${TARGETARCH}

ARG TARGETARCH

LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

RUN yum install -y \
    make \
    cuda-command-line-tools-11-0-${NV_CUDA_LIB_VERSION} \
    cuda-libraries-devel-11-0-${NV_CUDA_LIB_VERSION} \
    cuda-minimal-build-11-0-${NV_CUDA_LIB_VERSION} \
    cuda-cudart-devel-11-0-${NV_CUDA_RUNTIME_VERSION_DEV} \
    cuda-nvprof-11-0-${NV_NVPROF_VERSION} \
    cuda-nvml-devel-11-0-${NV_NVML_VERSION_DEV} \
    libcublas-devel-11-0-${NV_CUBLAS_VERSION_DEV} \
    libnpp-devel-11-0-${NV_LIBNPP_VERSION_DEV} \
    ${NV_LIBNCCL_PACKAGE_DEV} \
    && yum clean all \
    && rm -rf /var/cache/yum/*


ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs