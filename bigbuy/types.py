import sys
from typing import TypedDict, Union

from api_session import JSONDict

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


# TODO
BBCategoryDict = JSONDict
BBLanguageDict = JSONDict
BBManufacturerDict = JSONDict
BBProductDict = JSONDict
