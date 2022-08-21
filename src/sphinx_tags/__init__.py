"""Sphinx extension to create tags for documentation pages.

"""
import os
from sphinx.util.docutils import SphinxDirective
from docutils import nodes

__version__ = "0.0.2dev"

TAGSTART = ".. tags::"


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
            link = os.path.join(self.env.app.config.tags_output_dir, f"{tag}.html")
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
        self.filename = f"{self.name}.rst"

    def create_file(self, path, items):
        """Create rst file with list of documents associated with a given tag.

        This file is reached as a link from the tag name.

        """
        content = []
        content.append(self.name)
        content.append("#" * len(self.name))
        content.append("")
        #  Return link block at the start of the page"""
        content.append(".. toctree::")
        content.append("    :maxdepth: 1")
        content.append("")
        #  items is a list of files associated with this tag
        for item in items:
            link = item.filename
            content.append(f"    {item.title} <../{link}>")
        content.append("")
        with open(os.path.join(path, self.filename), "w", encoding="utf8") as f:
            f.write("\n".join(content))


class Entry:
    """Extracted info from *.rst file.

    We need the path, the title and the tags.

    """
    def __init__(self, filepath, filename):
        self.filename = filename
        self.filepath = os.path.join(filepath, filename)
        with open(self.filepath, "r", encoding="utf8") as f:
            self.lines = f.read().split("\n")
        self.title = self.lines[0].strip()
        tagline = [line for line in self.lines if TAGSTART in line]
        self.tags = []
        if tagline:
            tagline = tagline[0].replace(TAGSTART, "")
            self.tags = tagline.split(",")
            self.tags = [tag.strip() for tag in self.tags]

    def assign_to_tags(self, tag_dict):
        """Append ourself to tags"""
        for tag in self.tags:
            if tag not in tag_dict:
                tag_dict[tag] = Tag(tag)
            tag_dict[tag].items.append(self)


def tagpage(tags, path, title):
    """Creates Tag overview page.

    This page contains a list of all available tags.

    """
    content = []
    content.append(":orphan:")
    content.append("")
    content.append(".. _tagoverview:")
    content.append("")
    content.append(title)
    content.append("#" * len(title))
    content.append("")
    tags = list(tags.values())
    # toctree for the page
    for tag in tags:
        content.append(f"* `{tag.name} ({len(tag.items)}) <{tag.name}.html>`_")
    content.append("")
    # toctree for the left sidebar (hidden)
    content.append(".. toctree::")
    content.append("    :caption: Site tags")
    content.append("    :maxdepth: 1")
    content.append("    :hidden:")
    content.append("")

    for tag in tags:
        content.append(f"    {tag.name} <{tag.name}.rst>")
    content.append("")

    filename = os.path.join(path, "tagsindex.rst")
    with open(filename, "w", encoding="utf8") as f:
        f.write("\n".join(content))


def assign_entries(app):
    """Assign all found entries to their tag."""
    pages = []
    tags = {}
    for entryname in os.listdir(app.srcdir):
        if entryname.endswith(".rst"):
            entry = Entry(app.srcdir, entryname)
            entry.assign_to_tags(tags)
            pages.append(entry)
    return tags, pages


def update_tags(app, config):
    """Update tags according to pages found"""
    if app.config.tags_create_tags:
        path = os.path.join(config.tags_output_dir)
        tags, pages = assign_entries(app)
        if not os.path.exists(path):
            os.makedirs(path)
        for tag in tags.values():
            tag.create_file(path, [item for item in pages if tag.name in item.tags])
        tagpage(tags, path, config.tags_overview_title)
        print("Tags updated")
    else:
        print("Tags were not created (tags_create_tags=False in conf.py)")


def diagnostics(app, env, docnames):
    """Print found docs for debugging purposes"""
    print(f"Diagnostics: {docnames}")


def setup(app):
    """Setup for Sphinx."""

    # Create config keys (with default values)
    # These values will be updated after config-inited
    app.add_config_value('tags_create_tags', False, 'html')
    app.add_config_value('tags_output_dir', '_tags', 'html')
    app.add_config_value('tags_overview_title', 'Tags overview', 'html')
    app.add_config_value('remove_from_toctrees', [app.config.tags_output_dir,], 'html')
    app.connect("config-inited", update_tags)
    app.add_directive("tags", TagLinks)
    # app.connect("env-before-read-docs", diagnostics)

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
