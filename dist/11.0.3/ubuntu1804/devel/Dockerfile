ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.0.3-runtime-ubuntu18.04 as base

ENV NV_CUDA_LIB_VERSION "11.0.3-1"

FROM base as base-amd64

ENV NV_CUDA_CUDART_DEV_VERSION 11.0.221-1
ENV NV_NVML_DEV_VERSION 11.0.167-1
ENV NV_LIBCUSPARSE_DEV_VERSION 11.1.1.245-1
ENV NV_LIBNPP_DEV_VERSION 11.1.0.245-1
ENV NV_LIBNPP_DEV_PACKAGE libnpp-dev-11-0=${NV_LIBNPP_DEV_VERSION}

ENV NV_LIBCUBLAS_DEV_VERSION 11.2.0.252-1
ENV NV_LIBCUBLAS_DEV_PACKAGE_NAME libcublas-dev-11-0
ENV NV_LIBCUBLAS_DEV_PACKAGE ${NV_LIBCUBLAS_DEV_PACKAGE_NAME}=${NV_LIBCUBLAS_DEV_VERSION}

ENV NV_NVPROF_VERSION 11.0.221-1
ENV NV_NVPROF_DEV_PACKAGE cuda-nvprof-11-0=${NV_NVPROF_VERSION}

ENV NV_LIBNCCL_DEV_PACKAGE_NAME libnccl-dev
ENV NV_LIBNCCL_DEV_PACKAGE_VERSION 2.15.5-1
ENV NCCL_VERSION 2.15.5-1
ENV NV_LIBNCCL_DEV_PACKAGE ${NV_LIBNCCL_DEV_PACKAGE_NAME}=${NV_LIBNCCL_DEV_PACKAGE_VERSION}+cuda11.0
FROM base as base-arm64

ENV NV_CUDA_CUDART_DEV_VERSION 11.0.221-1
ENV NV_NVML_DEV_VERSION 11.0.167-1
ENV NV_LIBCUSPARSE_DEV_VERSION 11.1.1.245-1
ENV NV_LIBNPP_DEV_VERSION 11.1.0.245-1
ENV NV_LIBNPP_DEV_PACKAGE libnpp-dev-11-0=${NV_LIBNPP_DEV_VERSION}

ENV NV_LIBCUBLAS_DEV_PACKAGE_NAME libcublas-dev-11-0
ENV NV_LIBCUBLAS_DEV_VERSION 11.2.0.252-1
ENV NV_LIBCUBLAS_DEV_PACKAGE ${NV_LIBCUBLAS_DEV_PACKAGE_NAME}=${NV_LIBCUBLAS_DEV_VERSION}

ENV NV_NVPROF_VERSION 11.0.221-1
ENV NV_NVPROF_DEV_PACKAGE cuda-nvprof-11-0=${NV_NVPROF_VERSION}

ENV NV_LIBNCCL_DEV_PACKAGE_NAME libnccl-dev
ENV NV_LIBNCCL_DEV_PACKAGE_VERSION 2.8.3-1
ENV NCCL_VERSION 2.8.3-1
ENV NV_LIBNCCL_DEV_PACKAGE ${NV_LIBNCCL_DEV_PACKAGE_NAME}=${NV_LIBNCCL_DEV_PACKAGE_VERSION}+cuda11.0
ENV NV_LIBNCCL_PACKAGE_SHA256SUM 7157c77a5593cfd4e0c600308a336a8087c067ce09ebf170493a1f516dd42a44
ENV NV_LIBNCCL_PACKAGE_SOURCE https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/sbsa/libnccl2_2.8.3-1+cuda11.0_arm64.deb
ENV NV_LIBNCCL_PACKAGE_SOURCE_NAME libnccl2_2.8.3-1+cuda11.0_arm64.deb

RUN apt-get update && apt-get install -y --no-install-recommends wget

RUN wget -q ${NV_LIBNCCL_PACKAGE_SOURCE} \
    && echo "$NV_LIBNCCL_PACKAGE_SHA256SUM  ${NV_LIBNCCL_PACKAGE_SOURCE_NAME}" | sha256sum -c --strict - \
    && dpkg -i ${NV_LIBNCCL_PACKAGE_SOURCE_NAME} \
    && rm -f ${NV_LIBNCCL_PACKAGE_SOURCE_NAME} \
    && apt-get purge --autoremove -y wget \
    && rm -rf /var/lib/apt/lists/*

ENV NV_LIBNCCL_DEV_PACKAGE_SHA256SUM e8fe10aa2dd8c54d97ecc6f3b92cef1e7243af07a03f8d7a18f49c4c90b8102e
ENV NV_LIBNCCL_DEV_PACKAGE_SOURCE https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/sbsa/libnccl-dev_2.8.3-1+cuda11.0_arm64.deb
ENV NV_LIBNCCL_DEV_PACKAGE_SOURCE_NAME libnccl-dev_2.8.3-1+cuda11.0_arm64.deb
RUN apt-get update && apt-get install -y --no-install-recommends wget

RUN wget -q ${NV_LIBNCCL_DEV_PACKAGE_SOURCE} \
    && echo "$NV_LIBNCCL_DEV_PACKAGE_SHA256SUM  ${NV_LIBNCCL_DEV_PACKAGE_SOURCE_NAME}" | sha256sum -c --strict - \
    && dpkg -i ${NV_LIBNCCL_DEV_PACKAGE_SOURCE_NAME} \
    && rm -f ${NV_LIBNCCL_DEV_PACKAGE_SOURCE_NAME} \
    && apt-get purge --autoremove -y wget \
    && rm -rf /var/lib/apt/lists/*

FROM base as base-ppc64le

ENV NV_CUDA_CUDART_DEV_VERSION 11.0.221-1
ENV NV_NVML_DEV_VERSION 11.0.167-1
ENV NV_LIBCUSPARSE_DEV_VERSION 11.1.1.245-1
ENV NV_LIBNPP_DEV_VERSION 11.1.0.245-1
ENV NV_LIBNPP_DEV_PACKAGE libnpp-dev-11-0=${NV_LIBNPP_DEV_VERSION}

ENV NV_LIBCUBLAS_DEV_VERSION 11.2.0.252-1
ENV NV_LIBCUBLAS_DEV_PACKAGE_NAME libcublas-dev-11-0
ENV NV_LIBCUBLAS_DEV_PACKAGE ${NV_LIBCUBLAS_DEV_PACKAGE_NAME}=${NV_LIBCUBLAS_DEV_VERSION}

ENV NV_NVPROF_VERSION 11.0.221-1
ENV NV_NVPROF_DEV_PACKAGE cuda-nvprof-11-0=${NV_NVPROF_VERSION}

ENV NV_LIBNCCL_DEV_PACKAGE_NAME libnccl-dev
ENV NV_LIBNCCL_DEV_PACKAGE_VERSION 2.8.3-1
ENV NCCL_VERSION 2.8.3-1
ENV NV_LIBNCCL_DEV_PACKAGE ${NV_LIBNCCL_DEV_PACKAGE_NAME}=${NV_LIBNCCL_DEV_PACKAGE_VERSION}+cuda11.0
ENV NV_LIBNCCL_PACKAGE_SHA256SUM 6f804cb32a6a4e83c46b60ea0f88160d0a11f6b965855bab55a106de73d3358c
ENV NV_LIBNCCL_PACKAGE_SOURCE https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/ppc64el/libnccl2_2.8.3-1+cuda11.0_ppc64el.deb
ENV NV_LIBNCCL_PACKAGE_SOURCE_NAME libnccl2_2.8.3-1+cuda11.0_ppc64el.deb

RUN apt-get update && apt-get install -y --no-install-recommends wget

RUN wget -q ${NV_LIBNCCL_PACKAGE_SOURCE} \
    && echo "$NV_LIBNCCL_PACKAGE_SHA256SUM  ${NV_LIBNCCL_PACKAGE_SOURCE_NAME}" | sha256sum -c --strict - \
    && dpkg -i ${NV_LIBNCCL_PACKAGE_SOURCE_NAME} \
    && rm -f ${NV_LIBNCCL_PACKAGE_SOURCE_NAME} \
    && apt-get purge --autoremove -y wget \
    && rm -rf /var/lib/apt/lists/*

ENV NV_LIBNCCL_DEV_PACKAGE_SHA256SUM 3d694a41a11f9f76b22709ac0533db306604e8a2473a71aca8280e8cf7c9f152
ENV NV_LIBNCCL_DEV_PACKAGE_SOURCE https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/ppc64el/libnccl-dev_2.8.3-1+cuda11.0_ppc64el.deb
ENV NV_LIBNCCL_DEV_PACKAGE_SOURCE_NAME libnccl-dev_2.8.3-1+cuda11.0_ppc64el.deb

RUN apt-get update && apt-get install -y --no-install-recommends wget

RUN wget -q ${NV_LIBNCCL_DEV_PACKAGE_SOURCE} \
    && echo "$NV_LIBNCCL_DEV_PACKAGE_SHA256SUM  ${NV_LIBNCCL_DEV_PACKAGE_SOURCE_NAME}" | sha256sum -c --strict - \
    && dpkg -i ${NV_LIBNCCL_DEV_PACKAGE_SOURCE_NAME} \
    && rm -f ${NV_LIBNCCL_DEV_PACKAGE_SOURCE_NAME} \
    && apt-get purge --autoremove -y wget \
    && rm -rf /var/lib/apt/lists/*


FROM base-${TARGETARCH}

ARG TARGETARCH

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-cudart-dev-11-0=${NV_CUDA_CUDART_DEV_VERSION} \
    cuda-command-line-tools-11-0=${NV_CUDA_LIB_VERSION} \
    cuda-minimal-build-11-0=${NV_CUDA_LIB_VERSION} \
    cuda-libraries-dev-11-0=${NV_CUDA_LIB_VERSION} \
    cuda-nvml-dev-11-0=${NV_NVML_DEV_VERSION} \
    ${NV_NVPROF_DEV_PACKAGE} \
    ${NV_LIBNPP_DEV_PACKAGE} \
    libcusparse-dev-11-0=${NV_LIBCUSPARSE_DEV_VERSION} \
    ${NV_LIBCUBLAS_DEV_PACKAGE} \
    ${NV_LIBNCCL_DEV_PACKAGE} \
    && rm -rf /var/lib/apt/lists/*

# Keep apt from auto upgrading the cublas and nccl packages. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN apt-mark hold ${NV_LIBCUBLAS_DEV_PACKAGE_NAME} ${NV_LIBNCCL_DEV_PACKAGE_NAME}
ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs
