# -*- coding: utf-8 -*-

"""
bigbuy.api
~~~~~~~~~~~

This module contains functionality for access to core Twitter API calls,
Twitter Authentication, and miscellaneous methods that are useful when
dealing with the Twitter API
"""
import re
import ujson
import requests
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth1, OAuth2

from . import __version__
from .advisory import BigbuyDeprecationWarning
from .compat import json, urlencode, parse_qsl, quote_plus, str, is_py2
from .compat import urlsplit
from .endpoints import EndpointsMixin
from .exceptions import BBError
from .helpers import _transparent_params


class BigBuy(EndpointsMixin, object):
    def __init__(self, app_key=None, mode="sandbox", client_args=None):
        """Instantiates an instance of BigBuy. Takes optional parameters for
        authentication and such (see below).

        :param app_key: (optional) Your applications key
        :param app_secret: (optional) Your applications secret key
        :param oauth_token: (optional) When using **OAuth 1**, combined with
        oauth_token_secret to make authenticated calls
        :param oauth_token_secret: (optional) When using **OAuth 1** combined
        with oauth_token to make authenticated calls
        :param access_token: (optional) When using **OAuth 2**, provide a
        valid access token if you have one
        :param token_type: (optional) When using **OAuth 2**, provide your
        token type. Default: bearer
        :param oauth_version: (optional) Choose which OAuth version to use.
        Default: 1
        :param api_version: (optional) Choose which Twitter API version to
        use. Default: 1.1

        :param client_args: (optional) Accepts some requests Session parameters
        and some requests Request parameters.
              See http://docs.python-requests.org/en/latest/api/#sessionapi
              and requests section below it for details.
              [ex. headers, proxies, verify(SSL verification)]
        :param auth_endpoint: (optional) Lets you select which authentication
        endpoint will use your application.
              This will allow the application to have DM access
              if the endpoint is 'authorize'.
                Default: authenticate.
        """

        self.app_key = app_key
        if mode == "sandbox":
            self.api_url = 'https://api.sandbox.bigbuy.eu/rest'
        elif mode == "production":
            self.api_url = 'https://api.bigbuy.eu/rest'
        self.client_args = client_args or {}
        default_headers = {'User-Agent': 'pyBigBuy v' + __version__}
        if 'headers' not in self.client_args:
            # If they didn't set any headers, set our defaults for them
            self.client_args['headers'] = default_headers
        elif 'User-Agent' not in self.client_args['headers']:
            # If they set headers, but didn't include User-Agent.. set
            # it for them
            self.client_args['headers'].update(default_headers)
        if 'Authorization' not in self.client_args['headers']:
            self.client_args['headers']['Authorization'] = 'Bearer %s' % app_key

        # Generate OAuth authentication object for the request
        # If no keys/tokens are passed to __init__, auth=None allows for
        # unauthenticated requests, although I think all v1.1 requests
        # need auth
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
        return '<Bigbuy: %s>' % (self.app_key)

    def _request(self, url, method='GET', params=None, api_call=None):
        """Internal request method"""
        method = method.lower()
        params = params or {}

        func = getattr(self.client, method)
        requests_args = {}
        if method == 'get' or method == 'delete':
            requests_args['params'] = params
        else:
            requests_args.update({
                "data": ujson.dumps(params),
            })
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
        # greater than 304 (not modified) is an error
        if response.status_code > 304:
            error_message = self._get_error_message(response)
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

    def _get_error_message(self, response):
        """Parse and return the first error message"""

        error_message = 'An error occurred processing your request.'
        try:
            content = response.json()
            # {"errors":[{"code":34,"message":"Sorry,
            # that page does not exist"}]}
            error_message = content['errors'][0]['message']
        except TypeError:
            error_message = content['errors']
        except ValueError:
            # bad json data
            pass
        except (KeyError, IndexError):
            # missing data so fallback to default message
            pass

        return error_message

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
