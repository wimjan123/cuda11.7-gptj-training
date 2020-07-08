ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.0-devel-ubi8
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 8.0.1.13
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN CUDNN_DOWNLOAD_SUM=c4f4c2aa35ed4caf5b8d2e31cae685a0846923d9e53882418851139b7b219835 && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.1/RHEL8_1-ppc64le/libcudnn8-8.0.1.13-1.cuda11.0.ppc64le.rpm -O && \
    echo "$CUDNN_DOWNLOAD_SUM  libcudnn8-8.0.1.13-1.cuda11.0.ppc64le.rpm" | sha256sum -c - && \
    rpm -vih libcudnn8-8.0.1.13-1.cuda11.0.ppc64le.rpm && \
    rm -f libcudnn8-8.0.1.13-1.cuda11.0.ppc64le.rpm && \
    ldconfig

RUN CUDNN_DOWNLOAD_SUM=7b22588c56cea5e31f9ecf7c5097e7e7e614d5ceb3c1764a1e7294af799c6350 && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/cudnn/v8.0.1/RHEL8_1-ppc64le/libcudnn8-devel-8.0.1.13-1.cuda11.0.ppc64le.rpm -O && \
    echo "$CUDNN_DOWNLOAD_SUM  libcudnn8-devel-8.0.1.13-1.cuda11.0.ppc64le.rpm" | sha256sum -c - && \
    rpm -vih libcudnn8-devel-8.0.1.13-1.cuda11.0.ppc64le.rpm && \
    rm -f libcudnn8-devel-8.0.1.13-1.cuda11.0.ppc64le.rpm && \
    ldconfig
