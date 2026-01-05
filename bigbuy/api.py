# -*- coding: utf-8 -*-

"""
Official documentation for Bigbuy API endpoints can be found at: https://api.bigbuy.eu/rest/doc/
"""
import base64
import mimetypes
from http.cookiejar import DefaultCookiePolicy
from typing import Optional, Union, Iterable, cast, Any

import requests
from api_session import APISession, JSONDict
from urllib3 import Retry

from . import __version__
from .exceptions import raise_for_response, BBError
from .rate_limit import RateLimit

__all__ = ['BigBuy']

from .types import BBProductImagesDict, BBTaxonomyDict, BBProductTaxonomyDict, BBLowestShippingCostDict, \
    BBAttributeDict, BBAttributeGroupDict, BBLanguageDict, BBManufacturerDict, BBProductDict, \
    BBProductCategoryDict, BBProductInformationDict, BBTrackingCarrierDict, BBOrderStatusDict, BBProductComplianceDict, \
    BBProductPriceDict, BBProductStockByHandlingDaysDict, BBProductTagDict, BBProductVariationDict, BBTagDict, \
    BBCarrierDict, BBVariationDict, BBCheckOrderDict

Id = Union[int, str]


class BigBuy(APISession):
    def __init__(self, app_key: Optional[str] = None,
                 *,
                 sandbox: bool = False,
                 retry_on_rate_limit: bool = False,
                 max_retry_on_rate_limit: int = 2,
                 **kwargs: Any):
        """Instantiates an instance of BigBuy.

        :param app_key: Your applications key
        :param sandbox: if `True`, use the client in sandbox mode.
        :param retry_on_rate_limit:
        :param max_retry_on_rate_limit:
        """
        if sandbox:
            base_url = 'https://api.sandbox.bigbuy.eu/rest'
        else:
            base_url = 'https://api.bigbuy.eu/rest'

        kwargs.setdefault("none_on_404", False)
        # BigBuy likes returning '200 OK' responses with empty bodies instead of 404s.
        kwargs.setdefault("none_on_empty", True)

        kwargs.setdefault("max_retries", Retry(
            allowed_methods=self.READ_METHODS,
            raise_on_status=False,
            status_forcelist={500, 502, 503, 524},
        ))

        super().__init__(base_url, user_agent=f'pyBigBuy v{__version__}', **kwargs)

        self.app_key = app_key
        self.retry_on_rate_limit = retry_on_rate_limit
        self.max_retry_on_rate_limit = max_retry_on_rate_limit
        self.headers.setdefault('Authorization', f'Bearer {app_key}')
        # Reject all cookies by default. They are not necessary for the API usage (and not documented).
        self.cookies.set_policy(DefaultCookiePolicy(allowed_domains=[]))

    def __repr__(self) -> str:
        attrs = f" key={self.app_key[:10]}…" if self.app_key else ""
        return f'<Bigbuy{attrs}>'

    def raise_for_response(self, response: requests.Response) -> None:
        return raise_for_response(response)

    def request_api(self, method: str, path: str, *args: Any,
                    throw: Optional[bool] = None,
                    retry_on_rate_limit: Optional[bool] = None,
                    max_retry_on_rate_limit: Optional[int] = None,
                    **kwargs: Any) -> requests.Response:
        if retry_on_rate_limit is None:
            retry_on_rate_limit = self.retry_on_rate_limit

        if max_retry_on_rate_limit is None:
            max_retry_on_rate_limit = self.max_retry_on_rate_limit

        r = super().request_api(method, f'/{path}.json', *args,
                                # We handle 'throw' by ourselves
                                throw=False,
                                **kwargs)

        if retry_on_rate_limit and max_retry_on_rate_limit > 0:
            if rate_limit := RateLimit.from_response(r):
                rate_limit.wait_until_expiration()
                # Retry after waiting for the rate-limit to expire
                return self.request_api(method, path, *args,
                                        throw=throw,
                                        retry_on_rate_limit=retry_on_rate_limit,
                                        max_retry_on_rate_limit=max_retry_on_rate_limit - 1,
                                        **kwargs)

        # throw=None == default behavior (True)
        if throw is True or throw is None:
            self.raise_for_response(r)

        return r

    # catalog
    def get_attribute(self, attribute_id: Id, **params: Any) -> BBAttributeDict:
        """Get a single attribute."""
        attribute: BBAttributeDict = self.get_json_api(f'catalog/attribute/{attribute_id}', params=params)
        return attribute

    def get_attribute_all_languages(self, attribute_id: Id, **params: Any) -> list[BBAttributeDict]:
        """Get a single attribute in all languages."""
        attributes: list[BBAttributeDict] = self.get_json_api(f'catalog/attributealllanguages/{attribute_id}',
                                                              params=params)
        return attributes

    def get_attribute_group(self, attribute_group_id: Id, **params: Any) -> BBAttributeGroupDict:
        """Get a single attribute group."""
        attribute_group: BBAttributeGroupDict = self.get_json_api(f'catalog/attributegroup/{attribute_group_id}',
                                                                  params=params)
        return attribute_group

    def get_attribute_group_all_languages(self, attribute_group_id: Id, **params: Any) -> list[BBAttributeGroupDict]:
        """Get a single attribute group in all languages."""
        attribute_groups: list[BBAttributeGroupDict] = self.get_json_api(
            f'catalog/attributegroupalllanguages/{attribute_group_id}', params=params)
        return attribute_groups

    def get_attribute_groups(self, **params: Any) -> list[BBAttributeGroupDict]:
        """Lists all attribute groups."""
        attribute_groups: list[BBAttributeGroupDict] = self.get_json_api('catalog/attributegroups', params=params)
        return attribute_groups

    def get_attributes(self, **params: Any) -> list[BBAttributeDict]:
        """Lists all attributes."""
        attributes: list[BBAttributeDict] = self.get_json_api('catalog/attributes', params=params)
        return attributes

    def get_languages(self, **params: Any) -> list[BBLanguageDict]:
        """Returns all languages"""
        languages: list[BBLanguageDict] = self.get_json_api('catalog/languages', params=params)
        return languages

    def get_manufacturer(self, manufacturer_id: Id, **params: Any) -> BBManufacturerDict:
        """Get a single manufacturer."""
        manufacturer: BBManufacturerDict = self.get_json_api(f'catalog/manufacturer/{manufacturer_id}', params=params)
        return manufacturer

    def get_manufacturers(self, **params: Any) -> list[BBManufacturerDict]:
        """Lists all manufacturers."""
        manufacturers: list[BBManufacturerDict] = self.get_json_api('catalog/manufacturers', params=params)
        return manufacturers

    def get_product(self, product_id: Id, **params: Any) -> BBProductDict:  # TODO: typing
        """Get a single product."""
        product: BBProductDict = self.get_json_api(f'catalog/product/{product_id}', params=params)
        return product

    def get_product_categories(self, product_id: Id, **params: Any) -> list[BBProductCategoryDict]:
        """Get product categories."""
        product_categories: list[BBProductCategoryDict] = self.get_json_api(f'catalog/productcategories/{product_id}',
                                                                            params=params)
        return product_categories

    def get_product_images(self, product_id: Id, **params: Any) -> BBProductImagesDict:
        """Get a single product images dict."""
        product_images: BBProductImagesDict = self.get_json_api(f'catalog/productimages/{product_id}', params=params)
        return product_images

    def get_product_information(self, product_id: Id, **params: Any) -> BBProductInformationDict:
        """Get a single product information dict."""
        product_information: BBProductInformationDict = self.get_json_api(f'catalog/productinformation/{product_id}',
                                                                          params=params)
        return product_information

    def get_product_information_all_languages(self, product_id: Id, **params: Any) -> list[BBProductInformationDict]:
        """Get a single product's information dicts in all languages."""
        product_information_dicts: list[BBProductInformationDict] = self.get_json_api(
            f'catalog/productinformationalllanguages/{product_id}', params=params)
        return product_information_dicts

    def get_product_information_by_sku(self, sku: str, **params: Any) -> BBProductInformationDict:
        """Get a single product by sku."""
        return self.get_json_api(f'catalog/productinformationbysku/{sku}', params=params)

    def get_product_compliance(self, product_id: Id, **params: Any) -> BBProductComplianceDict:
        """Get a single product compliance."""
        return self.get_json_api(f"catalog/productcompliance/{product_id}", params=params)

    def get_products(self, **params: Any) -> list[BBProductDict]:
        """Returns all products."""
        return self.get_json_api('catalog/products', params=params)

    def get_new_products(self, **params: Any) -> list[BBProductDict]:
        """Returns new or republished products in the last 7 days."""
        return self.get_json_api('catalog/new-products', params=params)

    def get_products_categories(self, **params: Any) -> list[BBProductCategoryDict]:
        """Returns all products categories."""
        return self.get_json_api('catalog/productscategories', params=params)

    def get_products_images(self, **params: Any) -> list[BBProductImagesDict]:
        """
        Returns all products images.

            Example format::

                {
                    "id": 123,
                    "images": [
                        {
                            "id": 45678,
                            "isCover": true,
                            "name": "H123_BC",
                            "url": "https://cdnbigbuy.com/images/H123_BC.jpg"
                        }
                    ]
                }
        """
        return self.get_json_api('catalog/productsimages', params=params)

    def get_products_information(self, **params: Any) -> list[BBProductInformationDict]:
        """Returns all products' information."""
        products_information: list[BBProductInformationDict] = self.get_json_api('catalog/productsinformation',
                                                                                 params=params)
        return products_information

    def get_products_prices(self, **params: Any) -> list[BBProductPriceDict]:
        """Returns all product pricing info."""
        product_prices: list[BBProductPriceDict] = self.get_json_api('catalog/productprices', params=params)
        return product_prices

    def get_product_variations_prices(self, **params: Any) -> list[BBProductPriceDict]:
        """Returns all product variation pricing info."""
        product_prices: list[BBProductPriceDict] = self.get_json_api('catalog/productvariationprices', params=params)
        return product_prices

    def get_products_stock_by_handling_days(self, **params: Any) -> list[BBProductStockByHandlingDaysDict]:
        """Returns all products stock by handling days."""
        products_stock: list[BBProductStockByHandlingDaysDict] = self.get_json_api(
            'catalog/productsstockbyhandlingdays', params=params)
        return products_stock

    def get_products_tags(self, **params: Any) -> list[BBProductTagDict]:
        """Lists all product tags."""
        product_tags: list[BBProductTagDict] = self.get_json_api('catalog/productstags', params=params)
        return product_tags

    def get_product_stock_by_handling_days(self, product_id: Id, **params: Any) -> BBProductStockByHandlingDaysDict:
        """Get a single product stock by handling days."""
        product_stock: BBProductStockByHandlingDaysDict = self.get_json_api(
            f'catalog/productstockbyhandlingdays/{product_id}', params=params)
        return product_stock

    def get_products_variations(self, **params: Any) -> list[BBProductVariationDict]:
        """Returns all products variations."""
        products_variations: list[BBProductVariationDict] = self.get_json_api('catalog/productsvariations',
                                                                              params=params)
        return products_variations

    def get_products_variations_stock_by_handling_days(self, **params: Any) -> list[BBProductStockByHandlingDaysDict]:
        """Returns all products variations stock by handling days."""
        product_stocks: list[BBProductStockByHandlingDaysDict] = self.get_json_api(
            'catalog/productsvariationsstockbyhandlingdays', params=params)
        return product_stocks

    def get_product_tags(self, product_id: Id, **params: Any) -> list[BBTagDict]:
        """Get tags for a single product."""
        tags: list[BBTagDict] = self.get_json_api(f'catalog/producttags/{product_id}', params=params)
        return tags

    def get_product_variations(self, product_id: Id, **params: Any) -> list[JSONDict]:  # TODO: typing
        """Get a single product's variations."""
        return self.get_json_api(f'catalog/productvariations/{product_id}', params=params)

    def get_product_variations_stock_by_handling_days(self, product_id: Id, **params: Any) -> JSONDict:  # TODO: typing
        """Get a single product variation's stocks by handling days."""
        return self.get_json_api(f'catalog/productvariationsstockbyhandlingdays/{product_id}', params=params)

    def get_tag(self, tag_id: Id, **params: Any) -> BBTagDict:
        """Get a single tag."""
        tag: BBTagDict = self.get_json_api(f'catalog/tag/{tag_id}', params=params)
        return tag

    def get_tag_all_languages(self, tag_id: Id, **params: Any) -> list[BBTagDict]:
        """Get a single tag in all languages."""
        tags: list[BBTagDict] = self.get_json_api(f'catalog/tagalllanguages/{tag_id}', params=params)
        return tags

    def get_tags(self, **params: Any) -> list[BBTagDict]:
        """Lists all tags."""
        tags: list[BBTagDict] = self.get_json_api('catalog/tags', params=params)
        return tags

    def get_variation(self, variation_id: Id, **params: Any) -> BBVariationDict:
        """Get a single variation."""
        variation: BBVariationDict = self.get_json_api(f'catalog/variation/{variation_id}', params=params)
        return variation

    def get_variations(self, **params: Any) -> list[BBVariationDict]:
        """Lists all variations.
        Format: {"id":1169758,"attributes":[{"id":24161}]}
        """
        variations: list[BBVariationDict] = self.get_json_api('catalog/variations', params=params)
        return variations

    # shipping
    def get_carriers(self, **params: Any) -> list[BBCarrierDict]:
        """Get the list of available carriers."""
        return self.get_json_api('shipping/carriers', params=params)

    def get_shipping_order(self, order: JSONDict) -> JSONDict:  # TODO: typing
        """Get the list of available shipping options with the calculated weight and cost in Kg and € respectively,
        for the given order.

        Example order:
            {"delivery":{"isoCountry":"ES","postcode":"46005"},"products":[{"reference":"V1300179","quantity":1}]}
        """
        # Note BigBuy's documentation says this returns a list of dicts, but in reality it returns a single dict
        return self.post_json_api('shipping/orders', json={"order": order}, bypass_read_only=True)

    # order
    def check_order(self, order: JSONDict, **params: Any) -> BBCheckOrderDict:
        """Check/simulate an order and return the total amount to pay.

        Example order:

            {
              "internalReference": "123456",
              "language": "es",
              "paymentMethod": "moneybox",
              "carriers": [
                { "name": "correos" },
                { "name": "chrono" }
              ],
              "shippingAddress": {
                "firstName": "John",
                "lastName": "Doe",
                "country": "ES",
                "postcode": "46005",
                "town": "Valencia",
                "address": "C/ Altea",
                "phone": "664869570",
                "email": "john@email.com",
                "comment": ""
              },
              "products": [
                {
                  "reference": "F1505138",
                  "quantity": 4
                }
              ]
            }

        Example response:

            {
              "totalWithoutTaxesAndWithoutShippingCost": 4.52,
              "totalWithoutTaxes": 8.52,
              "total": 9.809999999999999
            }
        """
        return self.post_json_api('order/check', json={"order": order}, bypass_read_only=True, **params)

    def check_multi_shipping_order(self, order: JSONDict, **params: Any) -> dict[str, list[JSONDict]]:  # TODO: typing
        """
        Check/simulate an order and return the total to pay. This is the multi-shipping version, which is required for
        some references.

        See `check_order` for the input format. The response differs because it splits the order in multiple sub-orders,
        each one with its check result.
        Example response:
            {
              "orders": [
                {
                  "productReferences": [ "S4602570" ],
                  "totalWithoutTaxesAndWithoutShippingCost": 4.52,
                  "totalWithoutTaxes": 8.52,
                  "total": 9.809999999999999,
                  "warehouse": 1
                },
                {
                  "productReferences": [ "S7106391" ],
                  "totalWithoutTaxesAndWithoutShippingCost": 109.2,
                  "totalWithoutTaxes": 109.2,
                  "total": 132.13,
                  "warehouse": 3
                }
              ],
              "errors": []
            }
        """
        return self.post_json_api('order/check/multishipping', json={"order": order}, bypass_read_only=True,
                                  **params)

    def create_order(self, order: JSONDict, **params: Any) -> requests.Response:
        """
        Submit an order and return the raw response.

        Example order:
            order = {
              "internalReference": "123456",
              "language": "es",
              "paymentMethod": "moneybox",
              "carriers": [
                {
                  "name": "correos"
                },
                {
                  "name": "chrono"
                }
              ],
              "shippingAddress": {
                "firstName": "John",
                "lastName": "Doe",
                "country": "ES",
                "postcode": "46005",
                "town": "Valencia",
                "address": "C/ Altea",
                "phone": "664869570",
                "email": "john@email.com",
                "comment": ""
              },
              "products": [
                {
                  "reference": "F1505138",
                  "quantity": 4
                }
              ]
            }
        """
        # NOTE: we must return the raw response because we need the headers to parse 'Location'
        return self.post_api('order/create', json={"order": order}, **params)

    def create_multi_shipping_order(self, order: JSONDict, **params: Any) -> dict[str, list[JSONDict]]:  # TODO: typing
        """
        Submit an order. This is the multi-shipping version, which is required for some references.

        See `create_order` for the input format.

        Example response:
            {"orders":[{"productReferences":["S1"],"id":"123","warehouse":1,"url":"\\/rest\\/order\\/123"},
                       {"productReferences":["S2", "S3"],"id":"124","warehouse":3,"url":"\\/rest\\/order\\/124"}],
             "errors":[]}
        """
        return self.post_json_api('order/create/multishipping', json={"order": order}, **params)

    def create_order_id(self, order: dict[str, Any], **params: Any) -> str:
        """Like create_order(), but return the order id."""
        response = self.create_order(order, **params)
        # Format:
        # {
        #     'Content-Length': '0',
        #     'Content-Type': 'application/json',
        #     'Date': 'Thu, 09 Apr 2020 07:24:56 GMT',
        #     'Location': '/rest/order/119...',
        #     'Set-Cookie': 'secure_key=16...065; expires=Thu, 16-Apr-2020 07:24:56 GMT; Max-Age=604800; path=/',
        # }
        # the id of the bigbuy order is only known in the location url in the headers
        return _get_order_id_from_response_redirect(response)

    def create_multi_shipping_order_ids(self, order: dict[str, Any], **params: Any) -> list[str]:
        """
        Like `create_multi_shipping_order()`, but return the order ids.
        This checks if the `errors` array is not empty and raises a `BBError` if so.
        """
        creation_response = self.create_multi_shipping_order(order, **params)
        if creation_response["errors"]:
            raise BBError("Multi-shipping order errors: %s" % creation_response)

        return [order["id"] for order in creation_response["orders"]]

    def get_order_by_customer_reference(self, reference: str, **params: Any) -> JSONDict:  # TODO: typing
        """
        Get order information by customer reference. Note that this doesn’t support multi-shipping orders and returns
        only one of the orders matching the customer reference.
        """
        return self.get_json_api(f'order/reference/{reference}', **params)

    def get_order_by_id(self, order_id: Id, **params: Any) -> JSONDict:
        """Get order information."""
        return self.get_json_api(f'order/{order_id}', **params)

    def get_order_delivery_notes(self, order_id: Id, **params: Any) -> JSONDict:  # TODO: typing
        """Get delivery notes for an order."""
        return self.get_json_api(f'order/delivery-notes/{order_id}', **params)

    def upload_order_invoice(self, order_id: Id, file_b64_content: str, mime_type: str, concept: str, amount: float,
                             **params: Any) -> list[bool]:
        """
        Upload a base64-encoded invoice to an order in PENDING INVOICE status.
        """
        invoice_payload = {
            "id_order": str(order_id),
            "file": file_b64_content,
            "mime_type": mime_type,
            "concept": concept,
            "amount": amount
        }
        return self.post_json_api("order/upload_invoice", json={"invoice": invoice_payload}, **params)

    def upload_order_invoice_by_path(self, order_id: Id, file_path: str, concept: str, amount: float,
                                     *, mime_type: Optional[str] = None, **params: Any) -> Any:  # TODO: typing
        """
        Wrapper around `upload_order_invoice` that reads the file from disk instead.

        :param order_id:
        :param file_path:
        :param concept:
        :param amount:
        :param mime_type: mime type of the file. If not provided it is guessed from the file path and defaults on
          `application/pdf`.
        """
        if mime_type is None:
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type is None:
                mime_type = "application/pdf"

        with open(file_path, "rb") as f:
            content = f.read()

        base64_content = base64.b64encode(content).decode("utf-8")

        return self.upload_order_invoice(order_id=order_id, file_b64_content=base64_content, mime_type=mime_type,
                                         concept=concept, amount=amount, **params)

    def get_order_statuses(self, **params: Any) -> list[BBOrderStatusDict]:
        """Get order statuses, as a list of dicts with "id" and "name" keys."""
        return self.get_json_api("order/orderstatuses", **params)

    # tracking
    def get_tracking_carriers(self, **params: Any) -> list[BBTrackingCarrierDict]:
        """Get the list of available carriers."""
        return self.get_json_api('tracking/carriers', **params)

    def get_tracking_order(self, order_id: Id, **params: Any) -> list[JSONDict]:  # TODO: typing
        """Get the list of available trackings."""
        return self.get_json_api(f'tracking/order/{order_id}', **params)

    def get_tracking_orders(self, order_ids: Iterable[Id], match_ids: bool = True, **params: Any) \
            -> list[Optional[JSONDict]]:  # TODO: typing
        """
        Get the list of available trackings for the given orders.

        If ``match_ids`` is true (the default), the returned sequence is guaranteed to have the same length
        as ``order_ids``, filled with ``None`` when appropriate. Otherwise, it should be in the same order but may
        be shorter as some orders may not have available tracking.
        """
        payload = {
            "track": {
                "orders": [{"id": order_id} for order_id in order_ids],
            }
        }

        trackings = cast(list[Optional[dict[str, Any]]],
                         self.post_json_api('tracking/orders', json=payload, bypass_read_only=True, **params))

        if not match_ids:
            return trackings

        tracking_by_id: dict[str, dict[str, Any]] = {}
        for tracking in trackings:
            if tracking:
                tracking_by_id[str(tracking["id"])] = tracking

        return [tracking_by_id.get(str(order_id)) for order_id in order_ids]

    def get_lowest_shipping_cost_by_country(self, reference: str, country_code: str,
                                            **params: Any) -> BBLowestShippingCostDict:
        """
        Equivalent of ``get_lowest_shipping_costs_by_country`` for a single product. Returns the lowest shipping cost
        for a product reference when sent to the provided country.
        """
        return self.post_json_api("shipping/lowest-shipping-cost-by-country",
                                  json={"product_country": {"reference": reference, "countryIsoCode": country_code}},
                                  bypass_read_only=True,
                                  **params)

    def get_lowest_shipping_costs_by_country(self, country_code: str, **params: Any) -> list[BBLowestShippingCostDict]:
        """
        Returns the lowest shipping cost for a product reference when sent to the provided country.

        As of 2022/04/21 the information is available for the following countries:
           FR, DK, CY, HU, GB, LT, MT, ES, LV, SK, RO, US, FI, GR, CZ, HR, SE, IE, LU, NL, AU, BG, NO, IT, DE, SI, PL,
           BE, CH, EE, PT, AT.

        Example item: ``{'reference': 'S4500511', 'cost': '4', 'carrierId': '43', 'carrierName': 'Chrono'}``.

        Warning: some dictionaries have ``'cost': None``.
        """
        return self.get_json_api(f"shipping/lowest-shipping-costs-by-country/{country_code}", **params)

    def get_purse_amount(self, **params: Any) -> float:
        """
        Get the amount of money available in the purse.
        """
        return float(self.get_json_api("user/purse", params=params))

    def get_taxonomies(self, **params: Any) -> list[BBTaxonomyDict]:
        """
        List all taxonomies.

        Example::

            {'id': 2, 'name': 'Acampada', 'url': 'acampada-y-foobar',
               'parentTaxonomy': 123, 'dateAdd': '2021-10-20 12:00:00', 'dateUpd': '2023-10-20 12:00:00',
               'urlImages': 'https://cdnbigbuy.com/images/HC123_BC_P00.jpg', 'isoCode': 'es'}
        """
        return self.get_json_api("catalog/taxonomies", params=params)

    def get_taxonomy_all_languages(self, taxonomy_id: Id, **params: Any) -> list[BBTaxonomyDict]:
        """
        Get a single taxonomy in all languages.
        """
        return self.get_json_api(f"catalog/taxonomyalllanguages/{taxonomy_id}", params=params)

    def get_product_taxonomies(self, product_id: Id, **params: Any) -> list[BBProductTaxonomyDict]:
        """
        Generate links between products and taxonomies.

        Example::

            [{'id': 5906, 'taxonomy': 5906, 'product': 334497}, {'id': 5908, 'taxonomy': 5908, 'product': 334497}]
        """
        return self.get_json_api(f"catalog/producttaxonomies/{product_id}", params=params)

    def get_products_taxonomies(self, **params: Any) -> list[BBProductTaxonomyDict]:
        """
        Return all taxonomies of all products.
        The format is the same as ``get_product_taxonomies``
        """
        return self.get_json_api("catalog/productstaxonomies", **params)

    def get_user_auth_status(self, **params: Any) -> None:
        """Get the auth status of the user. Always return None."""
        return self.get_json_api("user/auth/status", **params)


def _get_order_id_from_response_redirect(response: requests.Response) -> str:
    return response.headers["Location"].replace("/rest/order/", "")
