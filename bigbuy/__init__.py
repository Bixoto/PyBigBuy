"""
Bigbuy
-------

Bigbuy is a library for Python that wraps the BigBuy API.
"""

__author__ = 'Lugh <jbc@bixoto.com>'
__version__ = '0.0.1'

from .api import BigBuy
from .exceptions import (
    BBError, BBResponseError, BBSSLEndpointError, BBPackError, BBExportError, BBProductError, BBStockError,
    BBNoCarrierError, BBBankWireTooLowError, BBMoneyBoxTooLowError, BBTemporaryOrderError, BBOrderAlreadyExistsError,
    BBOrderTooLowError, BBIncorrectRefError, BBInvalidPaymentError, BBZipcodeFormatError, BBProductNotFoundError,
)