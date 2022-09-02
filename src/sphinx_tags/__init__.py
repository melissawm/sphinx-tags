"""Sphinx extension to create tags for documentation pages.

"""
import os
from sphinx.util.logging import getLogger
from sphinx.util.docutils import SphinxDirective
from docutils import nodes
from pathlib import Path

__version__ = "0.1.5"

logger = getLogger("sphinx-tags")


class TagLinks(SphinxDirective):
    """Custom directive for adding tags to Sphinx-generated files.

    Loosely based on https://stackoverflow.com/questions/18146107/how-to-add-blog-style-tags-in-restructuredtext-with-sphinx

    See also https://docutils.sourceforge.io/docs/howto/rst-directives.html

    """

    # Sphinx directive class attributes
    required_arguments = 1
    optional_arguments = 200  # Arbitrary.
    has_content = False

    # Custom attributes
    separator = ","
    intro_text = "Tags: "

    def run(self):
        tags = [arg.replace(self.separator, "") for arg in self.arguments]
        result = nodes.paragraph()
        result["classes"] = ["tags"]
        result += nodes.inline(text=self.intro_text)
        count = 0
        for tag in tags:
            count += 1
            # We want the link to be the path to the _tags folder, relative to this document's path
            # where
            #
            #  - self.env.app.config.tags_output_dir
            # |
            #  - subfolder
            #   |
            #    - current_doc_path
            docpath = Path(self.env.doc2path(self.env.docname)).parent
            rootdir = os.path.relpath(
                os.path.join(self.env.app.srcdir, self.env.app.config.tags_output_dir),
                docpath,
            )
            link = os.path.join(rootdir, f"{tag}.html")
            tag_node = nodes.reference(refuri=link, text=tag)
            result += tag_node
            if not count == len(tags):
                result += nodes.inline(text=f"{self.separator} ")
        return [result]


class Tag:
    """A tag contains entries"""

    def __init__(self, name):
        self.name = name
        self.items = []

    def create_file(self, items, extension, tags_output_dir, srcdir):
        """Create file with list of documents associated with a given tag in
        toctree format.

        This file is reached as a link from the tag name in each documentation
        file, or from the tag overview page.

        If we are using md files, generate and md file; otherwise, go with rst.

        Parameters
        ----------

        tags_output_dir : Path
            path where the file for this tag will be created
        items : list
            list of files associated with this tag (instance of Entry)
        extension : {["rst"], ["md"], ["rst", "md"]}
            list of file extensions used.
        srcdir : str
            root folder for the documentation (usually, project/docs)

        """
        content = []
        if "md" in extension:
            filename = f"{self.name}.md"
            content.append(f"# Tag: {self.name}")
            content.append("")
            content.append("```{toctree}")
            content.append("---")
            content.append("maxdepth: 1")
            content.append("caption: With this tag")
            content.append("---")
            #  items is a list of files associated with this tag
            for item in items:
                # We want here the filepath relative to /docs/_tags
                relpath = item.filepath.relative_to(srcdir)
                content.append(f"../{relpath}")
            content.append("```")
        else:
            filename = f"{self.name}.rst"
            content.append(f"Tag: {self.name}")
            content.append("#" * len(self.name) + "#####")
            content.append("")
            #  Return link block at the start of the page"""
            content.append(".. toctree::")
            content.append("    :maxdepth: 1")
            content.append("    :caption: With this tag")
            content.append("")
            #  items is a list of files associated with this tag
            for item in items:
                # We want here the filepath relative to /docs/_tags
                relpath = item.filepath.relative_to(srcdir)
                content.append(f"    ../{relpath}")

        content.append("")
        with open(
            os.path.join(srcdir, tags_output_dir, filename), "w", encoding="utf8"
        ) as f:
            f.write("\n".join(content))


class Entry:
    """Extracted info from source file (*.rst/*.md)"""

    def __init__(self, entrypath):
        self.filepath = entrypath
        with open(self.filepath, "r", encoding="utf8") as f:
            self.lines = f.read().split("\n")
        if self.filepath.name.endswith(".rst"):
            tagstart = ".. tags::"
            tagend = ""
        elif self.filepath.name.endswith(".md"):
            tagstart = "```{tags}"
            tagend = "```"
        tagline = [line for line in self.lines if tagstart in line]
        self.tags = []
        if tagline:
            tagline = tagline[0].replace(tagstart, "").rstrip(tagend)
            self.tags = tagline.split(",")
            self.tags = [tag.strip() for tag in self.tags]

    def assign_to_tags(self, tag_dict):
        """Append ourself to tags"""
        for tag in self.tags:
            if tag not in tag_dict:
                tag_dict[tag] = Tag(tag)
            tag_dict[tag].items.append(self)


def tagpage(tags, outdir, title, extension):
    """Creates Tag overview page.

    This page contains a list of all available tags.

    """
    tags = list(tags.values())

    if "md" in extension:
        content = []
        content.append("(tagoverview)=")
        content.append("")
        content.append(f"# {title}")
        content.append("")
        # toctree for this page
        content.append("```{toctree}")
        content.append("---")
        content.append("caption: Tags")
        content.append("maxdepth: 1")
        content.append("---")
        for tag in tags:
            content.append(f"{tag.name} ({len(tag.items)}) <{tag.name}>")
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
        content.append("#" * len(title))
        content.append("")
        # toctree for the page
        content.append(".. toctree::")
        content.append("    :caption: Tags")
        content.append("    :maxdepth: 1")
        content.append("")
        for tag in tags:
            content.append(f"    {tag.name} ({len(tag.items)}) <{tag.name}.rst>")
        content.append("")
        filename = os.path.join(outdir, "tagsindex.rst")

    with open(filename, "w", encoding="utf8") as f:
        f.write("\n".join(content))


def assign_entries(app):
    """Assign all found entries to their tag."""
    pages = []
    tags = {}
    result = []
    for extension in app.config.tags_extension:
        result.extend(list(Path(app.srcdir).rglob(f"*.{extension}")))
    for entrypath in result:
        entry = Entry(entrypath)
        entry.assign_to_tags(tags)
        pages.append(entry)
    return tags, pages


def update_tags(app):
    """Update tags according to pages found"""
    if app.config.tags_create_tags:
        tags_output_dir = Path(app.config.tags_output_dir)
        if not os.path.exists(os.path.join(app.srcdir, tags_output_dir)):
            os.makedirs(os.path.join(app.srcdir, tags_output_dir))

        # Create pages for each tag
        tags, pages = assign_entries(app)
        for tag in tags.values():
            tag.create_file(
                [item for item in pages if tag.name in item.tags],
                app.config.tags_extension,
                tags_output_dir,
                app.srcdir,
            )
        # Create tags overview page
        tagpage(
            tags,
            os.path.join(app.srcdir, tags_output_dir),
            app.config.tags_overview_title,
            app.config.tags_extension,
        )
        logger.info("Tags updated", color="white")
    else:
        logger.info(
            "Tags were not created (tags_create_tags=False in conf.py)", color="white"
        )


def setup(app):
    """Setup for Sphinx."""

    # Create config keys (with default values)
    # These values will be updated after config-inited

    app.add_config_value("tags_create_tags", False, "html")
    app.add_config_value("tags_output_dir", "_tags", "html")
    app.add_config_value("tags_overview_title", "Tags overview", "html")
    app.add_config_value("tags_extension", ["rst"], "html")
    # internal config values
    app.add_config_value(
        "remove_from_toctrees",
        [
            app.config.tags_output_dir,
        ],
        "html",
    )

    # Update tags
    # TODO: tags should be updated after sphinx-gallery is generated, and the
    # gallery is also connected to builder-inited. Are there situations when
    # this will not work?
    app.connect("builder-inited", update_tags)
    app.add_directive("tags", TagLinks)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
