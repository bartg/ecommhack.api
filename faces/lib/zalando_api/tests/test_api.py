# encoding: utf-8
from __future__ import absolute_import, unicode_literals
import logging

from django.test.testcases import TestCase
from faces.lib.tests.testcases import APITestCase

from faces.lib.zalando_api.api import ZalandoAPI


log = logging.getLogger(__name__)


class TestZalandoAPI(TestCase):

    def setUp(self):
        super(TestZalandoAPI, self).setUp()
        self.api = ZalandoAPI()

    @APITestCase.vcr.use_cassette('zalando_api/articles.yaml')
    def test_articles(self):
        articles = [article for page in self.api.articles.get(pages=2, page_size=5) for article in page]
        log.info(articles)
        self.assertEqual(len(articles), 10)
