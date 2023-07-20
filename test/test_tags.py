from io import StringIO
from pathlib import Path
from textwrap import dedent

import pytest
from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("text", testroot="test1")
def test_index(app: SphinxTestApp, status: StringIO, warning: StringIO) -> None:
    app.build()
    build_dir = Path(app.srcdir) / "_build" / "text"
    assert "build succeeded" in status.getvalue()
    assert not warning.getvalue().strip()

    contents = (build_dir / "_tags" / "tagsindex.txt").read_text()
    expected_contents = """\
    Tags overview
    *************


    Tags
    ^^^^

    * [{(tag   4)}] (1)

    * tag 3 (1)

    * tag2 (1)

    * tag_1 (2)

    * tag_5 (1)
    """
    assert contents == dedent(expected_contents)


@pytest.mark.sphinx("text", testroot="test1")
def test_index_toctree(app: SphinxTestApp, status: StringIO, warning: StringIO) -> None:
    app.build()
    build_dir = Path(app.srcdir) / "_build" / "text"
    assert "build succeeded" in status.getvalue()
    assert not warning.getvalue().strip()

    contents = (build_dir / "index.txt").read_text()
    expected_contents = """\
    Test Doc
    ********

    Test document

    * Page 1

    * Page 2

    * Tags overview

      * [{(tag   4)}] (1)

        * Page 1

      * tag 3 (1)

        * Page 1

      * tag2 (1)

        * Page 1

      * tag_1 (2)

        * Page 1

        * Page 2

      * tag_5 (1)

        * Page 2
    """
    assert contents == dedent(expected_contents)


@pytest.mark.sphinx("text", testroot="test1")
def test_tag_pages(app: SphinxTestApp, status: StringIO, warning: StringIO) -> None:
    app.build()
    build_dir = Path(app.srcdir) / "_build" / "text"
    assert "build succeeded" in status.getvalue()
    assert not warning.getvalue().strip()

    contents = (build_dir / "_tags" / "tag_1.txt").read_text()
    expected_contents = """\
    My tags: tag_1
    **************


    With this tag
    ^^^^^^^^^^^^^

    * Page 1

    * Page 2
    """
    assert contents == dedent(expected_contents)

    contents = (build_dir / "_tags" / "tag-3.txt").read_text()
    expected_contents = """\
    My tags: tag 3
    **************


    With this tag
    ^^^^^^^^^^^^^

    * Page 1
    """
    assert contents == dedent(expected_contents)
