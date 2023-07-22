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
        ],
    )


@run_all_formats()
def test_index(app: SphinxTestApp, status: StringIO, warning: StringIO):
    app.build()
    build_dir = Path(app.srcdir) / "_build" / "text"
    assert "build succeeded" in status.getvalue()
    assert not warning.getvalue().strip()

    # Check tags index page
    contents = (build_dir / "_tags" / "tagsindex.txt").read_text()
    expected_contents = (OUTPUT_DIR / "_tags" / "tagsindex.txt").read_text()
    assert contents == expected_contents

    # Check full toctree created by index
    contents = (build_dir / "index.txt").read_text()
    expected_contents = (OUTPUT_DIR / "index.txt").read_text()
    assert contents == expected_contents


@run_all_formats()
def test_tag_pages(app: SphinxTestApp, status: StringIO, warning: StringIO):
    app.build()
    build_dir = Path(app.srcdir) / "_build" / "text"
    assert "build succeeded" in status.getvalue()
    assert not warning.getvalue().strip()

    # Check all expected tag pages
    for tag in ["tag_1", "tag2", "tag-3", "tag-4", "tag_5", "test-tag-please-ignore"]:
        contents = (build_dir / "_tags" / f"{tag}.txt").read_text()
        expected_contents = (OUTPUT_DIR / "_tags" / f"{tag}.txt").read_text()
        assert contents == expected_contents
