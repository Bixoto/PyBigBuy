"""
Bigbuy
-------

Bigbuy is a library for Python that wraps the BigBuy API.
"""

__author__ = 'Bixoto <tech@bixoto.com>'

from .api import BigBuy
from .exceptions import (
    BBError, BBResponseError, BBPackError, BBExportError, BBProductError, BBStockError,
    BBNoCarrierError, BBBankWireTooLowError, BBMoneyBoxTooLowError, BBTemporaryOrderError, BBOrderAlreadyExistsError,
    BBOrderTooLowError, BBIncorrectRefError, BBInvalidPaymentError, BBZipcodeFormatError, BBProductNotFoundError,
    BBServerError, BBRateLimitError, BBValidationError, BBWarehouseSplitError, BBShippingError, BBTimeoutError,
)
from .rate_limit import RateLimit
from .types import (
    BBAttributeDict, BBAttributeGroupDict, BBImageDict, BBCheckOrderDict, BBLanguageDict, BBLowestShippingCostDict,
    BBTaxonomyDict, BBTrackingCarrierDict, BBProductImagesDict, BBProductTaxonomyDict, BBManufacturerDict,
    BBProductDict, BBProductCategoryDict, BBProductInformationDict, BBOrderStatusDict, BBProductComplianceDict,
    BBProductPriceDict, BBStockByHandlingDaysDict, BBProductStockByHandlingDaysDict, BBProductTagDict, BBTagDict,
    BBPriceLargeQuantitiesDict, BBProductVariationDict, BBShippingServiceDict, BBCarrierDict, BBIntIdDict,
    BBVariationDict,
    BBSplitCheckOrderDict, BBMultiCheckOrderDict, BBOrderCarrierDict, BBOrderProductDict, BBOrderDict, BBSlimOrderDict,
    BBOrderDeliveryNoteDict, BBReferenceQuantityDict, BBStrIdDict, BBTrackingDict, BBTrackingOrderDict,
)
from .version import __version__

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
    "BBImageDict",
    "BBIntIdDict",
    "BBLanguageDict",
    "BBLowestShippingCostDict",
    "BBManufacturerDict",
    "BBMultiCheckOrderDict",
    "BBOrderCarrierDict",
    "BBOrderDeliveryNoteDict",
    "BBOrderDict",
    "BBOrderProductDict",
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
    "BBReferenceQuantityDict",
    "BBShippingServiceDict",
    "BBSlimOrderDict",
    "BBSplitCheckOrderDict",
    "BBStockByHandlingDaysDict",
    "BBStrIdDict",
    "BBTagDict",
    "BBTaxonomyDict",
    "BBTrackingCarrierDict",
    "BBTrackingDict",
    "BBTrackingOrderDict",
    "BBVariationDict",
)
