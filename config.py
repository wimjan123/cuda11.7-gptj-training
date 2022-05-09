import logging

from dataclasses import dataclass, field
from typing import List, TypeVar
from collections import namedtuple

from dotdict import DotDict

from beeprint import pp  # type: ignore

log = logging.getLogger()

HTTP_RETRY_ATTEMPTS = 3
HTTP_RETRY_WAIT_SECS = 30

L4T_BASE_IMAGE_NAME = "nvcr.io/nvidian/nvidia-l4t-base"

# Increased buildkit version from 0.8.1 to 0.10.3 to overcome ubuntu 22.04 build failures
MOBY_BUILDKIT_VERSION = "v0.10.3"

# Can be removed with python 3.11 https://peps.python.org/pep-0673/
TSupportedPlatform = TypeVar("TSupportedPlatform", bound="SupportedPlatform")


@dataclass(frozen=True)
class SupportedArchitecture:
    """ """

    arch: str
    common_name: str
    repo_name: tuple
    real_name: str = ""


@dataclass(frozen=True)
class SupportedPlatform:
    """ """

    distro: str
    version: str
    arches: List[SupportedArchitecture]
    package_format: str
    flavor: str = ""
    image_name: str = ""
    common_name: str = ""

    def full_name(self) -> str:
        """ """
        return f"{self.distro}{self.version}"

    def shipit_distro_name(self) -> str:
        """ """
        return f"{self.distro}{self.version.replace('.','')}"

    def shipit_distro_arch(self, shipit_arch_key: str) -> bool:
        """ """
        return any(x.arch in shipit_arch_key for x in self.arches)

    def rhel_based_supported(self, distro: str) -> bool:
        return (
            "rhel" in distro and "rpm" in self.package_format and self.version in distro
        )

    def common_arches_csv(self) -> str:
        """ """
        csv: List[str] = []
        for arch in self.arches:
            csv.append(arch.common_name)
        return ", ".join(csv)


_package_repo_arch_repr = namedtuple("repo_name", ["deb", "rpm"])

_arches = DotDict(
    {
        "arm64": SupportedArchitecture(
            arch="arm64",
            common_name="arm64",
            repo_name=_package_repo_arch_repr(deb="sbsa", rpm="sbsa"),
            real_name="sbsa",
        ),
        "x86_64": SupportedArchitecture(
            arch="x86_64",
            # common name is really amd64, but only containers use that in our world
            common_name="x86_64",
            repo_name=_package_repo_arch_repr(deb="x86_64", rpm="x86_64"),
            real_name="amd64",
        ),
        "ppc64le": SupportedArchitecture(
            arch="ppc64le",
            common_name="ppc64le",
            repo_name=_package_repo_arch_repr(deb="ppc64el", rpm="ppc64le"),
        ),
        "jetson": SupportedArchitecture(
            arch="jetson",
            common_name="arm64",
            repo_name=_package_repo_arch_repr(deb="arm64", rpm="arm64"),
            real_name="aarch64",
        ),
    }
)


def _pop_supported_platforms():
    return [
        SupportedPlatform(
            distro="ubuntu",
            version="22.04",
            arches=[_arches.arm64, _arches.x86_64],
            package_format="deb",
        ),
        SupportedPlatform(
            distro="ubuntu",
            version="20.04",
            arches=[_arches.arm64, _arches.x86_64],
            package_format="deb",
        ),
        SupportedPlatform(
            distro="ubuntu",
            version="18.04",
            arches=[_arches.x86_64],
            package_format="deb",
        ),
        SupportedPlatform(
            distro="centos", version="7", arches=[_arches.x86_64], package_format="rpm"
        ),
        SupportedPlatform(
            distro="ubi",
            version="9",
            arches=[_arches.x86_64, _arches.arm64, _arches.ppc64le],
            package_format="rpm",
        ),
        SupportedPlatform(
            distro="ubi",
            version="8",
            arches=[_arches.x86_64, _arches.arm64, _arches.ppc64le],
            package_format="rpm",
        ),
        SupportedPlatform(
            distro="ubi", version="7", arches=[_arches.x86_64], package_format="rpm"
        ),
        SupportedPlatform(
            distro="centos", version="7", arches=[_arches.x86_64], package_format="rpm"
        ),
        SupportedPlatform(
            distro="ubuntu",
            version="18.04",
            arches=[_arches.jetson],
            package_format="deb",
            common_name="l4t",
            flavor="jp4",
            image_name="gitlab-master.nvidia.com:5005/cuda-installer/cuda/l4t-cuda",
        ),
        SupportedPlatform(
            distro="ubuntu",
            version="20.04",
            arches=[_arches.jetson],
            package_format="deb",
            common_name="l4t",
            flavor="jp5",
            image_name="gitlab-master.nvidia.com:5005/cuda-installer/cuda/l4t-cuda",
        ),
    ]


@dataclass(frozen=True)
class SupportedPlatformsList:
    list: List[SupportedPlatform] = field(default_factory=_pop_supported_platforms)

    def is_supported(self, distro: str) -> bool:
        """ """
        for p in self.list:
            if distro in p.shipit_distro_name() or (
                p.rhel_based_supported(distro) and p.version in distro
            ):
                return True
        return False

    def translated_name(self, distro: str) -> List[str]:
        """ """
        name: List[str] = []
        for p in self.list:
            if distro in p.shipit_distro_name() or (
                p.rhel_based_supported(distro) and p.version in distro
            ):
                name.append(p.shipit_distro_name())
        assert name
        return name

    def by_distro(self: TSupportedPlatform, distro: str) -> TSupportedPlatform:
        """ """
        for x in self.list:
            if distro in x.shipit_distro_name():
                return x

    def all_architectures(self) -> List[str]:
        """ """
        theset = set()
        for x in self.list:
            for y in x.arches:
                theset.add(y.arch)
        return list(sorted(theset))


supported_platforms = SupportedPlatformsList()
