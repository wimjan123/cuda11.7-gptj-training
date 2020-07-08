ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.2-runtime-centos8
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 8.0.1.13
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

# cuDNN license: https://developer.nvidia.com/cudnn/license_agreement
RUN CUDNN_DOWNLOAD_SUM=03cbe5844ff01b3550ba5d0bbf6eab1c33630f18669978af2a7ebf7366a5c442 && \
    curl -fsSL http://developer.download.nvidia.com/compute/redist/cudnn/v8.0.1/cudnn-10.2-linux-x64-v8.0.1.13.tgz -O && \
    echo "$CUDNN_DOWNLOAD_SUM  cudnn-10.2-linux-x64-v8.0.1.13.tgz" | sha256sum -c - && \
    tar --no-same-owner -xzf cudnn-10.2-linux-x64-v8.0.1.13.tgz -C /usr/local --wildcards 'cuda/lib64/libcudnn.so.*' && \
    rm cudnn-10.2-linux-x64-v8.0.1.13.tgz && \
    ldconfig
