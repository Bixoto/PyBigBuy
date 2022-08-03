from datetime import datetime
from typing import Callable

import pytest
import responses
from responses.registries import OrderedRegistry

from bigbuy import BigBuy, BBRateLimitError
from bigbuy.rate_limit import RATE_LIMIT_RESPONSE_TEXT


def test_init_defaults(app_key):
    bb = BigBuy(app_key)
    assert bb.none_on_404 is False
    assert bb.none_on_empty is True
    assert bb.retry_on_rate_limit is False
    assert bb.base_url == "https://api.sandbox.bigbuy.eu/rest"


def test_init_production(app_key):
    bb = BigBuy(app_key, mode="production")
    assert bb.base_url == "https://api.bigbuy.eu/rest"


def test_repr(app_key):
    bb = BigBuy(app_key)
    assert repr(bb) == f"<Bigbuy key={app_key[:10]}…>"


@responses.activate
def test_get_json_api(app_key):
    bb = BigBuy(app_key)
    payload = {"test": "ok"}

    responses.get(
        bb.base_url + "/toto.json",
        json=payload,
    )

    assert bb.get_json_api("toto") == payload


@responses.activate()
def test_get_json_api_rate_limit_no_retry(app_key):
    bb = BigBuy(app_key)

    responses.get(
        bb.base_url + "/toto.json",
        body=RATE_LIMIT_RESPONSE_TEXT,
        status=429,
        headers={
            "X-Ratelimit-Reset": str(int(datetime.utcnow().timestamp()))
        }
    )

    with pytest.raises(BBRateLimitError):
        bb.get_json_api("toto")


@responses.activate(registry=OrderedRegistry)
def test_get_json_api_auto_retry_once(app_key):
    bb = BigBuy(app_key, retry_on_rate_limit=True)
    payload = {"test": "ok"}

    responses.get(
        bb.base_url + "/toto.json",
        body=RATE_LIMIT_RESPONSE_TEXT,
        status=429,
        headers={
            "X-Ratelimit-Reset": str(int(datetime.utcnow().timestamp()))
        }
    )

    responses.get(
        bb.base_url + "/toto.json",
        json=payload,
    )

    assert bb.get_json_api("toto") == payload


@responses.activate(assert_all_requests_are_fired=True)
def test_get_api_endpoints(app_key):
    bb = BigBuy(app_key=app_key)
    payload = {"test": "ok"}

    for test_case in (
            ("catalog/attribute/123", bb.get_attribute, ("123",)),
            ("catalog/attributealllanguages/124", bb.get_attribute_all_languages, ("124",)),
            ("catalog/attributegroup/125", bb.get_attribute_group, ("125",)),
            ("catalog/attributegroupalllanguages/126", bb.get_attribute_group_all_languages, ("126",)),
            ("catalog/attributegroups", bb.get_attribute_groups),
            ("catalog/attributes", bb.get_attributes),
            ("catalog/categories", bb.get_categories),
            ("catalog/category/127", bb.get_category, ("127",)),
            ("catalog/categoryalllanguages/128", bb.get_category_all_languages, ("128",),),
            ("catalog/languages", bb.get_languages),
            ("catalog/manufacturer/129", bb.get_manufacturer, ("129",)),
            ("catalog/manufacturers", bb.get_manufacturers),
            ("catalog/product/130", bb.get_product, ("130",)),
            ("catalog/productcategories/131", bb.get_product_categories, ("131",)),
            ("catalog/productimages/132", bb.get_product_images, ("132",)),
            ("catalog/productinformation/133", bb.get_product_information, ("133",)),
            ("catalog/productinformationalllanguages/134", bb.get_product_information_all_languages, ("134",)),
            ("catalog/productinformationbysku/SK135", bb.get_product_information_by_sku, ("SK135",)),
            ("catalog/products", bb.get_products),
            ("catalog/productscategories", bb.get_products_categories),
            ("catalog/productsimages", bb.get_products_images),
            ("catalog/productsinformation", bb.get_products_information),
            ("catalog/productsstock", bb.get_products_stock),
            ("catalog/productsstockavailable", bb.get_products_stock_available),
            ("catalog/productstags", bb.get_products_tags),
            ("catalog/productstaxonomies", bb.get_products_taxonomies),
            ("catalog/productstock/136", bb.get_product_stock, ("136",)),
            ("catalog/productsvariations", bb.get_products_variations),
            ("catalog/productsvariationsstock", bb.get_products_variations_stock),
            ("catalog/productsvariationsstockavailable", bb.get_products_variations_stock_available),
            ("catalog/producttags/137", bb.get_product_tags, ("137",)),
            ("catalog/producttaxonomies/123", bb.get_product_taxonomies, ("123",)),
            ("catalog/productvariations/138", bb.get_product_variations, ("138",)),
            ("catalog/productvariationsstock/139", bb.get_product_variations_stock, ("139",)),
            ("catalog/tag/140", bb.get_tag, ("140",)),
            ("catalog/tagalllanguages/141", bb.get_tag_all_languages, ("141",)),
            ("catalog/tags", bb.get_tags),
            ("catalog/taxonomies", bb.get_taxonomies),
            ("catalog/taxonomyalllanguages/42", bb.get_taxonomy_all_languages, ("42",)),
            ("catalog/variation/142", bb.get_variation, ("142",)),
            ("catalog/variations", bb.get_variations),
            ("module/", bb.get_modules),
            ("module/platforms", bb.get_module_platforms),
            ("order/123", bb.get_order_by_id, ("123",)),
            ("order/reference/REF123", bb.get_order_by_customer_reference, ("REF123",)),
            ("shipping/carriers", bb.get_carriers),
            ("shipping/lowest-shipping-costs-by-country/XX", bb.get_lowest_shipping_costs_by_country, ("XX",)),
            ("tracking/carriers", bb.get_tracking_carriers),
            ("tracking/order/123", bb.get_tracking_order, ("123",)),
    ):
        endpoint: str = test_case[0]
        method: Callable = test_case[1]
        args: tuple = test_case[2] if len(test_case) == 3 else ()

        responses.get(f"{bb.base_url}/{endpoint}.json", json=payload)
        assert method(*args) == payload


@responses.activate()
def test_get_purse_amount(app_key):
    bb = BigBuy(app_key)
    responses.get(bb.base_url + "/user/purse.json", body="3.14")
    assert bb.get_purse_amount() == 3.14