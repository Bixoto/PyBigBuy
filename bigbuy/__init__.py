"""
Bigbuy
-------

Bigbuy is a library for Python that wraps the BigBuy API.
"""

__author__ = 'Bixoto <tech@bixoto.com>'
__version__ = '3.24.0'

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
    BBImageDict, BBCheckOrderDict,
    BBLanguageDict,
    BBLowestShippingCostDict,
    BBTaxonomyDict,
    BBTrackingCarrierDict,

    BBProductImagesDict,
    BBProductTaxonomyDict, BBManufacturerDict, BBProductDict, BBProductCategoryDict, BBProductInformationDict,
    BBOrderStatusDict, BBProductComplianceDict, BBProductPriceDict, BBStockByHandlingDaysDict,
    BBProductStockByHandlingDaysDict, BBProductTagDict, BBTagDict, BBPriceLargeQuantitiesDict, BBProductVariationDict,
    BBShippingServiceDict, BBCarrierDict, BBIdDict, BBVariationDict,
)

__all__ = (
    "__author__",
    "__version__",

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
    "BBCarrierDict",
    "BBCheckOrderDict",
    "BBIdDict",
    "BBImageDict",
    "BBLanguageDict",
    "BBLowestShippingCostDict",
    "BBManufacturerDict",
    "BBOrderStatusDict",
    "BBPriceLargeQuantitiesDict",
    "BBProductCategoryDict",
    "BBProductComplianceDict",
    "BBProductDict",
    "BBProductImagesDict",
    "BBProductInformationDict",
    "BBProductPriceDict",
    "BBProductStockByHandlingDaysDict",
    "BBProductTagDict",
    "BBProductTaxonomyDict",
    "BBProductVariationDict",
    "BBShippingServiceDict",
    "BBStockByHandlingDaysDict",
    "BBTagDict",
    "BBTaxonomyDict",
    "BBTrackingCarrierDict",
    "BBVariationDict",
)
