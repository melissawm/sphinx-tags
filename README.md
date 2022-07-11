# sphinx-tags

A tiny Sphinx extension that implements blog-style tags for documentation.

## Installation

After activating a virtual environment manager such as `venv` or `conda`, use

```
python -m pip install sphinx-tags
```

## Usage

Refer to the [documentation](https://sphinx-tags.readthedocs.io/en/latest/) for usage instructions.

## Contributing

Feel free to submit issues or PRs - keep in mind this is experimental!

### Setup for development

After cloning this repo and activating a virtual environment manager such as
`venv` or `conda`, use

```
python -m pip install -e ".[sphinx]"
```

To build the documentation locally, use

```
sphinx-build docs docs/_build/html
```

## Code of Conduct

All contributors and maintainers are expected to follow the
[PSF Code of Conduct](https://github.com/psf/community-code-of-conduct).

## Notes

This is loosely based on [this StackOverflow answer](https://stackoverflow.com/questions/18146107/how-to-add-blog-style-tags-in-restructuredtext-with-sphinx).
