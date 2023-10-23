# PyBigBuy Changelog

Note: the BigBuy API is not versioned and some endpoints are often added or removed without notice.
The removal of methods that call deleted endpoints is not considered a breaking change.

## Unreleased

* Add official support for Python 3.12.0
* Use `BBTimeoutError` for more timeout errors instead of `BBResponseError`

## 3.19.2 (2023/10/19)

* Add `get_user_auth_status`, `get_product_stock_by_handling_days`, `get_product_variations_stock_by_handling_days`
* Deprecate `get_products_stock`, `get_product_stock`, `get_products_variations_stock`
  and `get_product_variations_stock`, because the endpoint they’re calling are deprecated and will be removed
  on April 1st, 2024

## 3.19.1 (2023/09/29)

* Remove `get_products_stock_available` and `get_products_variations_stock_available`,
  because BigBuy removed the endpoints on September 28, 2023

## 3.19.0 (2023/09/11)

* Add official support for Python 3.12-rc2

### Breaking change

* Remove the `mode` argument of the class constructor. This has been deprecated for almost a year, since 3.16.0.
  Use `sandbox=True` to use the sandbox mode instead of `mode="sandbox"`. Note the class now defaults to production mode
  rather than the sandbox.

## 3.18.1 (2023/07/27)

* Add `get_order_delivery_notes` for the new `order/delivery-notes` route
* Add `BBTimeoutError` as a subclass of `BBServerError` and `TimeoutError`
* Support more weird HTML formatting for 500 errors

## 3.18.0 (2023/07/11)

* Add `get_order_statuses` for the new `order/orderstatuses` route
* Add `get_new_products` for the new `catalog/new-products` route
* Support another weird HTML formatting for 500 errors
* Allow to import `BBShippingError` and `BBWarehouseSplitError` directly from `bigbuy`

### Breaking changes

* Remove `BBRateLimitError.reset_time` (use `BBRateLimitError.rate_limit.reset_time`)
* Remove `wait_rate_limit(e)` (use `e.wait_rate_limit()`)
* Remove `BBWarehouseError` (use `BBWarehouseSplitError`)

## 3.17.0 (2022/11/08)

* Document `create_multi_shipping_order` response
* Rename `BBWarehouseError` as `BBWarehouseSplitError` but keep the alias `BBWarehouseError` for now

### Breaking changes

* Remove the ability to call `get_shipping_order`/`check_order`/`create_order` with `{"order": order}` instead of
  `order`. This behavior has been deprecated in 3.13.11.
* Rename `create_multi_shipping_order_id` as `create_multi_shipping_order_ids`
* `create_multi_shipping_order` now returns a dict instead of a `Response` object
* All cookies are now rejected by default. You can change this by using
  `.cookies.set_policy(http.cookiejar.DefaultCookiePolicy())`. Cookies are not necessary for the API usage so this
  should not break anything.

## 3.16.1 (2022/11/07)

* Add `check_multi_shipping_order`, `create_multi_shipping_order`, `create_multi_shipping_order_id`
* Add a `BBWarehouseError` for the new warehouse errors that BigBuy returns on some orders
* Add `BBShippingError` as a parent class for `BBWarehouseError` and `BBNoCarrierError`

## 3.16.0 (2022/10/12)

* Deprecated `mode` argument of `BigBuy` and add the optional `sandbox` boolean keyword argument. If `sandbox` is not
  set, the behavior is exactly the same as today. If it’s set, it overrides the mode. In the future, we’ll remove `mode`
  in favor of `sandbox=True` (sandbox mode) or `sandbox=False` (production mode; the default).
* `raise_for_response`: trim more garbage in HTML error responses
* Remove `get_products_stock_available_by_handling_days` and `get_products_variations_stock_available_by_handling_days`:
  BigBuy removed the endpoints

### Breaking changes

* Arguments `retry_on_rate_limit` and `max_retry_on_rate_limit` of `BigBuy` are now keyword-only.
  Before you could use `BigBuy(app_key, "sandbox", True)`; now you must use
  `BigBuy(app_key, "sandbox", retry_on_rate_limit=True)`

## 3.15.3 (2022/08/17)

This is the first public release.

* Add `get_products_stock_by_handling_days`, `get_products_stock_available_by_handling_days`,
  `get_products_variations_stock_by_handling_days`, `get_products_variations_stock_available_by_handling_days`
* Add `upload_order_invoice` and `upload_order_invoice_by_path`
* Fix `repr()` on `BigBuy` instances without app key

## 3.15.2 (2022/08/03)

* Add optional `max_retry_on_rate_limit` to `BigBuy` to configure the maximum number of retries in case of rate-limit
  error response. This has no effect if `retry_on_rate_limit` is not used.

## 3.15.0, 3.15.1 (2022/08/03)

* Add `RateLimit` and move all the rate-limit logic in it. Existing attributes and functions are conserved for
  backward-compatibility.
* Improve the "automatic retry on rate-limit errors" feature by making it work on all calls. Previously, it worked only
  on calls using `throw=True` and not on `get_json_api(none_on_404=True)` ones
* `wait_rate_limit`: remove the 0.01s of additional delay introduced in the previous release. Don’t return `False` if
  the delta is negative.
* Remove `get_order_addresses` and `get_order_carriers`: the endpoints they were calling have been removed by BigBuy
  three months ago

## 3.14.0 (2022/07/28)

* Add optional `retry_on_rate_limit` boolean flag to `BigBuy` to enable automatic retry on rate-limit errors
* Pass keyword arguments given to `__init__` to the parent
* `wait_rate_limit`: add 0.01s of additional delay (configurable)

## 3.13.11 (2022/07/28)

* Deprecate functions called as `function({"order": order})` in favor of `function(order)`
* `raise_for_response`: trim some garbage in HTML error responses

## 3.13.10 (2022/06/27)

* Add `wait_rate_limit` to wait for a `BBRateLimitError` delay

## 3.13.9 (2022/06/16)

* `raise_for_response`: raise a `BBProductError` with a more useful error message when BigBuy returns the error
  `Products error.`
* Additional typing hints

## 3.13.8 (2022/05/25)

* `get_*`: return `None` when we get an empty response from BigBuy instead of crashing when trying to decode it as JSON.
  The API has been returning a lot of `200 OK` with empty bodies lately instead of proper 404s.
* Add methods to get taxonomies
* All methods now accept additional keyword parameters to pass to the underlying `requests` call
* Additional typing hints
* Remove dead doc links in docstrings

## 3.13.7 (2022/05/25)

* `raise_for_response`: don’t crash on empty response bodies

## 3.13.5, 3.13.6 (2022/05/24)

* `raise_for_response` now support soft errors where a full error response is embedded in a `200 OK` response body

## 3.13.4 (2022/05/24)

* `raise_for_response` now supports soft errors; for example BigBuy may return a `200 OK` response whose body is
  `{"code": 409, "message": "Something went wrong"}`. This is now treated as an error instead of a success.

## 3.13.3 (2022/04/29)

* Add `get_modules` and `get_module_platforms`
* Raise `BBValidationError` instead of a generic `BBResponseError` on even more validation errors.

## 3.13.2 (2022/04/22)

* Add `create_order_id` and `get_purse_amount`

## 3.13.1 (2022/04/21)

* Add `get_lowest_shipping_cost_by_country` and `get_lowest_shipping_costs_by_country`

## 3.13.0 (2022/04/21)

* `.request_api` now always return a `requests.Response` object and don’t accept a `raw_response` parameter anymore.
  This is a breaking change only if you rely on a direct call to this method.
* Raise `BBValidationError` instead of a generic `BBResponseError` on more validation errors. This is not breaking
  since the former inherit from the latter.
* `get_tracking_orders` now accepts both `int` and `str` order ids.

## 3.12.1 (2022/04/01)

* Fix typo in `setup.py` by generating it with Poetry (it used `api-sessions` instead of `api-session`)

## 3.12.0 (2022/04/01)

* All calls now raise by default

## 3.11.0 (2022/03/31)

This release revert the main change of 3.10.0.

* All `POST` calls now raise by default

## 3.10.0 (2022/03/31)

* The client now raises if a response has an error body, even if its HTTP status code doesn’t indicate an error.

## 3.9.0 (2022/03/14)

* Use `api-session` as a base class. This changes `BigBuy#request_api`’s signature: `request_api(endpoint, method)`
  becomes `request_api(method, endpoint)`.
* Add `BBValidationError`
* `requests.RequestError` exceptions are no longer wrapped in `BBResponseError`

## 3.8.6 (2021/10/07)

* Fix the previous release

## 3.8.4, 3.8.5 (2021/10/06)

* Raise `BBServerError` on another format of internal server error responses

## 3.8.3 (2021/10/06)

* Raise `BBServerError` on internal server errors

## 3.8.1, 3.8.2 (2021/09/23)

* Add `BBServerError` as a subclass of `BBResponseError` for `503`/`504` errors

## 3.8.0 (2021/06/04)

* Fix `bigbuy.__version__`
* Make BigBuy an HTTP client
* Add a class for each error code
* Clarify error messages
* Add type hints

## 3.7.0 (2019/11/05)

First version.
