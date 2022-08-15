.. _config:

Configuration for sphinx-tags
=============================

A few custom configuration keys can be used in your ``conf.py`` file.

- ``tags_create_tags``
  - Default: ``True``
- ``tags_output_dir``
  - Default: ``_tags``

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

By default, ``sphinx-tags`` will generate a hidden ``toctree`` element for the
"Tags overview" page. This means that if your theme uses a sidebar navigation
element, your tags will appear there.
