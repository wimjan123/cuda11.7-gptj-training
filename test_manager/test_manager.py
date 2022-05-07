import pathlib
import os

from beeprint import pp  # type: ignore

import pytest

from manager import Manager, ManagerGenerate


def test_check_arches():
    """Sanity checks for the generated Dockerfile templates for arm64

    The NVARCH environment variable should be set to "sbsa" and not "arm64" in the Dockerfiles.

    This variable is used for the repo paths.
    """
    # _, rc = Manager.run(["prog", "--manifest=manifests/cuda.yaml", "generate", "--os-name=ubuntu", "--os-version=20.04", "--cuda-version=11.4.0", "--release-label=11.4.0"], exit=False)
    # pp(rc)
    # assert rc == 0
    arches = []
    def get_arches(filepath):
        narches = []
        with open(filepath) as file:
            lines = file.readlines()
            for line in lines:
                if "ENV NVARCH" in line:
                    narches.append(line.rstrip())
        return narches

    arches = get_arches(pathlib.Path("dist/11.4.0/ubuntu2004/base/Dockerfile"))
    assert arches
    assert any("x86_64" in arg for arg in arches)
    assert any("sbsa" in arg for arg in arches)

    arches = get_arches(pathlib.Path("dist/11.4.0/ubi8/base/Dockerfile"))
    assert arches
    assert any("x86_64" in arg for arg in arches)
    assert any("sbsa" in arg for arg in arches)

def haz_nvprof(filepath):
    with open(filepath) as file:
        lines = file.readlines()
        for line in lines:
            if "cuda-nvprof" in line:
                return True
    return False

def get_dockefiles(distro):
    files = []
    for root, _, _ in os.walk("dist"):
        if any(x in root for x in ["deprecated", "base", "runtime", "cudnn"]) or "devel" not in root:
            continue
        if "rhel" not in distro and distro not in root:
            continue
        if "rhel" in distro and not any(d in root for d in ["ubi", "centos", "rockylinux"]):
            continue
        files.append(pathlib.Path(f"{root}/Dockerfile"))
    return files

def test_check_nvprof_install_ubuntu():
    """Checks that ubuntu generated output contain nvprof"""
    failed = False
    for df in get_dockefiles("ubuntu"):
        if not haz_nvprof(df):
            print(f"missing nvprof: {df}")
            failed = True
        else:
            print(f"has nvprof: {df}")
    if failed:
        pytest.fail("nvprof is not being installed in some ubuntu docker files!")


def test_check_nvprof_install_rhel():
    """Checks that ubuntu generated output contain nvprof"""
    failed = False
    for df in get_dockefiles("rhel"):
        if not haz_nvprof(df):
            print(f"missing nvprof: {df}")
            failed = True
        else:
            print(f"has nvprof: {df}")
    if failed:
        pytest.fail("nvprof is not being installed in some rhel-based docker files!")
