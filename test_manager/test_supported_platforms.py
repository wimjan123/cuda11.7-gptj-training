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
