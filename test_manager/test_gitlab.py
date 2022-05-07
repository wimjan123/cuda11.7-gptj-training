import pathlib

from beeprint import pp  # type: ignore

from manager import Manager, ManagerGenerate

import config


def test_check_moby_buildkit_set():
    """Ensures moby/buildkit version is set to the correct version in the gitlab pipeline."""
    _, rc = Manager.run(
        ["prog", "--manifest=manifests/cuda.yaml", "generate", "--ci"], exit=False
    )
    pp(config.MOBY_BUILDKIT_VERSION)
    assert rc == 0
    count = 0
    with open(pathlib.Path(".gitlab-ci.yml")) as file:
        lines = file.readlines()
        for line in lines:
            if f"image=moby/buildkit:{config.MOBY_BUILDKIT_VERSION}" in line:
                count = count + 1
    assert count == 3
