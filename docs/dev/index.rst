.. tags:: development

Contribute
==========

All contributions are welcome in ``sphinx-tags``! All contributors and
maintainers are expected to follow the `PSF Code of Conduct
<https://github.com/psf/community-code-of-conduct>`__.


If you want to point out existing problems or suggest enhancements to code or
documentation, please `open an issue on GitHub
<https://github.com/melissawm/sphinx-tags/issues>`__.

If you want to submit a Pull Request with a patch or new feature, make sure you
follow the guide below.

Pull request guidelines
-----------------------

1. **Set up your development environment**

   After cloning this repo and activating a virtual environment manager such as
   `venv` or `conda`, use

   ::

     python -m pip install -e ".[dev,sphinx]"

   To build the documentation locally, use

   ::

     sphinx-build docs docs/_build/html

2. **Hack away!**

3. **Style checks**

   ``sphinx-tags`` uses `pre-commit <https://pre-commit.com/>`__, and code is
   formatted according to `black <https://github.com/psf/black>`__. To make sure
   your code conforms to this style, you can:

   - Setup pre-commit for your local clone::

      pre-commit install

   - Run pre-commit::

      pre-commit run --all

   - Re-add any changed files to your staging area and run pre-commit again to
     make sure any fixes are applied to your code.

4. **Test Coverage**

    For any new or changed behavior, please add unit test coverage. See notes in
    `conftest.py <https://github.com/melissawm/sphinx-tags/tree/main/test/conftest.py>`__
    for details on testing setup.

5. **Commit your changes and send your pull request as usual.**

Releases
--------

``sphinx-tags`` uses `flit <https://github.com/pypa/flit>`__ to manage releases.

To cut a new release:

1. Make sure the version string in ``src/sphinx_tags/__init__.py`` is updated
   with the release number you want.
2. Run ``flit publish`` to upload your new version to PyPI.
3. Run ``git tag <version>``, and ``git push origin --tags`` to update the tags
   on GitHub.
4. Make a new release using the GitHub interface.
