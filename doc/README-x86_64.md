## NVIDIA CUDA

[CUDA](https://developer.nvidia.com/cuda-zone) is a parallel computing platform and programming model developed by NVIDIA for general computing on graphical processing units (GPUs). With CUDA, developers can dramatically speed up computing applications by harnessing the power of GPUs.

The CUDA Toolkit from NVIDIA provides everything you need to develop GPU-accelerated applications. The CUDA Toolkit includes GPU-accelerated libraries, a compiler, development tools and the CUDA runtime.

The CUDA container images provide an easy-to-use distribution for CUDA supported platforms and architectures.

## End User License Agreements

The images are governed by the following NVIDIA End User License Agreements. By pulling and using the CUDA images, you accept the terms and conditions of these licenses.
Since the images may include components licensed under open-source licenses such as GPL, the sources for these components are archived [here](https://developer.download.nvidia.com/compute/cuda/opensource/image).

### NVIDIA Deep learning Container License

To view the NVIDIA Deep Learning Container license, click [here](https://developer.nvidia.com/ngc/nvidia-deep-learning-container-license)

## Documentation

For more information on CUDA, including the release notes, programming model, APIs and developer tools, visit the [CUDA documentation site](https://docs.nvidia.com/cuda).

## Announcement

### End-of-life for nvdia/cuda-arm64 and nvidia/cuda-ppc64le images names in place of Multi-arch image Manifests

For an upcoming release of Cuda Toolkit, support for the `nvidia/cuda-arm64` and `nvidia/cuda-ppc64le` images names will be dropped in place of multi-arch container image manifests in `nvidia/cuda` on NGC and Docker Hub.

The following product pages will still exist but will no longer be supported:

* https://hub.docker.com/r/nvidia/cuda-ppc64le
* https://hub.docker.com/r/nvidia/cuda-arm64
* https://ngc.nvidia.com/containers/nvidia:cuda-ppc64le
* https://ngc.nvidia.com/containers/nvidia:cuda-arm64

Additionally, existing cuda-arm64 and cuda-ppc64le tags will not be deleted from Docker Hub or NGC and will be marked as unsupported in our [documentation](https://gitlab.com/nvidia/container-images/cuda/blob/master/doc/unsupported-tags.md).

### Deprecated: "latest" tag

The "latest" tag for CUDA, CUDAGL, and OPENGL images has been deprecated on NGC and Docker Hub.

With the removal of the latest tag, the following use case will result in the "manifest unknown" error:

```
$ docker pull nvidia/cuda
Error response from daemon: manifest for nvidia/cuda:latest not found: manifest unknown: manifest
unknown
```

This is not a bug.

## Overview of Images

Three flavors of images are provided:
- `base`: Includes the CUDA runtime (cudart)
- `runtime`: Builds on the `base` and includes the [CUDA math libraries](https://developer.nvidia.com/gpu-accelerated-libraries), and [NCCL](https://developer.nvidia.com/nccl). A `runtime` image that also includes [cuDNN](https://developer.nvidia.com/cudnn) is available.
- `devel`: Builds on the `runtime` and includes headers, development tools for building CUDA images. These images are particularly useful for multi-stage builds.

The Dockerfiles for the images are open-source and licensed under 3-clause BSD. For more information see the Supported Tags section below.

### NVIDIA Container Toolkit

The [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-docker) for Docker is required to run CUDA images.

For CUDA 10.0, `nvidia-docker2` (v2.1.0) or greater is recommended. It is also recommended to use Docker 19.03.

### How to report a problem

Read [NVIDIA Container Toolkit Frequently Asked Questions](https://github.com/NVIDIA/nvidia-docker/wiki/Frequently-Asked-Questions) to see if the problem has been encountered before.

After it has been determined the problem is not with the NVIDIA runtime, report an issue at the [CUDA Container Image Issue Tracker](https://gitlab.com/nvidia/container-images/cuda/-/issues).

## Supported tags

Supported tags are updated to the latest CUDA and cuDNN versions. These tags are also periodically updated to fix CVE vulnerabilities.

For a full list of supported tags, click [*here*](https://gitlab.com/nvidia/container-images/cuda/blob/master/doc/supported-tags.md).

## LATEST CUDA 11.3 Update 1

Visit [OpenSource @ Nvidia](https://developer.download.nvidia.com/compute/cuda/opensource/image/) for the GPL sources of the packages contained in the CUDA base image layers.


### Ubuntu 20.04

- [`11.3.1-cudnn8-runtime-ubuntu20.04` (*11.3.1/ubuntu20.04-x86_64/runtime/cudnn8/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/ubuntu20.04-x86_64/runtime/cudnn8/Dockerfile)
- [`11.3.1-runtime-ubuntu20.04` (*11.3.1/ubuntu20.04-x86_64/runtime/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/ubuntu20.04-x86_64/runtime/Dockerfile)
- [`11.3.1-cudnn8-devel-ubuntu20.04` (*11.3.1/ubuntu20.04-x86_64/devel/cudnn8/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/ubuntu20.04-x86_64/devel/cudnn8/Dockerfile)
- [`11.3.1-devel-ubuntu20.04` (*11.3.1/ubuntu20.04-x86_64/devel/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/ubuntu20.04-x86_64/devel/Dockerfile)
- [`11.3.1-base-ubuntu20.04` (*11.3.1/ubuntu20.04-x86_64/base/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/ubuntu20.04-x86_64/base/Dockerfile)

### Ubuntu 18.04

- [`11.3.1-cudnn8-runtime-ubuntu18.04` (*11.3.1/ubuntu18.04-x86_64/runtime/cudnn8/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/ubuntu18.04-x86_64/runtime/cudnn8/Dockerfile)
- [`11.3.1-runtime-ubuntu18.04` (*11.3.1/ubuntu18.04-x86_64/runtime/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/ubuntu18.04-x86_64/runtime/Dockerfile)
- [`11.3.1-cudnn8-devel-ubuntu18.04` (*11.3.1/ubuntu18.04-x86_64/devel/cudnn8/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/ubuntu18.04-x86_64/devel/cudnn8/Dockerfile)
- [`11.3.1-devel-ubuntu18.04` (*11.3.1/ubuntu18.04-x86_64/devel/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/ubuntu18.04-x86_64/devel/Dockerfile)
- [`11.3.1-base-ubuntu18.04` (*11.3.1/ubuntu18.04-x86_64/base/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/ubuntu18.04-x86_64/base/Dockerfile)

### Ubuntu 16.04

- [`11.3.1-cudnn8-runtime-ubuntu16.04` (*11.3.1/ubuntu16.04-x86_64/runtime/cudnn8/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/ubuntu16.04-x86_64/runtime/cudnn8/Dockerfile)
- [`11.3.1-runtime-ubuntu16.04` (*11.3.1/ubuntu16.04-x86_64/runtime/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/ubuntu16.04-x86_64/runtime/Dockerfile)
- [`11.3.1-cudnn8-devel-ubuntu16.04` (*11.3.1/ubuntu16.04-x86_64/devel/cudnn8/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/ubuntu16.04-x86_64/devel/cudnn8/Dockerfile)
- [`11.3.1-devel-ubuntu16.04` (*11.3.1/ubuntu16.04-x86_64/devel/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/ubuntu16.04-x86_64/devel/Dockerfile)
- [`11.3.1-base-ubuntu16.04` (*11.3.1/ubuntu16.04-x86_64/base/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/ubuntu16.04-x86_64/base/Dockerfile)

### UBI 8

- [`11.3.1-cudnn8-runtime-ubi8` (*11.3.1/ubi8-x86_64/runtime/cudnn8/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/ubi8-x86_64/runtime/cudnn8/Dockerfile)
- [`11.3.1-runtime-ubi8` (*11.3.1/ubi8-x86_64/runtime/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/ubi8-x86_64/runtime/Dockerfile)
- [`11.3.1-cudnn8-devel-ubi8` (*11.3.1/ubi8-x86_64/devel/cudnn8/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/ubi8-x86_64/devel/cudnn8/Dockerfile)
- [`11.3.1-devel-ubi8` (*11.3.1/ubi8-x86_64/devel/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/ubi8-x86_64/devel/Dockerfile)
- [`11.3.1-base-ubi8` (*11.3.1/ubi8-x86_64/base/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/ubi8-x86_64/base/Dockerfile)

### UBI 7

- [`11.3.1-cudnn8-runtime-ubi7` (*11.3.1/ubi7-x86_64/runtime/cudnn8/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/ubi7-x86_64/runtime/cudnn8/Dockerfile)
- [`11.3.1-runtime-ubi7` (*11.3.1/ubi7-x86_64/runtime/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/ubi7-x86_64/runtime/Dockerfile)
- [`11.3.1-cudnn8-devel-ubi7` (*11.3.1/ubi7-x86_64/devel/cudnn8/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/ubi7-x86_64/devel/cudnn8/Dockerfile)
- [`11.3.1-devel-ubi7` (*11.3.1/ubi7-x86_64/devel/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/ubi7-x86_64/devel/Dockerfile)
- [`11.3.1-base-ubi7` (*11.3.1/ubi7-x86_64/base/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/ubi7-x86_64/base/Dockerfile)

### CentOS 8

*WARNING*: POSSIBLE MISSING IMAGE TAGS

The Cuda image tags for centos7 and 8 may be missing on NGC and Docker Hub. Centos upstream images often fail security scans required by Nvidia before publishing images. Please check https://gitlab-master.nvidia.com/cuda-installer/cuda/-/issues for any security notices!

- [`11.3.1-cudnn8-runtime-centos8` (*11.3.1/centos8-x86_64/runtime/cudnn8/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/centos8-x86_64/runtime/cudnn8/Dockerfile)
- [`11.3.1-runtime-centos8` (*11.3.1/centos8-x86_64/runtime/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/centos8-x86_64/runtime/Dockerfile)
- [`11.3.1-cudnn8-devel-centos8` (*11.3.1/centos8-x86_64/devel/cudnn8/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/centos8-x86_64/devel/cudnn8/Dockerfile)
- [`11.3.1-devel-centos8` (*11.3.1/centos8-x86_64/devel/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/centos8-x86_64/devel/Dockerfile)
- [`11.3.1-base-centos8` (*11.3.1/centos8-x86_64/base/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/centos8-x86_64/base/Dockerfile)

### CentOS 7

*WARNING*: POSSIBLE MISSING IMAGE TAGS

The Cuda image tags for centos7 and 8 may be missing on NGC and Docker Hub. Centos upstream images often fail security scans required by Nvidia before publishing images. Please check https://gitlab-master.nvidia.com/cuda-installer/cuda/-/issues for any security notices!

- [`11.3.1-cudnn8-runtime-centos7` (*11.3.1/centos7-x86_64/runtime/cudnn8/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/centos7-x86_64/runtime/cudnn8/Dockerfile)
- [`11.3.1-runtime-centos7` (*11.3.1/centos7-x86_64/runtime/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/centos7-x86_64/runtime/Dockerfile)
- [`11.3.1-cudnn8-devel-centos7` (*11.3.1/centos7-x86_64/devel/cudnn8/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/centos7-x86_64/devel/cudnn8/Dockerfile)
- [`11.3.1-devel-centos7` (*11.3.1/centos7-x86_64/devel/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/centos7-x86_64/devel/Dockerfile)
- [`11.3.1-base-centos7` (*11.3.1/centos7-x86_64/base/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/11.3.1/centos7-x86_64/base/Dockerfile)

### Unsupported tags

A list of tags that are no longer supported can be found [*here*](https://gitlab.com/nvidia/container-images/cuda/blob/master/doc/unsupported-tags.md)

### Source of this description

This [Readme](https://gitlab.com/nvidia/container-images/cuda/blob/master/doc/README.md) is located in the `doc` directory of the CUDA Container Image source repository. ([history](https://gitlab.com/nvidia/container-images/cuda/commits/master/doc/README.md))
