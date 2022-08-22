# How to cut a release

`sphinx-tags` uses [flit]() to manage releases.

To cut a new release:

1. Make sure the version string in `src/sphinx_tags/__init__.py` is updated with
   the release number you want;
2. Run `flit publish` to upload your new version to PyPI.
