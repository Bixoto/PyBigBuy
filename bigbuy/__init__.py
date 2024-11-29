"""
Bigbuy
-------

Bigbuy is a library for Python that wraps the BigBuy API.
"""

__author__ = 'Bixoto <tech@bixoto.com>'
__version__ = '3.21.0'

from .api import BigBuy
from .exceptions import (
    BBError, BBResponseError, BBPackError, BBExportError, BBProductError, BBStockError,
    BBNoCarrierError, BBBankWireTooLowError, BBMoneyBoxTooLowError, BBTemporaryOrderError, BBOrderAlreadyExistsError,
    BBOrderTooLowError, BBIncorrectRefError, BBInvalidPaymentError, BBZipcodeFormatError, BBProductNotFoundError,
    BBServerError, BBRateLimitError, BBValidationError, BBWarehouseSplitError, BBShippingError, BBTimeoutError,
)
from .rate_limit import RateLimit
from .types import (
    BBAttributeDict,
    BBAttributeGroupDict,
    BBImageDict,
    BBLowestShippingCostDict,
    BBTaxonomyDict,

    BBProductImagesDict,
    BBProductTaxonomyDict,
)

__all__ = (
    "BigBuy",
    "BBError",
    "BBResponseError",
    "BBPackError",
    "BBExportError",
    "BBProductError",
    "BBStockError",
    "BBNoCarrierError",
    "BBBankWireTooLowError",
    "BBMoneyBoxTooLowError",
    "BBTemporaryOrderError",
    "BBOrderAlreadyExistsError",
    "BBOrderTooLowError",
    "BBIncorrectRefError",
    "BBInvalidPaymentError",
    "BBZipcodeFormatError",
    "BBProductNotFoundError",
    "BBServerError",
    "BBRateLimitError",
    "BBValidationError",
    "BBWarehouseSplitError",
    "BBShippingError",
    "BBTimeoutError",
    "RateLimit",

    "BBAttributeDict",
    "BBAttributeGroupDict",
    "BBImageDict",
    "BBLowestShippingCostDict",
    "BBTaxonomyDict",
    "BBProductImagesDict",
    "BBProductTaxonomyDict",
)
