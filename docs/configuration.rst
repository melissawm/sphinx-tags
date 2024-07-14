.. _config:

Configuration
=============

A few custom configuration keys can be used in your ``conf.py`` file.

- ``tags_create_tags``
  - Whether to process tags or not. **Default:** ``False``
- ``tags_output_dir``
  - Output directory for the tags source files, relative to the project root.
  **Default:** ``_tags``
- ``tags_extension``
  - A list of file extensions to inspect. Use ``"rst"`` if you are using pure
  Sphinx, and ``"md"`` if your are using MyST. Note that if you list both
  ``["md", "rst"]``, all generated pages to be created as Markdown files.
  **Default:** ``["rst"]``
- ``tags_intro_text``
  - The string used on pages that have tags. **Default:** ``Tags``
- ``tags_page_title``
  - The title of the tag page, after which the tag is listed. **Default:**
  ``My tags``
- ``tags_page_header``
  - The string after which the pages with the tag are listed. **Default:**
  ``With this tag``
- ``tags_index_head``
  - The string used as caption in the tagsindex file. **Default:** ``Tags``
- ``tags_create_badges``
  - Whether to display tags using sphinx-design badges. **Default:** ``False``
- ``tags_badge_colors``
  - Colors to use for badges based on tag name. **Default:** ``{}``


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

Tag badges
----------
If you also use the `sphinx-design <https://sphinx-design.readthedocs.io>`_ extension,
you can optionally use its `badges <https://sphinx-design.readthedocs.io/en/latest/badges_buttons.html#badges>`_
to display tags. To enable this, set ``tags_create_badges = True`` in ``conf.py``.

Badge Colors
~~~~~~~~~~~~

You can also define which colors to use, based on the tag name. This can be defined
in ``tags_badge_colors``, which should be a dict mapping tag names to colors.

Color values may be one of:

* ``None`` (plain badge): :bdg:`plain`
* ``'primary'``: :bdg-primary:`primary`
* ``'secondary'``: :bdg-secondary:`secondary`
* ``'success'``: :bdg-success:`success`
* ``'info'``: :bdg-info:`info`
* ``'warning'``: :bdg-warning:`warning`
* ``'danger'``: :bdg-danger:`danger`
* ``'light'``: :bdg-light:`light`
* ``'dark'``: :bdg-dark:`dark`

Example::

  tags_create_badges = True
  tags_badge_colors = {
      "tag1": "primary",
      "tag2": "secondary",
      "tag3": "success",
  }

Which will result in badges like this:
:bdg-primary:`tag1` :bdg-secondary:`tag2` :bdg-success:`tag3`

You may also use glob patterns to match multiple tags::

  tags_badge_colors = {
      "tag_*": "primary",
      "status:*": "warning",
      "*": "dark",  # Used as a default value
  }

This will result in badges like this:
:bdg-primary:`tag_1` :bdg-primary:`tag_2` :bdg-warning:`status:done` :bdg-dark:`other`

Special characters
------------------

Tags can contain spaces and special characters such as emoji. In that case, the
tag will be normalized when processed. See our :doc:`examples/examples` for more details.

Usage with sphinx-autobuild
---------------------------

`Sphinx-autobuild <https://github.com/sphinx-doc/sphinx-autobuild>`_ is a live-reload
tool for local development that automatically rebuilds your docs when changes are
detected. Sphinx-tags dynamically generates a tag overview and tag index pages
during each build, so you will want to tell sphinx-autobuild to ignore these
files so it doesn't get stuck in a loop. Example:

.. code-block:: sh

    sphinx-autobuild docs docs/_build/html --ignore '**/_tags/*'

If you have set ``tags_output_dir`` to a different path, use that instead of ``_tags``.

.. tags:: tag documentation
