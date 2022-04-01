# Contributing to PyBigBuy

## Run tests

    poetry run pytest

## Making a release

1. Update the CHANGELOG
2. Update the version in `pyproject.toml` and in `bigbuy/__init__.py`
3. Commit
5. Tag
6. Push the code and the tag
7. Wait for the [CI job][ci] to finish

[ci]: https://gitlab.com/bixoto/pybigbuy/-/jobs
