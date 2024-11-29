from typing import TypedDict, Union, List


class BBImageDict(TypedDict):
    id: int
    isCover: bool
    name: str
    url: str


class BBProductImagesDict(TypedDict):
    """A product ID and a list of images."""
    id: int
    images: List[BBImageDict]


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
