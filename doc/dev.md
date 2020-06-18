# Cuda Container Image Automation Documentation

This document is divided into three sections:

1. *Development Environment*: Setup the Python environment for developing the automation script.
1. *Gitlab Pipelines*: Contains details on how to operate the gitlab automation.
1. *Image Manifests*: Features of the yaml file used to generate image scripts.

## Development Environment

Setup the environment to work on manager.py and generate container image scripts from templates for building images.

### Setup

1. Install poetry. See https://poetry.eustace.io/docs/#installation

1. Install the dependencies with `poetry install`

1. Enter the virtual environment with `poetry shell`

Once in the virtual environment, run the script with:

```
python manager.py
```

# Gitlab Pipelines

## Triggering pipelines

Pipelines can be triggered automatically or explicitly via commit message.

The pipeline mechanism used for this project within gitlab is a workround [until multiple pipelines per gitlab-ci.yaml file is implemented in gitlab.](https://gitlab.com/gitlab-org/gitlab-ce/issues/22972)

### Manual triggering with optional dry-run

To run the pipeline without publishing to the registries indicated in `manifest.yaml`:

1. Go to the [pipelines](https://gitlab-master.nvidia.com/cuda-installer/cuda/pipelines) page and click "Run Pipeline".

1. Ensure the correct branch of the repo is selected.

1. Add an input variable, it should be set to `TRIGGER_OVERRIDE` with a value of "all"

   1. The "Explicit Triggering" section below has details on the potential of this value.

1. Add an input variable, it should be set to `DRY_RUN` with a value of "1".

1. Click "Run Pipeline"

### Automatic triggering

FIXME: As of June 17, 2020 this feature is broken. It will be fixed at a future date or removed.

By default on the master branch, the manifest.yaml file is compared against the previous version from the last commit. The changed keys within the manifest are then used to trigger builds via the gitlab api.

### Explicit triggering

Pipeline triggering can be overridden via the git commit message with:

```
ci.trigger = <pipeline>[,...]
```

Where pipeline can be:

- `all`: All of the pipelines are built.
- `<distro><distro_version>-cuda<major>.<minor>`: A specific cuda version for a specific cuda version.
- `cuda<major>.<minor>`: A cuda version for all distros.
- `<distro><distro_version>`: all cuda versions for a distro version.
- **TODO**: `cudnn<version>`: A cudnn version for all distros.

### Examples

* `ci.trigger = cuda11.0`: All cuda 11.0 pipelines for all platforms and architectures.
* `ci.trigger = ubuntu18.04-cuda11.0`: All ubuntu18.04 pipelines for cuda11.0 on all supported architectures.
* `ci.trigger = ubuntu18.04,ubuntu16.04`: All ubuntu18.04 and 16.04 pipelines for all supported cuda versions and architectures.
* `ci.trigger = ubuntu18.04-cuda11.0-x86_64`: Only ubuntu18.04 cuda11.0 pipeline for x86_64.

# Image Manifests

TODO: This section needs a re-write.

Configuration of Dockerfile and Test output for the numerous platforms and architectures supported by CUDA Docker is defined in manifest.yaml.

### Image definition

To define a new image:

```
ubi7:
  template_path: redhat
  cuda:
    repo_url: "http://developer.download.nvidia.com/compute/cuda/repos/rhel6/x86_64"
    v10.0:
      build_version: 130
      cuda_requires: "brand=tesla,driver>=384,driver<385 brand=tesla,driver>=410,driver<411"
      cudnn7:
        version: "7.6.0.64"
        sha256sum: "c4e1ee4168f4cadabaa989487a47bed09f34d34e35398b6084a2699d11bd2560"
```

Notable keys:

* *template_path*: The path to search in for templates for this image. The path should be in the same directory as manager.py.

* *cuda*: Controls the versions of cuda supported by this image definition. It is possible to define multiple cuda versions as well as multiple cudnn versions.

* *repo_url*: A variable used in the container source templates.

* *skip_tests*: Don't generate tests for the cuda version.

And to generate the image:

```
python manager.py generate --os ubi --os-version 7 --cuda-version 10.1
```

### Container Push Repos

The container repos that manager.py can push are defined on a global level and can be excluded on a image level.

If `only_if` is defined on the repo object in manifest.yaml, manager.py will only use that repo if the defined value is also present in the global environment. For example:

```
docker_repos:
  docker.io:
    only_if: REGISTRY_TOKEN
```

will result in manager.py pushing to docker.io only if the `REGISTRY_TOKEN` global variable is defined in the environment.

#### Excluding push repos based on image

If an image root object in `manifest.yaml` contains the `exclude_repos` key, then manager.py will not push to that repo for that image. For example,

```
ubi7:
  base_image: registry.access.redhat.com/ubi7/ubi:latest
  exclude_repos:
    - docker.io
```

manager.py will not push the UBI-7 images to docker.io.
