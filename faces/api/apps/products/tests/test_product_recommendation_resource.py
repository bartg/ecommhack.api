# encoding: utf-8
from __future__ import absolute_import, unicode_literals
import logging

from rest_framework.status import HTTP_200_OK
from faces.api.apps.products.models import ProductModel

from faces.api.apps.products.scripts import fetch_products
from faces.api.apps.users.models import Gender
from faces.lib.tests.testcases import AuthenticatedAPITestCase, APITestCase


log = logging.getLogger(__name__)


class TestProductRecommendationResource(AuthenticatedAPITestCase):

    @APITestCase.vcr.use_cassette("api/product_recommendation.yaml")
    def test_smoke(self):
        # add some data for the recommender :-)
        self.user.gender = Gender.MALE
        self.user.age = 17
        self.user.save()

        fetch_products.run(page_size=50, pages=1)

        response = self.client.post("/products/recommendation/?user_id={}".format(self.user.id))
        self.assertEqual(response.status_code, HTTP_200_OK)
        prev_product_id = response.data["id"]

        product = ProductModel.objects.get(id=prev_product_id)
        # recommender should recommend
        self.assertTrue(product.gender_male)
        self.assertTrue(product.age_group_teen)

        response = self.client.post("/products/recommendation/?user_id={}".format(self.user.id))
        self.assertEqual(response.status_code, HTTP_200_OK)

        product_id = response.data["id"]

        product = ProductModel.objects.get(id=product_id)

        # recommender should recommend
        self.assertTrue(product.gender_male)
        self.assertTrue(product.age_group_teen)

        response = self.client.get("/products/recommendation/?user_id={}".format(self.user.id))
        self.assertEqual(response.status_code, HTTP_200_OK)

        self.assertEqual(prev_product_id, response.data["id"])
