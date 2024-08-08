# Contributing to PyBigBuy

## Test endpoints coverage

Run `./endpoints_coverage.sh` to print a diff between endpoints in the API and endpoints implemented in the library.
This helps to detect removed or added endpoints, since BigBuy doesn't announce changes to the API.

## Run tests

    poetry run pytest

## Make a release

1. Update the CHANGELOG
2. Update the version in `pyproject.toml` and in `bigbuy/__init__.py`
3. Commit
4. Tag with `v` + version. For example: `v3.16.0`
5. Push the code and the tag
6. Wait for the [CI job][ci] to finish

[ci]: https://github.com/Bixoto/PyBigBuy/actions
