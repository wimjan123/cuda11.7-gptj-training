# Nvidia CUDA Linux Container Image Sources

Usage of the CUDA container images requires the [Nvidia Container Runtime](https://github.com/NVIDIA/nvidia-container-runtime).

Container images are available from:

- https://ngc.nvidia.com/catalog/containers/nvidia:cuda
- https://hub.docker.com/r/nvidia/cuda

## Announcement

### Tag deprecation

The following tags will no longer be updated.

* `<cuda_version>-base`, `<cuda_version>-runtime`, `<cuda_version>-devel`
  * These tags will be deleted.
* All tags for 9.2, 9.1, 9.0, and 8.0

### Cuda Repo Signing Key has Changed!

This may present itself as the following errors.

debian:

```
Reading package lists... Done
W: GPG error: http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64  InRelease: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY A4B469963BF863CC
W: The repository 'http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64  InRelease' is not signed.
N: Data from such a repository can't be authenticated and is therefore potentially dangerous to use.
N: See apt-secure(8) manpage for repository creation and user configuration details.
```

RPM:

```
warning: /var/cache/dnf/cuda-fedora32-x86_64-d60aafcddb176bf5/packages/libnvjpeg-11-1-11.3.0.105-1.x86_64.rpm: Header V4 RSA/SHA512 Signature, key ID d42d0685: NOKEY
cuda-fedora32-x86_64                                                                                  23 kB/s | 1.6 kB     00:00
Importing GPG key 0x7FA2AF80:
 Userid     : "cudatools <cudatools@nvidia.com>"
 Fingerprint: AE09 FE4B BD22 3A84 B2CC FCE3 F60F 4B3D 7FA2 AF80
 From       : https://developer.download.nvidia.com/compute/cuda/repos/fedora32/x86_64/7fa2af80.pub
Is this ok [y/N]: y
Key imported successfully
Import of key(s) didn't help, wrong key(s)?
Public key for libnvjpeg-11-1-11.3.0.105-1.x86_64.rpm is not installed. Failing package is: libnvjpeg-11-1-11.3.0.105-1.x86_64
 GPG Keys are configured as: https://developer.download.nvidia.com/compute/cuda/repos/fedora32/x86_64/7fa2af80.pub
The downloaded packages were saved in cache until the next successful transaction.
You can remove cached packages by executing 'dnf clean packages'.
Error: GPG check FAILED
```

Updated images will be pushed out over the next few days containing the new repo key. Please follow progress using the links below:

* https://forums.developer.nvidia.com/t/notice-cuda-linux-repository-key-rotation/212771h
* https://gitlab.com/nvidia/container-images/cuda/-/issues/158

### Multi-arch image manifests are now LIVE for all supported CUDA container image versions

It is now possible to build CUDA container images for all supported architectures using Docker
Buildkit in one step. See the example script below.

The deprecated image names `nvidia/cuda-arm64` and `nvidia/cuda-ppc64le` will remain available, but no longer supported.

The following product pages still exist but will no longer be supported:

* https://hub.docker.com/r/nvidia/cuda-ppc64le
* https://hub.docker.com/r/nvidia/cuda-arm64

The following gitlab repositories will be archived:

* https://gitlab.com/nvidia/container-images/cuda-ppc64le
* https://gitlab.com/nvidia/container-images/cuda-arm64

### Deprecated: "latest" tag

The "latest" tag for CUDA, CUDAGL, and OPENGL images has been deprecated on NGC and Docker Hub.

With the removal of the latest tag, the following use case will result in the "manifest unknown"
error:

```
$ docker pull nvidia/cuda
Error response from daemon: manifest for nvidia/cuda:latest not found: manifest unknown: manifest
unknown
```

This is not a bug.

## IMAGE SECURITY NOTICE

The CUDA images are scanned for CVE vulnerabilities prior to release and some images may contain CVEs at the time of publication.

Our Product Security teams reviews the CVEs and determines if the CVE should block the release or not. We try to mitigate as much as we can, but since we do not control the upstream base images, some cuda image releases might be impacted.

Please consult the README on the NGC or Docker Hub pages for details.

## LD_LIBRARY_PATH NOTICE

The `LD_LIBRARY_PATH` is set inside the container to legacy nvidia-docker v1 paths that do not exist on newer installations. This is done to maintain compatibility for our partners that still use nvidia-docker v1 and this will not be changed for the forseable future. [There is a chance this might cause issues for some.](https://gitlab.com/nvidia/container-images/cuda/-/issues/47)

## Building from source

The container image scripts are archived in the `dist/` directory and are available for all supported distros and cuda versions.

Here is an example on how to build an multi-arch container image for Ubuntu 18.04 and CUDA 11.6.0:

```bash
./build.sh -d --image-name my-remote-container-registry/cuda --cuda-version 11.6.0 --os ubuntu18.04 --arch x86_64,arm64 --push
```

See `./build.sh --help` for usage.

## Cuda Container Image Automation

The [README_CICD.md](https://gitlab.com/nvidia/container-images/cuda/blob/master/README_CICD.md) document provides details on how the gitlab pipelines work and how to control, modify, or debug them.
