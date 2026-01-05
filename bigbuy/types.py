import sys
from typing import TypedDict, Union, Any, Optional

if sys.version_info >= (3, 11):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired


class BBImageDict(TypedDict):
    id: int
    isCover: bool
    name: str
    url: str


class BBProductImagesDict(TypedDict):
    """A product ID and a list of images."""
    id: int
    images: list[BBImageDict]


class BBTaxonomyDict(TypedDict):
    id: int
    name: str
    url: str
    parentTaxonomy: int
    dateAdd: str
    dateUpd: str
    urlImages: str
    isoCode: str


class BBProductTaxonomyDict(TypedDict):
    """A link between a product and a taxonomy"""
    id: int
    taxonomy: int
    product: int


class BBLowestShippingCostDict(TypedDict):
    reference: str
    cost: Union[str, None]
    carrierId: str
    carrierName: str


class BBAttributeDict(TypedDict):
    id: int
    attributeGroup: int
    name: str
    isoCode: str


class BBAttributeGroupDict(TypedDict):
    id: int
    name: str
    isoCode: str


class BBProductCategoryDict(TypedDict):
    id: int
    product: int
    category: int
    position: int


class BBProductInformationDict(TypedDict):
    id: int
    sku: str
    name: str
    description: str
    url: str
    isoCode: str
    dateUpdDescription: NotRequired[str]


class BBTrackingCarrierDict(TypedDict):
    id: str
    name: str


class BBOrderStatusDict(TypedDict):
    id: int
    name: str


class BBProductComplianceDict(TypedDict):
    # TODO: better types
    generalProductSafetyRegulations: list[dict[str, Any]]
    id: int
    productComplianceDocuments: list[Any]
    sku: str


class BBProductPriceDict(TypedDict):
    id: int
    sku: str
    wholesalePrice: float
    retailPrice: float
    inShopsPrice: float


class BBStockByHandlingDaysDict(TypedDict):
    quantity: int
    minHandlingDays: int
    maxHandlingDays: int
    warehouse: int


class BBProductStockByHandlingDaysDict(TypedDict):
    id: int
    sku: str
    stocks: list[BBStockByHandlingDaysDict]


class BBTagDict(TypedDict):
    id: int
    name: str
    linkRewrite: str
    language: str


class BBProductTagDict(TypedDict):
    id: int
    sku: str
    tag: BBTagDict


class BBPriceLargeQuantitiesDict(TypedDict):
    id: int
    quantity: int
    price: float


class BBProductVariationDict(TypedDict):
    id: int
    sku: str
    ean13: str
    extraWeight: float
    product: int
    wholesalePrice: float
    retailPrice: float
    inShopsPrice: float
    width: float
    height: float
    depth: float
    priceLargeQuantities: list[BBPriceLargeQuantitiesDict]
    logisticClass: str


# {'id': '43', 'delay': '1-2 jours', 'name': 'Chrono', 'pod': True}
class BBShippingServiceDict(TypedDict):
    id: str
    delay: str
    name: str
    pod: bool


class BBCarrierDict(TypedDict):
    id: str
    name: str
    shippingServices: list[BBShippingServiceDict]


class BBIdDict(TypedDict):
    id: int


class BBVariationDict(TypedDict):
    """Format: {"id":1169758,"attributes":[{"id":24161}]}."""
    id: int
    attributes: list[BBIdDict]


class BBManufacturerDict(TypedDict):
    id: int
    name: str
    urlImage: str
    reference: int


class BBLanguageDict(TypedDict):
    name: str
    isoCode: str


class BBCheckOrderDict(TypedDict):
    totalWithoutTaxesAndWithoutShippingCost: float
    totalWithoutTaxes: float
    total: float


class BBProductDict(TypedDict):
    sku: str
    id: int
    active: int
    attributes: bool
    canon: NotRequired[Optional[float]]
    categories: bool
    category: int
    condition: str
    dateAdd: NotRequired[str]
    dateUpd: str
    dateUpdCategories: NotRequired[Optional[str]]
    dateUpdDescription: NotRequired[str]
    dateUpdProperties: NotRequired[Optional[str]]
    dateUpdImages: NotRequired[str]
    dateUpdStock: NotRequired[str]
    depth: float
    ean13: NotRequired[Optional[str]]
    height: float
    images: bool
    inShopsPrice: float
    intrastat: str
    logisticClass: str
    manufacturer: int
    partNumber: NotRequired[Optional[str]]
    priceLargeQuantities: list[BBPriceLargeQuantitiesDict]
    retailPrice: float
    tags: bool
    taxId: int
    taxRate: int
    taxonomy: int
    video: str
    weight: float
    wholesalePrice: float
    width: float
