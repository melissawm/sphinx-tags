# Changelog
## Version 0.1 (August 23, 2022)

- Includes support for MyST and sphinx-gallery

## Version 0.1.6 (October 9, 2022)

- Added page title and header as a parameter
- Alphabetic sorting of tags
- Added removal of all .md and .rst files in the tag folder before generating them again (avoids having duplicates after removing/changing some tag)
- Tag intro text as a parameter

## Version 0.2.0 (January 26, 2023)

- Added optional integration with sphinx-design badges [gh-35](https://github.com/melissawm/sphinx-tags/pull/35)
- Added support for symlinked sources [gh-37](https://github.com/melissawm/sphinx-tags/pull/37)
- Documentation improvements [gh-41](https://github.com/melissawm/sphinx-tags/pull/41)

## Version 0.2.1 (June 28, 2023)

- Added support for tagging Jupyter Notebooks using `nbsphinx` [gh-51](https://github.com/melissawm/sphinx-tags/pull/51)

## Version 0.3.0

- Fixed tag labels with spaces
- Fixed tag labels with emoji
- Added normalization for tag URLs to remove/replace urlencoded characters
- Exclude files that match `exclude_patterns` from being tagged
