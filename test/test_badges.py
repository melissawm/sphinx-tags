"""General tests for tag index and tag pages"""
from io import StringIO
from pathlib import Path
from test.conftest import OUTPUT_ROOT_DIR

import pytest
from bs4 import BeautifulSoup
from sphinx.testing.util import SphinxTestApp

OUTPUT_DIR = OUTPUT_ROOT_DIR / "badges"
EXPECTED_CLASSES = {
    "tag-1": "sd-bg-primary",
    "tag-2": "sd-bg-secondary",
    "prefix-tag-3": "sd-bg-info",
    "tag-4": "sd-bg-dark",
}


@pytest.mark.sphinx("html", testroot="badges")
def test_badges(app: SphinxTestApp, status: StringIO, warning: StringIO):
    """Parse output HTML for a page with badges, find badge links, and check for CSS classes for
    expected badge colors
    """
    app.build()
    assert "build succeeded" in status.getvalue()
    assert not warning.getvalue().strip()

    build_dir = Path(app.srcdir) / "_build" / "html"
    page_1 = (build_dir / "page_1.html").read_text()
    soup = BeautifulSoup(page_1, "html.parser")
    # print(soup.prettify())

    badge_links = soup.find_all("a", class_="sd-badge")
    classes_by_tag = {Path(a.get("href")).stem: a.get("class") for a in badge_links}

    for tag, cls in EXPECTED_CLASSES.items():
        assert cls in classes_by_tag[tag]
