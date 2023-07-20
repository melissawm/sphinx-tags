"""Notes on testing setup:
* A Sphinx test app is provided via `app` fixture from `sphinx.testing.fixtures`.
    * This first needs to be enabled as a plugin
* The `sources` dir contains source files and config to use for tests
    * Set via the `rootdir` fixture
* A subdirectory to use for a specific test can be set by a pytest mark:
    * `@pytest.mark.sphinx("text", testroot="...")
    * This subdirectory must contain a conf.py and source files
* The `outputs` dir contains expected output files
"""
from pathlib import Path

import pytest
import sphinx.testing

collect_ignore = ["sources", "outputs"]
pytest_plugins = "sphinx.testing.fixtures"

OUTPUT_ROOT_DIR = Path(__file__).parent.absolute() / "outputs"
SOURCE_ROOT_DIR = Path(__file__).parent.absolute() / "sources"


@pytest.fixture(scope="session")
def rootdir():
    return sphinx.testing.path.path(SOURCE_ROOT_DIR)
