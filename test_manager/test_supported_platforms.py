from config import *


def test_arches_csv():
    """Test csv output for a platforms supported architectures."""
    assert (
        supported_platforms.by_distro("ubuntu2204").common_arches_csv() == "arm64, x86_64"
    )
    assert (
        supported_platforms.by_distro("ubi8").common_arches_csv()
        == "x86_64, arm64, ppc64le"
    )


def test_all_architectures():
    """ """
    assert supported_platforms.all_architectures() == [
        "arm64",
        "jetson",
        "ppc64le",
        "x86_64",
    ]
