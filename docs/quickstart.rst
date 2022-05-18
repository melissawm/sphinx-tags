Quickstart
==========

The ``sphinx-tags`` package enables the use of blog-style tags with Sphinx.

.. tags:: documentation, installation

Tags are created using the custom directive ``.. tags::`` with the tag titles
as arguments.

Installation
------------

Use pip or conda to install ``sphinx-tags``:

.. tabs::

   .. tab:: pip

      .. code-block::

         pip install sphinx-tags

   .. tab:: conda

      .. note:: This is not yet available.

      .. code-block::

         conda install -c conda-forge sphinx-tags

Usage
-----

To assign one or more tags to a page in the documentation, use

.. code-block::

   .. tags:: tag1, tag2

Tags must be separated by commas, and the tags will be shown in the rendered
html output at the same position in the page as in the source .rst file.

For each tag, a new rst file is created in ``tags/<tagname>.rst`` containing a
table of contents of each file associated with that tag.

A :ref:`tagoverview` page is also created that can be added to the index and show
all tags defined for this documentation set.
