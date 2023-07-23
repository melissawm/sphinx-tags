"""Notes on testing setup:
* A Sphinx test app is provided via `app` fixture from `sphinx.testing.fixtures`.
    * This first needs to be enabled as a plugin
* The `sources` dir contains source files and config to use for tests
    * Set via the `rootdir` fixture
* A subdirectory to use for a specific test can be set by a pytest marker:
    * `@pytest.mark.sphinx("text", testroot="...")
    * This subdirectory must contain a conf.py and source files
* The `outputs` dir contains expected output files
"""
import shutil
from os import symlink
from pathlib import Path
from unittest.mock import patch

import pytest
import sphinx.testing
import sphinx.testing.path

collect_ignore = ["sources", "outputs"]
pytest_plugins = "sphinx.testing.fixtures"

OUTPUT_ROOT_DIR = Path(__file__).parent.absolute() / "outputs"
SOURCE_ROOT_DIR = Path(__file__).parent.absolute() / "sources"


@pytest.fixture(scope="session")
def rootdir():
    """This fixture overrides the root directory used by SphinxTestApp. It also patches
    sphinx.testing's custom path object to copy symlinks as symlinks; otherwise symlink paths are
    resolved and copied as files.
    """

    def copytree(src, dest):
        shutil.copytree(src, dest, symlinks=True)

    with patch.object(sphinx.testing.path.path, "copytree", copytree):
        yield sphinx.testing.path.path(SOURCE_ROOT_DIR)


@pytest.fixture(scope="session", autouse=True)
def create_symlinks():
    """Create symlinks for source files and subdirectories, and remove them after tests finish"""
    symlink_dest_dir = SOURCE_ROOT_DIR / "test-symlink"

    for file in SOURCE_ROOT_DIR.glob("test-rst/*.rst"):
        symlink(file, symlink_dest_dir / file.name)
    for dir in SOURCE_ROOT_DIR.glob("test-rst/subdir*"):
        symlink(dir, symlink_dest_dir / dir.name, target_is_directory=True)

    yield

    for file in symlink_dest_dir.glob("*.rst"):
        file.unlink()
    for dir in symlink_dest_dir.glob("subdir*"):
        try:
            dir.unlink()
        # Unlink will fail on Windows
        except OSError:
            dir.rmdir()
