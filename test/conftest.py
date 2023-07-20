"""Notes:
* A Sphinx test app is provided via `app` fixture from `sphinx.testing.fixtures`.
    * This first needs to be enabled as a plugin
* The `rootdir` fixture sets the root directory for source files used by the test app
* A subdirectory for a specific test is set by `@pytest.mark.sphinx("text", testroot="...")
* This subdirectory must contain a conf.py and source files
"""
import pytest
from sphinx.testing.path import path

collect_ignore = ["sources"]
pytest_plugins = "sphinx.testing.fixtures"


@pytest.fixture(scope="session")
def rootdir():
    return path(__file__).parent.abspath() / "sources"
