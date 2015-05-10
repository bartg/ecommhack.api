# encoding: utf-8
from __future__ import absolute_import, unicode_literals

import logging
import requests


log = logging.getLogger(__name__)


class HttpApiClient(object):

    @property
    def default_headers(self):
        return {}

    def url_for(self, path):
        raise NotImplementedError

    def get(self, path, params=None, custom_headers=None):
        """
        :param path: The core api request path
        :param params: Optional URL params
        :param custom_headers: Optional custom HTTP headers (default header can be overwritten)
        :return: The HTTP response

        :type path: str | unicode
        :type params: dict
        :type custom_headers: dict

        :rtype: requests.models.Response

        :raises requests.exceptions.RequestException
        """
        if custom_headers is None:
            custom_headers = {}

        headers = self.default_headers
        headers.update(custom_headers)

        response = requests.get(self.url_for(path), params=params, headers=headers)
        if not response.ok:
            log.error(response.content)
            response.raise_for_status()

        return response

    def post(self, path, json=None, params=None, custom_headers=None):
        """
        :param path: The core api request path
        :param json: Payload
        :param params: Optional URL params
        :param custom_headers: Optional custom HTTP headers (default header can be overwritten)
        :return: The HTTP response

        :type path: str | unicode
        :type json: dict
        :type params: dict
        :type custom_headers: dict

        :rtype: requests.models.Response

        :raises requests.exceptions.RequestException
        """
        if params is None:
            params = {}

        if custom_headers is None:
            custom_headers = {}

        headers = self.default_headers
        headers.update(custom_headers)

        response = requests.post(self.url_for(path), json=json, params=params, headers=headers)

        if not response.ok:
            log.error(response.content)
            response.raise_for_status()

        return response

    def put(self, path, json=None, params=None, custom_headers=None):
        """
        :param path: The core api request path
        :param json: The payload sent in the request body
        :param params: Optional URL params
        :param custom_headers: Optional custom HTTP headers (default header can be overwritten)
        :return: The HTTP response

        :type path: str | unicode
        :type json: unicode
        :type params: dict
        :type custom_headers: dict

        :rtype: requests.models.Response

        :raises requests.exceptions.RequestException
        """
        headers = self._get_request_headers(custom_headers)

        response = requests.put(self.url_for(path), json=json, params=params, headers=headers)

        if not response.ok:
            log.error(response.content)
            response.raise_for_status()

        return response

    def delete(self, path, params=None, custom_headers=None):
        """
        :param path: The core api request path
        :param params: Optional URL params
        :param custom_headers: Optional custom HTTP headers (default header can be overwritten)
        :return: The HTTP response

        :type path: str | unicode
        :type params: dict
        :type custom_headers: dict

        :rtype: requests.models.Response

        :raises requests.exceptions.RequestException
        """
        headers = self._get_request_headers(custom_headers)

        response = requests.delete(self.url_for(path), params=params, headers=headers)

        if not response.ok:
            log.error(response.content)
            response.raise_for_status()

        return response

    def _get_request_headers(self, custom_headers=None):
        """
        :type custom_headers: dict | None
        :rtype: dict
        """
        if custom_headers is None:
            custom_headers = {}

        headers = self.default_headers
        headers.update(custom_headers)

        return headers
