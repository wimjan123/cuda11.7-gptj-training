## NVIDIA CUDA

[CUDA](https://developer.nvidia.com/cuda-zone) is a parallel computing platform and programming model developed by NVIDIA for general computing on graphical processing units (GPUs). With CUDA, developers can dramatically speed up computing applications by harnessing the power of GPUs.

The CUDA Toolkit from NVIDIA provides everything you need to develop GPU-accelerated applications. The CUDA Toolkit includes GPU-accelerated libraries, a compiler, development tools and the CUDA runtime.

The CUDA container images provide an easy-to-use distribution for CUDA supported platforms and architectures.

## Documentation

For more information on CUDA, including the release notes, programming model, APIs and developer tools, visit the [CUDA documentation site](https://docs.nvidia.com/cuda).

## Overview of Images

Three flavors of images are provided:
- `base`: Includes the CUDA runtime (cudart)
- `runtime`: Builds on the `base` and includes the [CUDA math libraries](https://developer.nvidia.com/gpu-accelerated-libraries), and [NCCL](https://developer.nvidia.com/nccl). A `runtime` image that also includes [cuDNN](https://developer.nvidia.com/cudnn) is available. 
- `devel`: Builds on the `runtime` and includes headers, development tools for building CUDA images. These images are particularly useful for multi-stage builds.

The Dockerfiles for the images are open-source and licensed under 3-clause BSD. For more information see the Supported Tags section below.

### End User License Agreements

The images are governed by the following NVIDIA End User License Agreements. By pulling and using the CUDA images, you accept the terms and conditions of these licenses. 
Since the images may include components licensed under open-source licenses such as GPL, the sources for these components are archived [here](https://developer.download.nvidia.com/compute/cuda/opensource/).

#### CUDA Toolkit EULA

To view the license for the CUDA Toolkit included in this image, click [*here*](http://docs.nvidia.com/cuda/eula/index.html)

#### cuDNN EULA

To view the license for the cuDNN Toolkit included in this image, click [*here*](https://docs.nvidia.com/deeplearning/sdk/cudnn-sla/index.html)

### NVIDIA Container Toolkit

The [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-docker) for Docker is required to run CUDA images.

For CUDA 10.0, `nvidia-docker2` (v2.1.0) or greater is recommended. It is also recommended to use Docker 19.03.

### How to report a problem

Read [NVIDIA Container Toolkit Frequently Asked Questions](https://github.com/NVIDIA/nvidia-docker/wiki/Frequently-Asked-Questions) to see if the problem has been encountered before.

After it has been determined the problem is not with the NVIDIA runtime, report an issue at the [CUDA Container Image Issue Tracker](https://gitlab.com/nvidia/container-images/cuda/-/issues).

## Supported tags

Supported tags are updated to the latest CUDA and cuDNN versions. These tags are also periodically updated to fix CVE vulnerabilities.

For a full list of supported tags, click [*here*](https://gitlab.com/nvidia/container-images/cuda/blob/master/doc/supported-tags.md).

## LATEST CUDA 11.0

Visit [OpenSource @ Nvidia](https://developer.download.nvidia.com/compute/cuda/opensource/image/11.0/) for the GPL sources of the packages contained in the CUDA base image layers.

### Ubuntu 18.04

- [`11.0-base`, `11.0-base-ubuntu18.04` (*11.0/ubuntu18.04-ppc64le/base/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.0/ubuntu18.04-ppc64le/base/Dockerfile)
- [`11.0-runtime`, `11.0-runtime-ubuntu18.04` (*11.0/ubuntu18.04-ppc64le/runtime/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.0/ubuntu18.04-ppc64le/runtime/Dockerfile)
- [`11.0-cudnn8-runtime`, `11.0-cudnn8-runtime-ubuntu18.04` (*11.0/ubuntu18.04-ppc64le/runtime/cudnn8/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.0/ubuntu18.04-ppc64le/runtime/cudnn8/Dockerfile)
- [`latest`, `11.0-devel`, `11.0-devel-ubuntu18.04` (*11.0/ubuntu18.04-ppc64le/devel/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.0/ubuntu18.04-ppc64le/devel/Dockerfile)
- [`11.0-cudnn8-devel`, `11.0-cudnn8-devel-ubuntu18.04` (*11.0/ubuntu18.04-ppc64le/devel/cudnn8/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.0/ubuntu18.04-ppc64le/devel/cudnn8/Dockerfile)

### RHEL8 based distros

CUDA images based on UBI 8 and CentOS 8 are not available due to known CVE vulnerabilities in these operating system images. We are working to address these issues ASAP.

### Unsupported tags

A list of tags that are no longer supported can be found [*here*](https://gitlab.com/nvidia/container-images/cuda/blob/master/doc/unsupported-tags.md)

### Source of this description

This [Readme](https://gitlab.com/nvidia/container-images/cuda/blob/master/doc/README.md) is located in the `doc` directory of the CUDA Container Image source repository. ([history](https://gitlab.com/nvidia/container-images/cuda/commits/master/doc/README.md))
