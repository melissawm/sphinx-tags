"""Tests for tag validation logic"""

from io import StringIO
import pytest
from sphinx.errors import ExtensionError
from sphinx.testing.util import SphinxTestApp
from test.conftest import OUTPUT_ROOT_DIR
import logging
from sphinx_tags import TagLinks
from unittest.mock import MagicMock

OUTPUT_DIR = OUTPUT_ROOT_DIR / "general"

"""Positive cases"""


@pytest.mark.sphinx("html", testroot="validations")
def test_default(app: SphinxTestApp, status: StringIO):
    app.build(force_all=True)
    assert "build succeeded" in status.getvalue()


@pytest.mark.sphinx(
    "html", testroot="validations", confoverrides={"tags_maximum_tag_count": 3}
)
def test_maximum_pass(app: SphinxTestApp, status: StringIO):
    app.build(force_all=True)
    assert "build succeeded" in status.getvalue()


@pytest.mark.sphinx(
    "html", testroot="validations", confoverrides={"tags_minimum_tag_count": 2}
)
def test_minimum_pass(app: SphinxTestApp, status: StringIO):
    app.build(force_all=True)
    assert "build succeeded" in status.getvalue()


"""Negative cases"""


@pytest.mark.sphinx(
    "html",
    testroot="validations",
    freshenv=True,
    confoverrides={"tags_allowed_tag_names_regex": ["nottag.*"]},
)
def test_allowed_tag_names_regex_error(app: SphinxTestApp):
    with pytest.raises(ExtensionError):
        app.build(force_all=True)


@pytest.mark.sphinx(
    "html",
    testroot="validations",
    freshenv=True,
    confoverrides={"tags_minimum_tag_count": 4},
)
def test_minimum_error(app: SphinxTestApp):
    with pytest.raises(ExtensionError):
        app.build(force_all=True)


@pytest.mark.sphinx(
    "html",
    testroot="validations",
    freshenv=True,
    confoverrides={"tags_maximum_tag_count": 1},
)
def test_maximum_error(app: SphinxTestApp):
    with pytest.raises(ExtensionError):
        app.build(force_all=True)
