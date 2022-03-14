"""
Bigbuy
-------

Bigbuy is a library for Python that wraps the BigBuy API.
"""

__author__ = 'Bixoto <info@bixoto.com>'
__version__ = '3.9.0'

from .api import BigBuy
from .exceptions import (
    BBError, BBResponseError, BBPackError, BBExportError, BBProductError, BBStockError,
    BBNoCarrierError, BBBankWireTooLowError, BBMoneyBoxTooLowError, BBTemporaryOrderError, BBOrderAlreadyExistsError,
    BBOrderTooLowError, BBIncorrectRefError, BBInvalidPaymentError, BBZipcodeFormatError, BBProductNotFoundError,
    BBServerError, BBRateLimitError, BBValidationError,
)
