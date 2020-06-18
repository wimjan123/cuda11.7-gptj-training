ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.2-base-ubi8

LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

RUN yum install -y \
    cuda-libraries-$CUDA_PKG_VERSION \
    cuda-nvtx-$CUDA_PKG_VERSION \
    libcublas10-10.2.2.89-1 \
    && rm -rf /var/cache/yum/*

RUN yum install -y xz && NCCL_DOWNLOAD_SUM=a9ee790c3fc64b0ecbb00db92eddc1525552eda10a8656ff4b7380f66d81bda1 && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/nccl/v2.7/nccl_2.7.3-1+cuda10.2_x86_64.txz -O && \
    echo "$NCCL_DOWNLOAD_SUM  nccl_2.7.3-1+cuda10.2_x86_64.txz" | sha256sum -c - && \
    unxz nccl_2.7.3-1+cuda10.2_x86_64.txz && \
    tar --no-same-owner -xvf nccl_2.7.3-1+cuda10.2_x86_64.tar -C /usr/local/cuda/lib64/ --strip-components=2 --wildcards '*/lib/libnccl.so.*' && \
    tar --no-same-owner -xvf  nccl_2.7.3-1+cuda10.2_x86_64.tar -C /usr/lib64/pkgconfig/ --strip-components=3 --wildcards '*/lib/pkgconfig/*' && \
    rm -f nccl_2.7.3-1+cuda10.2_x86_64.tar && \
    ldconfig
