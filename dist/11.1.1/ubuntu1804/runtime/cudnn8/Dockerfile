ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.1.1-runtime-ubuntu18.04 as base

FROM base as base-amd64

ENV NV_CUDNN_VERSION 8.0.5.39
ENV NV_CUDNN_PACKAGE_NAME "libcudnn8"

ENV NV_CUDNN_PACKAGE "libcudnn8=$NV_CUDNN_VERSION-1+cuda11.1"

FROM base as base-arm64

ENV NV_CUDNN_VERSION 8.0.5.39
ENV NV_CUDNN_PACKAGE_NAME "libcudnn8"

ENV NV_CUDNN_PACKAGE "libcudnn8=$NV_CUDNN_VERSION-1+cuda11.1"

FROM base as base-ppc64le

ENV NV_CUDNN_VERSION 8.0.4.30
ENV NV_CUDNN_PACKAGE_NAME "libcudnn8"

ENV NV_CUDNN_PACKAGE "libcudnn8=$NV_CUDNN_VERSION-1+cuda11.1"

ENV NV_CUDNN_DL_HASHCMD sha256sum
ENV NV_CUDNN_DL_SUM 2779c07458fc4ae690070decf59cfcb3ec9a67607f9a26819f1631e661961ccb
ENV NV_CUDNN_DL_BASENAME libcudnn8_8.0.4.30-1+cuda11.1_ppc64el.deb
ENV NV_CUDNN_DL_URL https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/ppc64el/libcudnn8_8.0.4.30-1+cuda11.1_ppc64el.deb

RUN apt-get update && apt-get install -y --no-install-recommends wget

RUN wget -q ${NV_CUDNN_DL_URL} \
    && echo "${NV_CUDNN_DL_SUM}  ${NV_CUDNN_DL_BASENAME}" | ${NV_CUDNN_DL_HASHCMD} -c - \
    && dpkg -i ${NV_CUDNN_DL_BASENAME} \
    && rm -f ${NV_CUDNN_DL_BASENAME} \
    && apt-get purge --autoremove -y wget

FROM base-${TARGETARCH}

ARG TARGETARCH

LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"
LABEL com.nvidia.cudnn.version="${NV_CUDNN_VERSION}"

