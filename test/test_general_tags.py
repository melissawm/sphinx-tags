"""General tests for tag index and tag pages"""
from io import StringIO
from pathlib import Path
from test.conftest import OUTPUT_ROOT_DIR

import pytest
from sphinx.testing.util import SphinxTestApp

OUTPUT_DIR = OUTPUT_ROOT_DIR / "general"


def run_all_formats():
    """Return a decorator that runs a test in all supported markup formats"""
    return pytest.mark.parametrize(
        (),
        [
            pytest.param(marks=pytest.mark.sphinx("text", testroot="myst")),
            pytest.param(marks=pytest.mark.sphinx("text", testroot="rst")),
            pytest.param(marks=pytest.mark.sphinx("text", testroot="symlink")),
            pytest.param(marks=pytest.mark.sphinx("text", testroot="ipynb")),
        ],
    )


@run_all_formats()
def test_build(app: SphinxTestApp, status: StringIO, warning: StringIO):
    app.build()
    assert "build succeeded" in status.getvalue()

    # Build with notebooks and text output results in spurious errors "File Not Found: _tags/*.html"
    # For all other formats, ensure no warnings are raised
    if not app.srcdir.endswith("ipynb"):
        assert not warning.getvalue().strip()


@run_all_formats()
def test_index(app: SphinxTestApp):
    app.build()
    build_dir = Path(app.srcdir) / "_build" / "text"

    # Check tags index page
    contents = (build_dir / "_tags" / "tagsindex.txt").read_text()
    expected_contents = (OUTPUT_DIR / "_tags" / "tagsindex.txt").read_text()
    assert contents == expected_contents

    # Check full toctree created by index
    contents = (build_dir / "index.txt").read_text()
    expected_contents = (OUTPUT_DIR / "index.txt").read_text()
    assert contents == expected_contents


@run_all_formats()
def test_tag_pages(app: SphinxTestApp):
    app.build()
    build_dir = Path(app.srcdir) / "_build" / "text"

    # Check all expected tag pages
    for tag in ["tag_1", "tag2", "tag-3", "tag-4", "tag_5", "test-tag-please-ignore"]:
        contents = (build_dir / "_tags" / f"{tag}.txt").read_text()
        expected_contents = (OUTPUT_DIR / "_tags" / f"{tag}.txt").read_text()
        assert contents == expected_contents


@run_all_formats()
def test_tagged_pages(app: SphinxTestApp):
    app.build()
    build_dir = Path(app.srcdir) / "_build" / "text"

    # Check all expected tag pages
    for page in [Path("page_1.txt"), Path("page_2.txt"), Path("subdir") / "page_3.txt"]:
        contents = (build_dir / page).read_text()
        expected_contents = (OUTPUT_DIR / page).read_text()
        assert contents == expected_contents
