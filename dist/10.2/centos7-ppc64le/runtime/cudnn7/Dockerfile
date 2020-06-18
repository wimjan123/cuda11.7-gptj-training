ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.2-runtime-centos7
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 7.6.5.32
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

# cuDNN license: https://developer.nvidia.com/cudnn/license_agreement
RUN CUDNN_DOWNLOAD_SUM=7dc08b6ab9331bfd12207d4802c61db1ad7cace7395b67a6e7b16efa0335668b && \
    curl -fsSL http://developer.download.nvidia.com/compute/redist/cudnn/v7.6.5/cudnn-10.2-linux-ppc64le-v7.6.5.32.tgz -O && \
    echo "$CUDNN_DOWNLOAD_SUM  cudnn-10.2-linux-ppc64le-v7.6.5.32.tgz" | sha256sum -c - && \
    tar --no-same-owner -xzf cudnn-10.2-linux-ppc64le-v7.6.5.32.tgz -C /usr/local --wildcards 'cuda/targets/ppc64le-linux/lib/libcudnn.so.*' && \
    rm cudnn-10.2-linux-ppc64le-v7.6.5.32.tgz && \
    ldconfig
