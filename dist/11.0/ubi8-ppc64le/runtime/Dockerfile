ARG IMAGE_NAME
FROM ${IMAGE_NAME}:11.0-base-ubi8-rc

LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

RUN yum install -y \
    cuda-libraries-11-0-11.0.1-1 \
    cuda-nvtx-11-0-11.0.167-1 \
    && rm -rf /var/cache/yum/*

RUN yum install -y xz && NCCL_DOWNLOAD_SUM=8486ac373c246f2468c55788597da2eb3b195f5fcdfaf4c3832c78c2849207ee && \
    curl -fsSL https://developer.download.nvidia.com/compute/redist/nccl/v2.7/nccl_2.7.3-1+cuda11.0_ppc64le.txz -O && \
    echo "$NCCL_DOWNLOAD_SUM  nccl_2.7.3-1+cuda11.0_ppc64le.txz" | sha256sum -c - && \
    unxz nccl_2.7.3-1+cuda11.0_ppc64le.txz && \
    tar --no-same-owner -xvf nccl_2.7.3-1+cuda11.0_ppc64le.tar -C /usr/local/cuda/lib64/ --strip-components=2 --wildcards '*/lib/libnccl.so.*' && \
    tar --no-same-owner -xvf  nccl_2.7.3-1+cuda11.0_ppc64le.tar -C /usr/lib64/pkgconfig/ --strip-components=3 --wildcards '*/lib/pkgconfig/*' && \
    rm -f nccl_2.7.3-1+cuda11.0_ppc64le.tar && \
    ldconfig
