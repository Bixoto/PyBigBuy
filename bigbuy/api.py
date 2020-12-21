# -*- coding: utf-8 -*-

"""
bigbuy.api
~~~~~~~~~~~

This module contains functionality for access to core Twitter API calls,
Twitter Authentication, and miscellaneous methods that are useful when
dealing with the Twitter API
"""
import requests

from . import __version__
from .compat import str
from .endpoints import EndpointsMixin
from .exceptions import BBError

__all__ = ['BigBuy']


def _get_error_message(response):
    """Parse and return the first error message"""

    error_message = f'An error occurred processing your request: {response.text}'
    try:
        # {"errors":[{"code":34,"message":"Sorry, that page does not exist"}]}
        content = response.json()
    except ValueError:
        # bad JSON data
        return error_message

    errors = content.get("errors")
    if not errors:
        return error_message

    return errors[0].get("message", error_message)


class BigBuy(EndpointsMixin, object):
    def __init__(self, app_key=None, mode="sandbox", client_args=None):
        """Instantiates an instance of BigBuy. Takes optional parameters for
        authentication and such (see below).

        :param app_key: (optional) Your applications key
        :param mode: "sandbox" or "production"
        :param client_args: (optional) Accepts some requests Session parameters
        and some requests Request parameters.
              See http://docs.python-requests.org/en/latest/api/#sessionapi
              and requests section below it for details.
              [ex. headers, proxies, verify(SSL verification)]
        """

        self.app_key = app_key
        if mode == "sandbox":
            self.api_url = 'https://api.sandbox.bigbuy.eu/rest'
        elif mode == "production":
            self.api_url = 'https://api.bigbuy.eu/rest'
        self.client_args = client_args or {}
        default_headers = {'User-Agent': 'pyBigBuy v' + __version__}
        self.client_args.setdefault('headers', default_headers)
        if 'User-Agent' not in self.client_args['headers']:
            # If they set headers, but didn't include User-Agent set it for them
            self.client_args['headers'].update(default_headers)
        if 'Authorization' not in self.client_args['headers']:
            self.client_args['headers']['Authorization'] = 'Bearer %s' % app_key

        self.client = requests.Session()

        # Make a copy of the client args and iterate over them
        # Pop out all the acceptable args at this point because they will
        # Never be used again.
        client_args_copy = self.client_args.copy()
        for k, v in client_args_copy.items():
            if k in ('cert', 'hooks', 'max_redirects', 'proxies'):
                setattr(self.client, k, v)
                self.client_args.pop(k)  # Pop, pop!

        # Headers are always present, so we unconditionally pop them and merge
        # them into the session headers.
        self.client.headers.update(self.client_args.pop('headers'))
        self._last_call = None

    def __repr__(self):
        return '<Bigbuy: %s>' % self.app_key

    def _request(self, url, method='GET', params=None, api_call=None):
        """Internal request method"""
        method = method.lower()
        params = params or {}

        func = getattr(self.client, method)
        requests_args = {}
        if method == 'get' or method == 'delete':
            requests_args['params'] = params
        else:
            requests_args["json"] = params
        try:
            response = func(url, **requests_args)
        except requests.RequestException as e:
            raise BBError(str(e))

        # create stash for last function intel
        self._last_call = {
            'api_call': api_call,
            'api_error': None,
            'cookies': response.cookies,
            'headers': response.headers,
            'status_code': response.status_code,
            'url': response.url,
            'content': response.text,
        }
        if not response.ok:
            error_message = _get_error_message(response)
            self._last_call['api_error'] = error_message
            raise BBError(
                error_message,
                error_code=response.status_code,
                retry_after=response.headers.get('X-Rate-Limit-Reset'),
                post_mortem=self._last_call
            )
        content = ''
        try:
            if response.status_code == 204:
                content = response.content
            elif response.status_code == 201:
                content = response
            else:
                content = response.json()
        except ValueError:
            if response.content != '':
                raise BBError('Response was not valid JSON. \
                                   Unable to decode.')

        return content

    def request(self, endpoint, method='GET', params=None, version='1.1'):
        """Return dict of response received from Twitter's API

        :param endpoint: (required) Full url or Twitter API endpoint
                         (e.g. search/tweets)
        :type endpoint: string
        :param method: (optional) Method of accessing data, either
                       GET, POST or DELETE. (default GET)
        :type method: string
        :param params: (optional) Dict of parameters (if any) accepted
                       the by Twitter API endpoint you are trying to
                       access (default None)
        :type params: dict or None
        :param version: (optional) Twitter API version to access
                        (default 1.1)
        :type version: string
        :rtype: dict
        """

        if endpoint.startswith('http://'):
            raise BBError('api.bigbuy.com is restricted to SSL/TLS traffic.')
        if endpoint.startswith('https://'):
            url = endpoint
        else:
            url = '%s/%s.json' % (self.api_url, endpoint)

        content = self._request(url, method=method, params=params,
                                api_call=url)

        return content

    def get(self, endpoint, params=None, version='1.1'):
        """Shortcut for GET requests via :class:`request`"""
        return self.request(endpoint, params=params, version=version)

    def post(self, endpoint, params=None, version='1.1'):
        """Shortcut for POST requests via :class:`request`"""
        return self.request(endpoint, 'POST', params=params, version=version)

    def delete(self, endpoint, params=None, version='1.1'):
        """Shortcut for delete requests via :class:`request`"""
        return self.request(endpoint, 'DELETE', params=params, version=version)
