ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.1-base-ubi8

LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV NCCL_VERSION 2.7

# setopt flag prevents yum from auto upgrading. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN /usr/bin/yum install --setopt=obsoletes=0 -y \
    cuda-libraries-$CUDA_PKG_VERSION \
    cuda-nvtx-$CUDA_PKG_VERSION \
    cuda-npp-$CUDA_PKG_VERSION \
    libcublas10-10.2.1.243-1 \
    && /usr/bin/yum clean all \
    && rm -rf /var/cache/yum/*

RUN /usr/bin/yum install -y xz && NCCL_DOWNLOAD_SUM=673535e03774aff57806fcc092b72b049e6303d48b8dfaafa3247a2b1c538ef6 \
    && curl -fsSL https://developer.download.nvidia.com/compute/redist/nccl/v2.7/nccl_2.7.8-1+cuda10.1_x86_64.txz -O \
    && echo "$NCCL_DOWNLOAD_SUM  nccl_2.7.8-1+cuda10.1_x86_64.txz" | sha256sum -c - \
    && unxz nccl_2.7.8-1+cuda10.1_x86_64.txz \
    && tar --no-same-owner --keep-old-files -xvf nccl_2.7.8-1+cuda10.1_x86_64.tar -C /usr/local/cuda/lib64/ --strip-components=2 --wildcards '*/lib/libnccl.so.*' \
    && tar --no-same-owner --keep-old-files -xvf  nccl_2.7.8-1+cuda10.1_x86_64.tar -C /usr/lib64/pkgconfig/ --strip-components=3 --wildcards '*/lib/pkgconfig/*' \
    && rm -f nccl_2.7.8-1+cuda10.1_x86_64.tar \
    && ldconfig \
    && /usr/bin/yum clean all \
    && rm -rf /var/cache/yum/*
