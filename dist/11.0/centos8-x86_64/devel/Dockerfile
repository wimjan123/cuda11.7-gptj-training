ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.0-runtime-centos8-rc

LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

RUN yum install -y \
    cuda-nvml-devel-11-0-11.0.167-1 \
    cuda-command-line-tools-11-0-11.0.1-1 \
    cuda-cudart-devel-11-0-11.0.171-1 \
    cuda-libraries-devel-11-0-11.0.1-1 \
    cuda-minimal-build-11-0-11.0.1-1 \
    libcublas-devel-11-0-11.0.0.191-1 \
    && rm -rf /var/cache/yum/*

RUN yum install -y xz && NCCL_DOWNLOAD_SUM=d112b722bf557cff96d571ac3386e4f539be7b3e9412561bde59b0ad6e59263d && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/nccl/v2.7/nccl_2.7.3-1+cuda11.0_x86_64.txz -O && \
    echo "$NCCL_DOWNLOAD_SUM  nccl_2.7.3-1+cuda11.0_x86_64.txz" | sha256sum -c - && \
    unxz nccl_2.7.3-1+cuda11.0_x86_64.txz && \
    tar --no-same-owner -xvf  nccl_2.7.3-1+cuda11.0_x86_64.tar -C /usr/local/cuda/include/ --strip-components=2 --wildcards '*/include/*' && \
    tar --no-same-owner -xvf  nccl_2.7.3-1+cuda11.0_x86_64.tar -C /usr/local/cuda/lib64/ --strip-components=2 --wildcards '*/lib/libnccl.so' && \
    rm -f nccl_2.7.3-1+cuda11.0_x86_64.tar && \
    ldconfig

ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs