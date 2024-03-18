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
    "prefix:tag-3": "sd-bg-info",
    "tag 4": "sd-bg-dark",
}


@pytest.mark.sphinx("html", testroot="badges")
def test_build(app: SphinxTestApp, status: StringIO, warning: StringIO):
    app.build()
    assert "build succeeded" in status.getvalue()


@pytest.mark.sphinx("html", testroot="badges")
def test_badges(app: SphinxTestApp, status: StringIO, warning: StringIO):
    """Parse output HTML for a page with badges, find badge links, and check for CSS classes for
    expected badge colors
    """
    app.build()
    assert "build succeeded" in status.getvalue()
    # assert not warning.getvalue().strip()

    build_dir = Path(app.srcdir) / "_build" / "html"
    page_1 = (build_dir / "page_1.html").read_text()
    assert page_1 is not None
    soup = BeautifulSoup(page_1, "html.parser")
    # print(soup.prettify())
    assert soup is not None
    print(soup)
    badge_links = soup.find_all("span", class_="sd-badge")
    print("badge: ", badge_links)

    for (tag, class_), span in zip(EXPECTED_CLASSES.items(), badge_links):
        assert tag in span.text  # hard to test tag 4 b/c of the icon
        assert class_ in span["class"]
