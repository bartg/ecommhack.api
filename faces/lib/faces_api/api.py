# encoding: utf-8
from __future__ import absolute_import, unicode_literals
from decimal import Decimal

import logging
from django.conf import settings
from faces.lib import HttpApiClient


log = logging.getLogger(__name__)


class FaceAPIClient(HttpApiClient):
    URL_PATTERN = "https://api.projectoxford.ai/face/v0{path}"

    def __init__(self, subscription_key):
        self.subscription_key = subscription_key

    @property
    def default_headers(self):
        """
        :return: The default headers that are sent with every request unless explicitly overwritten
        :rtype: dict
        """
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Ocp-Apim-Subscription-Key": self.subscription_key
        }

    @classmethod
    def url_for(cls, path):
        """
        Returns the full core api url for the given relative path

        :param path: Relative core api path
        :return: Full core api url

        :type path: str | unicode
        :rtype: unicode
        """
        if not path.startswith("/"):
            path = "/{path}".format(path=path)

        return cls.URL_PATTERN.format(path=path)


class FaceAPI(object):

    def __init__(self, subscription_key=settings.FACE_API_SUBSCRIPTION_KEY):
        self.client = FaceAPIClient(subscription_key=subscription_key)

    @property
    def faces(self):
        return Faces(client=self.client)

    @property
    def persons(self):
        return Persons(client=self.client)

    @property
    def person_groups(self):
        return PersonGroups(client=self.client)


class FaceAPIResource(object):

    def __init__(self, client):
        """
        :type client: FaceAPIClient
        """
        self.client = client


class Faces(FaceAPIResource):

    def detect(self, image_url):
        """
        Tries to detect *one* face!

        :type image_url: unicode
        :rtype: dict | None
        """
        params = dict(analyzesFaceLandmarks=True, analyzesAge=True, analyzesGender=True, analyzesHeadPose=True)
        response = self.client.post("/detections", params=params, json={
            "url": image_url
        })

        faces = response.json()
        if not faces:
            return None

        return faces[0]

    def identify(self, face_id, person_group_id):
        """
        Tries to identify the given face in the given person group

        :type face_id: unicode
        :type person_group_id: unicode

        :returns (personId, faceId, confidence)
        :rtype: (unicode, unicode, Decimal)
        """
        response = self.client.post("/identifications", json={
            "faceIds": [face_id],
            "personGroupId": person_group_id,
            "maxNumOfCandidatesReturned": 1
        })

        results = response.json()

        if not results:
            return None

        result = results[0]

        candidates = result["candidates"]
        log.info("Got {} candidates for face_id {}: {}"
                 .format(len(candidates), face_id, candidates))

        if not candidates:
            return None

        candidate = candidates[0]
        return candidate["personId"], Decimal(candidate["confidence"])


class Persons(FaceAPIResource):

    def create(self, group_id, name):
        """
        :type group_id: unicode
        :type name: unicode

        :returns person_id
        :rtype: unicode
        """
        response = self.client.post("/persongroups/{group_id}/persons".format(group_id=group_id), json={
            "faceIds": [],
            "name": name
        })

        result = response.json()
        return result["personId"]

    def add_face(self, group_id, person_id, face_id):
        """
        :type group_id: unicode
        :type person_id: unicode
        :type face_id: unicode
        """
        self.client.put("/persongroups/{group_id}/persons/{person_id}/faces/{face_id}"
                        .format(group_id=group_id, person_id=person_id, face_id=face_id))
        return True


class PersonGroups(FaceAPIResource):

    def train(self, group_id):
        """
        :type group_id: unicode
        """
        self.client.post("/persongroups/{group_id}/training".format(group_id=group_id))
        return True
