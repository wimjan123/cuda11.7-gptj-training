# syntax = docker/dockerfile:1.0-experimental

#
# Jetson TensorRT Test Dockerfile by jesusa
#
# DO NOT PUBLISH PUBLICLY
#
ARG IMAGE_NAME

FROM ${IMAGE_NAME}:10.2.460-cudnn8-runtime-ubuntu18.04-006 as builds

# TEMPORARY
RUN mkdir /builds
WORKDIR /builds

#RUN wget https://urm.nvidia.com/artifactory/sw-gpu-cuda-installer-generic-local/packaging/rel-8.0/tensorrt/linux-aarch64/l4t/8.0.0.1/cuda-10.2/tensorrt_8.0.0.1-1+cuda10.2_arm64.deb
# RUN wget https://urm.nvidia.com/artifactory/sw-gpu-cuda-installer-generic-local/packaging/rel-8.0/tensorrt/linux-aarch64/l4t/8.0.0.1/cuda-10.2/libnvinfer-samples_8.0.0-1+cuda10.2_all.deb
# RUN wget https://urm.nvidia.com/artifactory/sw-gpu-cuda-installer-generic-local/packaging/rel-8.0/tensorrt/linux-aarch64/l4t/8.0.0.1/cuda-10.2/libnvinfer-bin_8.0.0-1+cuda10.2_arm64.deb
# RUN wget https://urm.nvidia.com/artifactory/sw-gpu-cuda-installer-generic-local/packaging/rel-8.0/tensorrt/linux-aarch64/l4t/8.0.0.1/cuda-10.2/libnvinfer-doc_8.0.0-1+cuda10.2_all.deb
# RUN wget https://urm.nvidia.com/artifactory/sw-gpu-cuda-installer-generic-local/packaging/rel-8.0/tensorrt/linux-aarch64/l4t/8.0.0.1/cuda-10.2/libnvinfer-dev_8.0.0-1+cuda10.2_arm64.deb

RUN wget https://urm.nvidia.com/artifactory/sw-gpu-cuda-installer-generic-local/packaging/rel-8.0/tensorrt/linux-aarch64/l4t/8.0.0.3/cuda-10.2/onnx-graphsurgeon_8.0.0-1+cuda10.2_arm64.deb

# WAR until kitmaker handles trt wheels
# RUN wget http://cuda-repo.nvidia.com/release-candidates/Libraries/TensorRT/v8.0/8.0.0.1-e155eb70/10.2-r440/l4t-aarch64/tar/TensorRT-8.0.0.1.Ubuntu-18.04.aarch64-gnu.cuda-10.2.cudnn8.2.tar.gz
# RUN tar -xvzf ./TensorRT-8.0.0.1.Ubuntu-18.04.aarch64-gnu.cuda-10.2.cudnn8.2.tar.gz

# WAR need to get wheels labeled "arm64"
# RUN --mount=from=builds,source=/builds,target=/builds \
#     cp /builds/TensorRT-8.0.0.1/python/tensorrt-8.0.0.1-cp38-none-linux_aarch64.whl \
#        /builds/TensorRT-8.0.0.1/python/tensorrt-8.0.0.1-cp38-none-linux_arm64.whl

FROM ${IMAGE_NAME}:10.2.460-cudnn8-runtime-ubuntu18.04-006

ARG NVIDIA_TENSORRT_VERSION
ENV NVIDIA_TENSORRT_VERSION ${NVIDIA_TENSORRT_VERSION}

ARG PYVER=3.8
RUN if [ "$PYVER" = "3.8" ]; then DISTUTILS="python3-distutils"; fi

RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 curl ca-certificates && \
    curl -fsSL http://cuda-internal.nvidia.com/release-candidates/kitpicks/tensorrt-rel-8-0-tegra/8.0.0/001/repos/l4t/arm64/7fa2af80.pub | apt-key add - && \
    echo "deb http://cuda-internal.nvidia.com/release-candidates/kitpicks/tensorrt-rel-8-0-tegra/8.0.0/001/repos/l4t/arm64 /" > /etc/apt/sources.list.d/cuda.list && \
    apt-get update && apt-get install -y --no-install-recommends \
        gnupg2 curl ca-certificates \
        python$PYVER \
        $DISTUTILS \
        git \
        pkg-config \
        unzip

    # PYSFX=`echo "$PYVER" | cut -c1-1 || echo ""` \
        # python$PYSFX-pip \

# RUN --mount=from=builds,source=/builds,target=/builds \
#     find /builds/ -iname "*.whl"

# RUN --mount=from=builds,source=/builds,target=/builds \
#     ls -lh /builds/

RUN --mount=from=builds,source=/builds,target=/builds \
    apt install -f \
    libnvinfer8 \
    libnvinfer-plugin8 \
    libnvparsers8 \
    libnvonnxparsers8 \
    python3-libnvinfer \
    /builds/onnx-graphsurgeon_8.0.0-1+cuda10.2_arm64.deb

RUN rm -rf /var/lib/apt/lists/*

# # Download pybind11-2.2.3 required by some python samples
# RUN cd ${HOME} && \
#     git clone -b v2.2.3 https://github.com/pybind/pybind11.git

# Ensure "python" gets $PYVER version of python
RUN rm -f /usr/bin/python && ln -s /usr/bin/python$PYVER /usr/bin/python
RUN MAJ=`echo "$PYVER" | cut -c1-1` && \
    rm -f /usr/bin/python$MAJ && ln -s /usr/bin/python$PYVER /usr/bin/python$MAJ

RUN curl -O https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    rm get-pip.py

# RUN pip install --upgrade --no-cache-dir numpy \
#     && pip install --upgrade --no-cache-dir pycuda pillow

# jesusa: needed for onnx_graphsurgeon wheel install
# RUN apt update && apt install -f -y protobuf-compiler

# # jesusa: TEMPORARY WAR
# # FIXME: Get wheels from artifactory
# RUN --mount=from=builds,source=/builds,target=/builds \
#     export PY=$(python -c 'import sys; print(str(sys.version_info[0])+str(sys.version_info[1]))') \
#     && pip install \
#         /builds/TensorRT-8.0.0.1/graphsurgeon/graphsurgeon-0.4.5-py2.py3-none-any.whl \
#         /builds/TensorRT-8.0.0.1/python/tensorrt-8.0.0.1-cp${PY}-none-linux_aarch64.whl \
#         /builds/TensorRT-8.0.0.1/uff/uff-0.6.9-py2.py3-none-any.whl \
#         /builds/TensorRT-8.0.0.1/onnx_graphsurgeon/onnx_graphsurgeon-0.2.6-py2.py3-none-any.whl

# # Install Polygraphy
# RUN pip install --no-cache-dir \
#     --extra-index-url https://pypi.ngc.nvidia.com \
#     --extra-index-url https://tensorrt-read-only:Tensorrt\@123@urm.nvidia.com/artifactory/api/pypi/sw-tensorrt-pypi/simple \
#     polygraphy

COPY NGC-DL-CONTAINER-LICENSE /
