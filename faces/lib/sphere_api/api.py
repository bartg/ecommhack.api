# encoding: utf-8
from __future__ import absolute_import, unicode_literals
import base64

import logging
import requests
from faces.lib import HttpApiClient


log = logging.getLogger(__name__)


class SphereAPIException(Exception):
    pass


class SphereAPIAuthenticator(object):
    AUTH_URL = "https://auth.sphere.io/oauth/token"

    def __init__(self, client_id, client_secret, project_key):
        """
        :type client_id: unicode
        :type client_secret: unicode
        :type project_key: unicode
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.project_key = project_key

    def auth(self):
        """
        BÄÄÄM BÄ BÄÄÄÄÄMMMMMMM
        :returns Access token
        :rtype: dict
        """
        encoded = base64.b64encode("{}:{}".format(self.client_id, self.client_secret))
        headers = {"Authorization": "Basic {}".format(encoded),
                   "Content-Type": "application/x-www-form-urlencoded"}
        body = "grant_type=client_credentials&scope=manage_project:{}".format(self.project_key)

        response = requests.post(self.AUTH_URL, data=body, headers=headers)
        if response.status_code is 200:
            return response.json()
        else:
            raise SphereAPIException("Failed to get an access token.")


class SphereAPIClient(HttpApiClient):
    URL_PATTERN = "https://api.sphere.io/{project_key}{path}"

    def __init__(self, access_token, project_key):
        self.access_token = access_token
        self.project_key = project_key

    @property
    def default_headers(self):
        """
        :return: The default headers that are sent with every request unless explicitly overwritten
        :rtype: dict
        """
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer {}".format(self.access_token)
        }

    def url_for(self, path):
        """
        Returns the full sphere api url for the given relative path

        :param path: Relative sphere api path
        :return: Full sphere api url

        :type path: str | unicode
        :rtype: unicode
        """
        if not path.startswith("/"):
            path = "/{path}".format(path=path)

        return self.URL_PATTERN.format(project_key=self.project_key, path=path)


class SphereAPI(object):

    def __init__(self, access_token, project_key):
        self.client = SphereAPIClient(access_token, project_key)


class ProductsResource(object):

    def __init__(self, client):
        """
        :type client: SphereAPIClient
        """
        self.client = client
