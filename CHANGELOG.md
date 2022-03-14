# PyBigBuy Changelog

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
