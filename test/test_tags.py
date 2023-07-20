from io import StringIO
from pathlib import Path
from test.conftest import OUTPUT_ROOT_DIR

import pytest
from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("text", testroot="test1")
def test_index(app: SphinxTestApp, status: StringIO, warning: StringIO) -> None:
    app.build()
    build_dir = Path(app.srcdir) / "_build" / "text"
    assert "build succeeded" in status.getvalue()
    assert not warning.getvalue().strip()

    # Check tags index page
    contents = (build_dir / "_tags" / "tagsindex.txt").read_text()
    expected_contents = (
        OUTPUT_ROOT_DIR / "test1" / "_tags" / "tagsindex.txt"
    ).read_text()
    assert contents == expected_contents

    # Check full toctree created by index
    contents = (build_dir / "index.txt").read_text()
    expected_contents = (OUTPUT_ROOT_DIR / "test1" / "index.txt").read_text()
    assert contents == expected_contents


@pytest.mark.sphinx("text", testroot="test1")
def test_tag_pages(app: SphinxTestApp, status: StringIO, warning: StringIO) -> None:
    app.build()
    build_dir = Path(app.srcdir) / "_build" / "text"
    assert "build succeeded" in status.getvalue()
    assert not warning.getvalue().strip()

    for tag in ["tag_1", "tag2", "tag-3", "tag-4", "tag_5"]:
        contents = (build_dir / "_tags" / f"{tag}.txt").read_text()
        expected_contents = (
            OUTPUT_ROOT_DIR / "test1" / "_tags" / f"{tag}.txt"
        ).read_text()
        assert contents == expected_contents
