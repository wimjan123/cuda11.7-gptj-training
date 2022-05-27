ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.1.1-base-ubuntu16.04 as base

ENV NV_CUDA_LIB_VERSION 11.1.1-1

FROM base as base-amd64

ENV NV_NVTX_VERSION 11.1.74-1
ENV NV_LIBNPP_VERSION 11.1.2.301-1
ENV NV_LIBNPP_PACKAGE libnpp-11-1=${NV_LIBNPP_VERSION}
ENV NV_LIBCUSPARSE_VERSION 11.3.0.10-1

ENV NV_LIBCUBLAS_PACKAGE_NAME libcublas-11-1
ENV NV_LIBCUBLAS_VERSION 11.3.0.106-1
ENV NV_LIBCUBLAS_PACKAGE ${NV_LIBCUBLAS_PACKAGE_NAME}=${NV_LIBCUBLAS_VERSION}

ENV NV_LIBNCCL_PACKAGE_NAME libnccl2
ENV NV_LIBNCCL_PACKAGE_VERSION 2.7.8-1
ENV NCCL_VERSION 2.7.8-1
ENV NV_LIBNCCL_PACKAGE ${NV_LIBNCCL_PACKAGE_NAME}=${NV_LIBNCCL_PACKAGE_VERSION}+cuda11.1
ENV NV_LIBNCCL_PACKAGE_SHA256SUM 49ea52c9fbc40e050a89b93937c7c6c23f47c13da70c961cb04284c3225fe63e
ENV NV_LIBNCCL_PACKAGE_SOURCE https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64/libnccl2_2.7.8-1+cuda11.1_amd64.deb
ENV NV_LIBNCCL_PACKAGE_SOURCE_NAME libnccl2_2.7.8-1+cuda11.1_amd64.deb

RUN apt-get update && apt-get install -y --no-install-recommends wget

RUN wget -q ${NV_LIBNCCL_PACKAGE_SOURCE} \
    && echo "$NV_LIBNCCL_PACKAGE_SHA256SUM  ${NV_LIBNCCL_PACKAGE_SOURCE_NAME}" | sha256sum -c --strict - \
    && dpkg -i ${NV_LIBNCCL_PACKAGE_SOURCE_NAME} \
    && rm -f ${NV_LIBNCCL_PACKAGE_SOURCE_NAME} \
    && apt-get purge --autoremove -y wget \
    && rm -rf /var/lib/apt/lists/*


FROM base-${TARGETARCH}

ARG TARGETARCH

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-libraries-11-1=${NV_CUDA_LIB_VERSION} \
    ${NV_LIBNPP_PACKAGE} \
    cuda-nvtx-11-1=${NV_NVTX_VERSION} \
    libcusparse-11-1=${NV_LIBCUSPARSE_VERSION} \
    ${NV_LIBCUBLAS_PACKAGE} \
    ${NV_LIBNCCL_PACKAGE} \
    && rm -rf /var/lib/apt/lists/*

# Keep apt from auto upgrading the cublas and nccl packages. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN apt-mark hold ${NV_LIBCUBLAS_PACKAGE_NAME} ${NV_LIBNCCL_PACKAGE_NAME}