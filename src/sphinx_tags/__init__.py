"""Sphinx extension to create tags for documentation pages.

"""

from sphinx.domains import Domain, Index, IndexEntry
from sphinx.util.logging import getLogger
from sphinx.util.docutils import SphinxDirective
from sphinx.errors import ExtensionError
from sphinx.util.rst import textwidth

# from sphinx.addnodes import pending_xref
from sphinx.builders import Builder

from pathlib import Path
from docutils import nodes
import os
from typing import List
from fnmatch import fnmatch
import re
from collections.abc import Iterable
from collections import defaultdict

__version__ = "1.0dev"

logger = getLogger("sphinx-tags")


class TagLinks(SphinxDirective):
    """Custom directive for adding tags to Sphinx-generated files.

    Loosely based on https://stackoverflow.com/questions/18146107/how-to-add-blog-style-tags-in-restructuredtext-with-sphinx

    See also https://docutils.sourceforge.io/docs/howto/rst-directives.html

    This directive can be used with arguments and with content.

    1. With arguments:

        .. raw:: rst
            .. tags:: tag1, tag2, tag3

    2. With (multiline) content:

        .. raw:: rst
            .. tags::

                tag1, tag2,
                tag3
    """

    # Sphinx directive class attributes
    required_arguments = 0
    optional_arguments = 1  # Arbitrary, split on separator
    final_argument_whitespace = True
    has_content = True
    separator = ","

    def run(self):
        if not (self.arguments or self.content):
            raise ExtensionError("No tags passed to 'tags' directive.")

        page_tags = []
        # normalize white space and remove "\n"
        if self.arguments:
            page_tags.extend(
                [_normalize_display_tag(tag) for tag in self.arguments[0].split(",")]
            )
        if self.content:
            # self.content: StringList(['different, tags,', 'separated'],
            #                          items=[(path, lineno), (path, lineno)])
            page_tags.extend(
                [
                    _normalize_display_tag(tag)
                    for tag in ",".join(self.content).split(",")
                ]
            )

        # Remove empty elements from page_tags
        # (can happen after _normalize_tag())
        page_tags = list(filter(None, page_tags))
        global_tags = self.env.get_domain("tags")
        # Append this document to the list of documents containing this tag
        for tag in page_tags:
            global_tags.add_tag(tag, self.env.docname)

        tag_dir = Path(self.env.app.srcdir) / self.env.app.config.tags_output_dir

        # sphinx.addnodes.pending_xref(rawsource="", *children, **attributes)
        result = nodes.paragraph()
        result["classes"] = ["tags"]
        result += nodes.inline(text=f"{self.env.app.config.tags_intro_text} ")
        count = 0

        current_doc_dir = Path(self.env.doc2path(self.env.docname)).parent
        relative_tag_dir = Path(os.path.relpath(tag_dir, current_doc_dir))
        for tag in page_tags:
            count += 1
            # We want the link to be the path to the _tags folder, relative to
            # this document's path where
            #
            #  - self.env.app.config.tags_output_dir
            # |
            #  - subfolder
            #   |
            #    - current_doc_path

            file_basename = _normalize_tag(tag, dashes=True)

            if self.env.app.config.tags_create_badges:
                result += self._get_badge_node(tag, file_basename, relative_tag_dir)
                tag_separator = " "
            else:
                result += self._get_plaintext_node(tag, file_basename, relative_tag_dir)
                tag_separator = f"{self.separator} "
            if not count == len(page_tags):
                result += nodes.inline(text=tag_separator)

        td = self.env.get_domain("tags")
        td.add_tagpage(self.env.docname, page_tags)

        return [result]

    def _get_plaintext_node(
        self, tag: str, file_basename: str, relative_tag_dir: Path
    ) -> List[nodes.Node]:
        """Get a plaintext reference link for the given tag"""
        link = relative_tag_dir / f"{file_basename}.html"
        # return pending_xref(refuri=str(link), text=tag)
        return nodes.reference(refuri=str(link), text=tag)

    def _get_badge_node(
        self, tag: str, file_basename: str, relative_tag_dir: Path
    ) -> List[nodes.Node]:
        """Get a sphinx-design reference badge for the given tag"""
        from sphinx_design.badges_buttons import XRefBadgeRole

        # Required to set Inliner state, since we're directly creating a role object.
        # Typically this would be done when parsing the role from document text.
        text_nodes, messages = self.state.inline_text("", self.lineno)

        # Ref paths always use forward slashes, even on Windows
        tag_ref = f"{tag} <{relative_tag_dir.as_posix()}/{file_basename}.html>"
        tag_color = self._get_tag_color(tag)
        tag_badge = XRefBadgeRole(tag_color)
        return tag_badge(
            name=f"bdg-ref-{tag_color}",
            rawtext=tag,
            text=tag_ref,
            lineno=self.lineno,
            inliner=self.state.inliner,
        )[0]

    def _get_tag_color(self, tag: str) -> str:
        """Check for a matching user-defined color for a given tag.
        Defaults to theme's primary color.
        """
        tag_colors = self.env.app.config.tags_badge_colors or {}
        for pattern, color in tag_colors.items():
            if fnmatch(tag, pattern):
                return color
        return "primary"


class TagsIndex(Index):
    """A custom index that creates a page with all tags and corresponding pages
    where they are defined.
    """

    name = "index"
    localname = "All tags"
    shortname = "TagsIndex"

    def generate(
        self, docnames: Iterable[str] | None = None
    ) -> tuple[list[tuple[str, list[IndexEntry]]], bool]:
        content = defaultdict(list)

        # sort the list of pages
        pages = sorted(self.domain.get_objects(), key=lambda page: page[0])

        # name, subtype, docname, anchor, extra, qualifier, description
        for _name, dispname, typ, docname, anchor, _priority in pages:
            content[dispname[0].lower()].append(
                (dispname, 0, docname, anchor, docname, "", typ)
            )

        # convert the dict to the sorted list of tuples expected
        return sorted(content.items()), True


class TagsDomain(Domain):

    name = "tags"
    label = "Tags"

    roles = {}

    directives = {
        "tags": TagLinks,
    }

    indices = [TagsIndex]

    # The values defined in initial_data will be copied to
    # env.domaindata[domain_name] as the initial data of the domain, and domain
    # instances can access it via self.data.
    initial_data = {
        "tags": [],  # list of tags
        "entries": {},  # list of pages with tags
        "pages": [],  # list of tag pages
    }

    def get_full_qualified_name(self, node):
        # print(f"Node: {node}")
        return f"tags.{node.arguments[0]}"

    def get_objects(self):
        yield from self.data["tags"]

    def add_tag(self, tagname, page):
        """Add a new tag to the domain."""
        anchor = f"{tagname}"

        # Add this page to the list of pages with this tag
        if self.data["entries"].get(tagname) is None:
            self.data["entries"][tagname] = [page]
        else:
            self.data["entries"][tagname].append(page)

        # Add this tag to the global list of tags
        # name, dispname, type, docname, anchor, priority
        self.data["tags"].append((tagname, tagname, "Tag", page, anchor, 0))
        # Create pages for each tag
        create_file(
            (tagname, self.data["entries"][tagname]),
            # self.app.config.tags_extension,
            ".md",
            # Path(self.app.config.tags_output_dir),
            Path("_tags"),
            # self.app.srcdir,
            Path("docs"),
            # self.app.config.tags_page_title,
            "My tags",
            # self.app.config.tags_page_header,
            "With this tag",
            # self.app.config.tags_intro_text
            "Tags:",
        )

    def add_tagpage(self, docname, tags):
        """Add a new page of tags to domain"""
        name = f"index.{docname}"
        anchor = f"index-{docname}"

        # name, dispname, type, docname, anchor, priority
        self.data["pages"].append(
            (name, docname, "TagsIndex", self.env.docname, anchor, 0)
        )


def create_file(
    tag: tuple,
    extension: List[str],
    tags_output_dir: Path,
    srcdir: str,
    tags_page_title: str,
    tags_page_header: str,
    tag_intro_text: str,
):
    """Create file with list of documents associated with a given tag in
    toctree format.

    This file is reached as a link from the tag name in each documentation
    file, or from the tag overview page.

    If we are using md files, generate and md file; otherwise, go with rst.

    Parameters
    ----------

    tag : tuple
        tag name and list of pages associated with this tag
    extension : {["rst"], ["md"], ["rst", "md"]}
        list of file extensions used.
    tags_output_dir : Path
        path where the file for this tag will be created
    srcdir : str
        root folder for the documentation (usually, project/docs)
    tags_page_title: str
        the title of the tag page, after which the tag is listed (e.g. "Tag: programming")
    tags_page_header: str
        the words after which the pages with the tag are listed (e.g. "With this tag: Hello World")
    tag_intro_text: str
        the words after which the tags of a given page are listed (e.g. "Tags: programming, python")
    """

    # Get sorted file paths for tag pages, relative to /docs/_tags
    file_basename = _normalize_tag(tag[0], dashes=True)
    name = _normalize_display_tag(tag[0])
    tag_page_paths = sorted([os.path.relpath(i, srcdir) for i in tag[1]])
    ref_label = f"sphx_tag_{file_basename}"

    content = []
    if "md" in extension:
        filename = f"{file_basename}.md"
        content.append(f"({ref_label})=")
        content.append(f"# {tags_page_title}: {name}")
        content.append("")
        content.append("```{toctree}")
        content.append("---")
        content.append("maxdepth: 1")
        content.append(f"caption: {tags_page_header}")
        content.append("---")
        for path in tag_page_paths:
            content.append(f"../{path}")
        content.append("```")
    else:
        filename = f"{file_basename}.rst"
        header = f"{tags_page_title}: {name}"
        content.append(f".. _{ref_label}:")
        content.append("")
        content.append(header)
        content.append("#" * textwidth(header))
        content.append("")
        content.append(".. toctree::")
        content.append("    :maxdepth: 1")
        content.append(f"    :caption: {tags_page_header}")
        content.append("")
        for path in tag_page_paths:
            content.append(f"    ../{path}")

    content.append("")
    with open(
        os.path.join(srcdir, tags_output_dir, filename), "w", encoding="utf8"
    ) as f:
        f.write("\n".join(content))


def _normalize_tag(tag: str, dashes: bool = False) -> str:
    """Normalize a tag name to use in output filenames and tag URLs.
    Replace whitespace and other non-alphanumeric characters with dashes.

    Example: 'Tag:with (special   characters) ' -> 'tag-with-special-characters'
    """
    char = " "
    if dashes:
        char = "-"
    return re.sub(r"[\s\W]+", char, tag).lower().strip(char)


def _normalize_display_tag(tag: str) -> str:
    """Strip extra whitespace from a tag name for display purposes.

    Example: '  Tag:with (extra   whitespace) ' -> 'Tag:with (extra whitespace)'
    """
    tag = tag.replace("\\n", "\n").strip('"').strip()
    return re.sub(r"\s+", " ", tag)


def tagpage(tags, outdir, title, extension, tags_index_head):
    """Creates Tag overview page.

    This page contains a list of all available tags.

    """
    if "md" in extension:
        content = []
        content.append("(tagoverview)=")
        content.append("")
        content.append(f"# {title}")
        content.append("")
        # toctree for this page
        content.append("```{toctree}")
        content.append("---")
        content.append(f"caption: {tags_index_head}")
        content.append("maxdepth: 1")
        content.append("---")
        content.append("PLACEHOLDER")
        content.append("```")
        content.append("")
        filename = os.path.join(outdir, "tagsindex.md")
    else:
        content = []
        content.append(":orphan:")
        content.append("")
        content.append(".. _tagoverview:")
        content.append("")
        content.append(title)
        content.append("#" * textwidth(title))
        content.append("")
        # toctree for the page
        content.append(".. toctree::")
        content.append(f"    :caption: {tags_index_head}")
        content.append("    :maxdepth: 1")
        content.append("")
        content.append("")  # placeholder
        content.append("")
        filename = os.path.join(outdir, "tagsindex.rst")

    with open(filename, "w", encoding="utf8") as f:
        f.write("\n".join(content))


def update_tags(app, env):
    """Update tags according to pages found"""
    if app.config.tags_create_tags:
        tags_output_dir = Path(app.config.tags_output_dir)
        # Create pages for each tag
        global_tags = app.env.get_domain("tags").data["entries"]
        # Inject these into found_docs
        for docname, tags in global_tags.items():
            env.found_docs.add(docname)
        # Inject these into the tagsindex
        tags_output_dir = Path(app.config.tags_output_dir)
        outdir = os.path.join(app.srcdir, tags_output_dir)
        newcontent = []
        if "md" in app.config.tags_extension:
            filename = os.path.join(outdir, "tagsindex.md")
            taglist = "{name} ({len}) <{file_basename}>"
        else:
            filename = os.path.join(outdir, "tagsindex.rst")
            taglist = "    {name} ({len}) <{file_basename}.rst>"

        for name, pages in global_tags.items():
            file_basename = _normalize_tag(name, dashes=True)
            newcontent.append(
                taglist.format(name=name, len=len(pages), file_basename=file_basename)
            )
        with open(filename, "r", encoding="utf8") as f:
            content = f.read()
        with open(filename, "w", encoding="utf8") as f:
            f.write(content.replace("PLACEHOLDER", "\n".join(newcontent)))
    else:
        logger.info(
            "Tags were not created (tags_create_tags=False in conf.py)", color="white"
        )
    logger.info("Tags updated", color="white")

    # Re-read files, create doctrees and add to env.found_docs and return
    # iterable of docnames to re-read for env-get-updated
    app.builder.read()
    return env.found_docs


def prepare_tags(app):
    if app.config.tags_create_tags:
        tags_output_dir = Path(app.config.tags_output_dir)

        if not os.path.exists(os.path.join(app.srcdir, tags_output_dir)):
            os.makedirs(os.path.join(app.srcdir, tags_output_dir))

        # Create tags overview page
        tagpage(
            [],
            os.path.join(app.srcdir, tags_output_dir),
            app.config.tags_overview_title,
            app.config.tags_extension,
            app.config.tags_index_head,
        )

        logger.info("Tags output dir created", color="green")
    else:
        logger.info(
            "Tags were not created (tags_create_tags=False in conf.py)", color="red"
        )


def setup(app):
    """Setup for Sphinx."""

    # Create config keys (with default values)
    # These values will be updated after config-inited

    app.add_config_value("tags_create_tags", False, "html")
    app.add_config_value("tags_output_dir", "_tags", "html")
    app.add_config_value("tags_overview_title", "Tags overview", "html")
    app.add_config_value("tags_extension", ["rst"], "html")
    app.add_config_value("tags_intro_text", "Tags:", "html")
    app.add_config_value("tags_page_title", "My tags", "html")
    app.add_config_value("tags_page_header", "With this tag", "html")
    app.add_config_value("tags_index_head", "Tags", "html")
    app.add_config_value("tags_create_badges", False, "html")
    app.add_config_value("tags_badge_colors", {}, "html")

    # internal config values
    app.add_config_value(
        "remove_from_toctrees",
        [
            app.config.tags_output_dir,
        ],
        "html",
    )

    # Tags should be updated after sphinx-gallery is generated, on
    # builder-inited
    app.connect("builder-inited", prepare_tags)
    app.connect("env-get-updated", update_tags)
    app.add_directive("tags", TagLinks)
    app.add_domain(TagsDomain)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
        "env_version": 1,
    }
