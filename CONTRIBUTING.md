# Contributing to PyBigBuy

## Run tests

    poetry run pytest

## Making a release

1. Update the CHANGELOG
2. Update the version in `pyproject.toml` and in `bigbuy/__init__.py`
3. Commit
4. Tag
5. Push the code and the tag
6. Wait for the [CI job][ci] to finish

[ci]: https://gitlab.com/bixoto/pybigbuy/-/jobs
