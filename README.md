# PyBigBuy

**PyBigBuy** is a Python client for BigBuy’s REST API.

Note: PyBigBuy is not affiliated to nor endorsed by BigBuy.

## Coverage

Starting with 3.17.0 PyBigBuy implements all API endpoints.
We release new versions of the API client each time there are new or modified endpoints.

## Install

Requirements:
* From PyBigBuy 3.21.0: Python 3.9+
* Up to 3.20.1: Python 3.8+

### Pip

    python -m pip install pybigbuy

### Poetry

    poetry add pybigbuy

## Usage

```python3
from bigbuy import BigBuy


client = BigBuy("your-API-token")
```

## License

Copyright 2020-2024 [Bixoto](https://bixoto.com/).
