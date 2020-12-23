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

    try:
        errors = content.get("errors")
        if errors:
            return errors[0].get("message", error_message)
    except (KeyError, IndexError, TypeError):
        pass

    return error_message


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
        default_headers = {'User-Agent': f'pyBigBuy v{__version__}'}
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

    def __repr__(self):
        return '<Bigbuy: %s>' % self.app_key

    def request(self, endpoint, method='get', params=None):
        """Return dict of response received from BigBuy's API

        :param endpoint: (required) Full url or API endpoint
        :type endpoint: string
        :param method: (optional) Method of accessing data, either
                       GET, POST or DELETE. (default GET)
        :type method: string
        :param params: (optional) Dict of parameters (if any) accepted
                       by the BigBuy API endpoint you are trying to
                       access (default None)
        :type params: dict or None
        :rtype: dict
        """

        if endpoint.startswith('http://'):
            raise BBError('api.bigbuy.com is restricted to SSL/TLS traffic.')
        if endpoint.startswith('https://'):
            url = endpoint
        else:
            url = '%s/%s.json' % (self.api_url, endpoint)

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
            raise BBResponseError(str(e), e.response)

        raise_for_response(response)

        # TODO(BF): challenge this part -- why does the return type differ based on the response code?
        #  As a caller I don't know what to expect when I call this function.
        if response.status_code == 204:
            content = response.content
        elif response.status_code == 201:
            content = response
        elif response.content != '':
            try:
                content = response.json()
            except ValueError:
                raise BBError('Response is not valid JSON. Unable to decode.')
        else:
            content = ''

        return content

    def get(self, endpoint, params=None):
        """Shortcut for GET requests via :class:`request`"""
        return self.request(endpoint, params=params)

    def post(self, endpoint, params=None):
        """Shortcut for POST requests via :class:`request`"""
        return self.request(endpoint, 'post', params=params)

    def delete(self, endpoint, params=None):
        """Shortcut for delete requests via :class:`request`"""
        return self.request(endpoint, 'delete', params=params)
