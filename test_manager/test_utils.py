import yaml

from utils import *


def test_supported_distro_list_by_cuda_version():
    """ """
    manifest: dict[str, dict[str, dict[str, str]]] = {}
    with open(pathlib.Path("manifests/cuda.yaml"), "r") as f:
        manifest = yaml.load(f, yaml.Loader)
    assert supported_distro_list_by_cuda_version(manifest, "11.0.3") == [
        "centos7",
        "ubi7",
        "ubi8",
        "ubi9",
        "ubuntu18.04",
        "ubuntu20.04",
        "ubuntu22.04",
    ]


def test_supported_arch_list():
    """ """
    manifest: dict[str, dict[str, dict[str, str]]] = {}
    with open(pathlib.Path("manifests/cuda.yaml"), "r") as f:
        manifest = yaml.load(f, yaml.Loader)
    assert supported_arch_list(manifest, "ubi8", "11.6.2") == [
        "arm64",
        "ppc64le",
        "x86_64",
    ]
