"""General tests for tag index and tag pages"""

from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from sphinx.errors import ExtensionError
from sphinx.testing.util import SphinxTestApp

from sphinx_tags import TagLinks

from test.conftest import OUTPUT_ROOT_DIR

OUTPUT_DIR = OUTPUT_ROOT_DIR / "general"
SINGLE_PAGE_OUTPUT_DIR = OUTPUT_ROOT_DIR / "general_single_page"


def assert_output_matches(build_dir: Path, expected_dir: Path, relative_path: Path):
    contents = build_dir / relative_path
    expected_contents = expected_dir / relative_path
    assert (
        contents.read_text().splitlines() == expected_contents.read_text().splitlines()
    )


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
        ids=["myst", "rst", "symlink", "ipynb"],
    )


@run_all_formats()
def test_build(app: SphinxTestApp, status: StringIO, warning: StringIO):
    app.build(force_all=True)
    assert "build succeeded" in status.getvalue()

    # Build with notebooks and text output results in spurious errors "File Not Found: _tags/*.html"
    # For all other formats, ensure no warnings are raised
    if not str(app.srcdir).endswith("ipynb"):
        assert not warning.getvalue().strip()


@pytest.mark.sphinx(confoverrides={"tags_create_tags": True})
@run_all_formats()
def test_index(app: SphinxTestApp):
    app.build(force_all=True)
    build_dir = Path(app.srcdir) / "_build" / "text"
    # Check tags index page
    assert_output_matches(build_dir, OUTPUT_DIR, Path("_tags") / "tagsindex.txt")

    # Check full toctree created by index
    assert_output_matches(build_dir, OUTPUT_DIR, Path("index.txt"))


@pytest.mark.sphinx(confoverrides={"tags_create_tags": True})
@run_all_formats()
def test_tag_pages(app: SphinxTestApp):
    app.build(force_all=True)
    build_dir = Path(app.srcdir) / "_build" / "text"

    # Check all expected tag pages
    for tag in ["tag_1", "tag2", "tag-3", "tag-4", "tag_5", "test-tag-please-ignore"]:
        assert_output_matches(build_dir, OUTPUT_DIR, Path("_tags") / f"{tag}.txt")


@run_all_formats()
def test_tagged_pages(app: SphinxTestApp):
    app.build(force_all=True)
    build_dir = Path(app.srcdir) / "_build" / "text"

    # Check all expected tag pages
    for page in [
        Path("page_1.txt"),
        Path("page_2.txt"),
        Path("page_5.txt"),
        Path("subdir") / "page_3.txt",
    ]:
        assert_output_matches(build_dir, OUTPUT_DIR, page)


@pytest.mark.sphinx(confoverrides={"tags_create_tags": True, "tags_single_page": True})
@run_all_formats()
def test_single_page_index(app: SphinxTestApp):
    app.build(force_all=True)
    build_dir = Path(app.srcdir) / "_build" / "text"

    assert_output_matches(
        build_dir, SINGLE_PAGE_OUTPUT_DIR, Path("_tags") / "tagsindex.txt"
    )
    assert_output_matches(build_dir, SINGLE_PAGE_OUTPUT_DIR, Path("index.txt"))


def test_empty_taglinks():
    tag_links = TagLinks(
        "tags",
        "",
        {},
        [],
        0,
        0,
        "",
        MagicMock(),
        MagicMock(),
    )
    msg = "No tags passed to 'tags' directive"
    with pytest.raises(ExtensionError, match=msg):
        tag_links.run()
