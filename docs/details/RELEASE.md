# How to cut a release

`sphinx-tags` uses [flit](https://github.com/pypa/flit) to manage releases.

```{tags} development
```

To cut a new release:

1. Make sure the version string in `src/sphinx_tags/__init__.py` is updated with
   the release number you want.
2. Run `flit publish` to upload your new version to PyPI.
3. Run `git tag <version>`, and `git push origin --tags` to update the tags on
   GitHub.
4. Make a new release using the GitHub interface.
