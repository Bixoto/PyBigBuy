# PyBigBuy

**PyBigBuy** is a Python client for BigBuy’s REST API.

Note: PyBigBuy is not affiliated to nor endorsed by BigBuy.

## Coverage

PyBigBuy aims to cover all API endpoints. As of 3.15.3+ they are all implemented, except `order/check/multishipping`
and `order/create/multishipping`.

## Install

### Pip

    python -m pip install pybigbuy

### Poetry

    poetry add pybigbuy

## Usage

```python3
from bigbuy import BigBuy


client = BigBuy("your-API-token", "production")
```

## License

Copyright 2020-2022 [Bixoto](https://bixoto.com/).
