# encoding: utf-8
from __future__ import absolute_import, unicode_literals
import base64

import logging
from django.conf import settings
from faces.lib import HttpApiClient


log = logging.getLogger(__name__)


class ZalandoAPIClient(HttpApiClient):
    URL_PATTERN = "https://api.zalando.com{path}"

    def __init__(self, client_name):
        """
        :type client_name: unicode
        """
        self.client_name = client_name

    @property
    def default_headers(self):
        """
        :return: The default headers that are sent with every request unless explicitly overwritten
        :rtype: dict
        """
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Accept-Language": "en-GB",
            "X-Client-Name": self.client_name
        }

    def url_for(self, path):
        """
        Returns the full zalando api url for the given relative path

        :param path: Relative sphere api path
        :return: Full sphere api url

        :type path: str | unicode
        :rtype: unicode
        """
        if not path.startswith("/"):
            path = "/{path}".format(path=path)

        return self.URL_PATTERN.format(path=path)


class ZalandoAPI(object):

    def __init__(self, client_name=settings.ZALANDO_API_CLIENT_NAME):
        self.client = ZalandoAPIClient(client_name=client_name)

    @property
    def articles(self):
        """
        :rtype: ArticlesResource
        """
        return ArticlesResource(client=self.client)


class ArticlesResource(object):

    def __init__(self, client):
        """
        :type client: ZalandoAPIClient
        """
        self.client = client

    def get(self, page_size=50, pages=1):
        """
        :type page_size: int
        :type pages: int

        :rtype: collections.Iterable[list]
        """
        for i in range(1, pages + 1):
            response = self.client.get("/articles?pageSize={}&page={}".format(page_size, i))
            data = response.json()
            yield data["content"]
