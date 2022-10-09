.. _config:

Configuration for sphinx-tags
=============================

A few custom configuration keys can be used in your ``conf.py`` file.

- ``tags_create_tags``
  - Whether to process tags or not. Default: ``True``
- ``tags_output_dir``
  - Output directory for the tags source files, relative to the project root.
  Default: ``_tags``
- ``tags_extension``
  - A list of file extensions to inspect. Use ``"rst"`` if you are using pure
  Sphinx, and ``"md"`` if your are using MyST. Note that if you list both
  ``["md", "rst"]``, all generated pages to be created as Markdown files.
  Default: ``["rst"]``
- ``tags_page_title``
  - The title of the tag page, after which the tag is listed.
  Default: ``Tag``
- ``tags_page_header``
  - The string after which the pages with the tag are listed.
  Default: ``With this tag``
- ``tags_index_head``
  - The string used as caption in the tagsindex file.
  Default: ``Tags``
- ``tags_intro_text``
  - The string used on pages that have tags.
  Default: ``Tags``

Tags overview page
------------------

You can customize the title of the tags overview page using the
``tags_overview_title`` key in your ``conf.py`` file. For example,

::

  tags_overview_title = "Site tags"

The default value for this configuration key is "Tags overview".

This page should show you a list of available tags, next to a number describing
how many pages are associated with each tag.

Tags in the sidebar
-------------------

By default, ``sphinx-tags`` will generate a ``toctree`` element for the "Tags
overview" page. This means that if your theme uses a sidebar navigation element,
your tags will appear there.
