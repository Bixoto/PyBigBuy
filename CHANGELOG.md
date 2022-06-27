# PyBigBuy Changelog

## Unreleased

* Add `wait_rate_limit` to wait for a `BBRateLimitError` delay

## 3.13.9 (2022/06/16)

* `raise_for_response`: raise a `BBProductError` with a more useful error message when BigBuy returns the error `Products error.`
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

## 3.13.6 (2022/05/24)

* Fix the parsing of soft errors introduced in the latest release

## 3.13.5 (2022/05/24)

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

* Fix the 3.8.4 release

## 3.8.5 (2021/10/06)

* Fix the previous release’s addition

## 3.8.4 (2021/10/06)

* Raise `BBServerError` on another format of internal server error responses

## 3.8.3 (2021/10/06)

* Raise `BBServerError` on internal server errors 

## 3.8.2 (2021/09/23)

* Add `BBServerError` as a subclass of `BBResponseError` for `503`/`504` errors

Note: 3.8.1 is the same as this version.

## 3.8.0 (2021/06/04)

* Make BigBuy an HTTP client
* Add a class for each error code
* Clarify error messages
* Add type hints

## 3.7.0 (2019/11/05)

First version.

It was 3.7.0 in `setup.py` but `0.0.1` in `__init__.py`.
