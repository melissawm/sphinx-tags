Quickstart
==========

The ``sphinx-tags`` package enables the use of blog-style tags with Sphinx.

.. tags:: tag documentation, tag installation

Tags are created using the custom directive ``.. tags::`` with the tag titles
as arguments.

Installation
------------

Use pip or conda to install ``sphinx-tags``:

.. tab-set::

    .. tab-item:: pip

      .. code-block::

         pip install sphinx-tags

    .. tab-item:: conda

      .. code-block::

         conda install -c conda-forge sphinx-tags

Usage
-----

To enable ``sphinx-tags`` in your documentation, enable the extension on your
``conf.py`` file::

   extensions = [
       ...
       "sphinx_tags",
   ]

Next, add the following configuration setting to ``conf.py``::

   tags_create_tags = True

To assign one or more tags to a page in the documentation, use:

.. tab-set::

    .. tab-item:: rST

      .. code-block:: rst

         .. tags:: tag1, tag2

    .. tab-item:: MyST (Markdown)

      .. code-block:: md

         ```{tags} tag1, tag2
         ```

Tags must be separated by commas, and the tags will be shown in the rendered
html output at the same position in the page as in the source file.

For each tag, a new source file is created in ``<output_dir>/<tagname>.<ext>``
containing a table of contents of each file associated with that tag (see
:ref:`config`). A reference label will be added to this file, to enable you to
cross-reference to it. The reference label will have the format: ``sphx_tag_<tagname>``
e.g., a reference would look like: ``:ref:`sphx_tag_tag1```.

A :ref:`tagoverview` page is also created that can be added to the index and
show all tags defined for this documentation set.

.. note::

   If you are using both ``md`` and ``rst`` files, all generated pages will be
   created as Markdown files.
