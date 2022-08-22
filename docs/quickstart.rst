Quickstart
==========

The ``sphinx-tags`` package enables the use of blog-style tags with Sphinx.

.. tags:: tagdocumentation, taginstallation

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

      .. note:: This is not yet available.

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

To assign one or more tags to a page in the documentation, use

.. code-block:: rst

   .. tags:: tag1, tag2

Tags must be separated by commas, and the tags will be shown in the rendered
html output at the same position in the page as in the source .rst file.

For each tag, a new rst file is created in ``<output_dir>/<tagname>.rst``
containing a table of contents of each file associated with that tag (see
:ref:`config`).

A :ref:`tagoverview` page is also created that can be added to the index and
show all tags defined for this documentation set.

.. note:: 

   If you are using MyST to write your documentation in Markdown, you can use
   
   ::

      ```{tags} tag1, tag2
      ```

.. note::

   If you are using both ``md`` and ``rst`` files, all generated pages will be
   created as Markdown files.