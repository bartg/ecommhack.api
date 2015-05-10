# encoding: utf-8
from __future__ import absolute_import, unicode_literals
import logging

from rest_framework.status import HTTP_200_OK

from faces.api.apps.products.scripts import fetch_products
from faces.lib.tests.testcases import AuthenticatedAPITestCase, APITestCase


log = logging.getLogger(__name__)


class TestProductListResource(AuthenticatedAPITestCase):

    @APITestCase.vcr.use_cassette("api/product_list.yaml")
    def test_smoke(self):
        fetch_products.run(page_size=5, pages=1)

        response = self.client.get("/products/")
        self.assertEqual(response.status_code, HTTP_200_OK)

        self.assertEqual(len(response.data["results"]), 5)
        self.assertEqual(dict(response.data["results"][0]), {
            u'images': [{u'largeUrl': u'https://i3.ztat.net/large/BG/34/2B/00/A8/02/BG342B00A-802@1.1.jpg', u'mediumHdUrl': u'https://i3.ztat.net/detail_hd/BG/34/2B/00/A8/02/BG342B00A-802@1.1.jpg', u'orderNumber': 1, u'thumbnailHdUrl': u'https://i3.ztat.net/thumb_hd/BG/34/2B/00/A8/02/BG342B00A-802@1.1.jpg', u'mediumUrl': u'https://i3.ztat.net/detail/BG/34/2B/00/A8/02/BG342B00A-802@1.1.jpg', u'largeHdUrl': u'https://i3.ztat.net/large_hd/BG/34/2B/00/A8/02/BG342B00A-802@1.1.jpg', u'smallUrl': u'https://i3.ztat.net/catalog/BG/34/2B/00/A8/02/BG342B00A-802@1.1.jpg', u'type': u'UNSPECIFIED', u'smallHdUrl': u'https://i3.ztat.net/catalog_hd/BG/34/2B/00/A8/02/BG342B00A-802@1.1.jpg'}, {u'largeUrl': u'https://i2.ztat.net/large/BG/34/2B/00/A8/02/BG342B00A-802@2.1.jpg', u'mediumHdUrl': u'https://i2.ztat.net/detail_hd/BG/34/2B/00/A8/02/BG342B00A-802@2.1.jpg', u'orderNumber': 2, u'thumbnailHdUrl': u'https://i2.ztat.net/thumb_hd/BG/34/2B/00/A8/02/BG342B00A-802@2.1.jpg', u'mediumUrl': u'https://i2.ztat.net/detail/BG/34/2B/00/A8/02/BG342B00A-802@2.1.jpg', u'largeHdUrl': u'https://i2.ztat.net/large_hd/BG/34/2B/00/A8/02/BG342B00A-802@2.1.jpg', u'smallUrl': u'https://i2.ztat.net/catalog/BG/34/2B/00/A8/02/BG342B00A-802@2.1.jpg', u'type': u'UNSPECIFIED', u'smallHdUrl': u'https://i2.ztat.net/catalog_hd/BG/34/2B/00/A8/02/BG342B00A-802@2.1.jpg'}, {u'largeUrl': u'https://i1.ztat.net/large/BG/34/2B/00/A8/02/BG342B00A-802@3.1.jpg', u'mediumHdUrl': u'https://i1.ztat.net/detail_hd/BG/34/2B/00/A8/02/BG342B00A-802@3.1.jpg', u'orderNumber': 3, u'thumbnailHdUrl': u'https://i1.ztat.net/thumb_hd/BG/34/2B/00/A8/02/BG342B00A-802@3.1.jpg', u'mediumUrl': u'https://i1.ztat.net/detail/BG/34/2B/00/A8/02/BG342B00A-802@3.1.jpg', u'largeHdUrl': u'https://i1.ztat.net/large_hd/BG/34/2B/00/A8/02/BG342B00A-802@3.1.jpg', u'smallUrl': u'https://i1.ztat.net/catalog/BG/34/2B/00/A8/02/BG342B00A-802@3.1.jpg', u'type': u'UNSPECIFIED', u'smallHdUrl': u'https://i1.ztat.net/catalog_hd/BG/34/2B/00/A8/02/BG342B00A-802@3.1.jpg'}, {u'largeUrl': u'https://i6.ztat.net/large/BG/34/2B/00/A8/02/BG342B00A-802@4.1.jpg', u'mediumHdUrl': u'https://i6.ztat.net/detail_hd/BG/34/2B/00/A8/02/BG342B00A-802@4.1.jpg', u'orderNumber': 4, u'thumbnailHdUrl': u'https://i6.ztat.net/thumb_hd/BG/34/2B/00/A8/02/BG342B00A-802@4.1.jpg', u'mediumUrl': u'https://i6.ztat.net/detail/BG/34/2B/00/A8/02/BG342B00A-802@4.1.jpg', u'largeHdUrl': u'https://i6.ztat.net/large_hd/BG/34/2B/00/A8/02/BG342B00A-802@4.1.jpg', u'smallUrl': u'https://i6.ztat.net/catalog/BG/34/2B/00/A8/02/BG342B00A-802@4.1.jpg', u'type': u'UNSPECIFIED', u'smallHdUrl': u'https://i6.ztat.net/catalog_hd/BG/34/2B/00/A8/02/BG342B00A-802@4.1.jpg'}, {u'largeUrl': u'https://i5.ztat.net/large/BG/34/2B/00/A8/02/BG342B00A-802@5.1.jpg', u'mediumHdUrl': u'https://i5.ztat.net/detail_hd/BG/34/2B/00/A8/02/BG342B00A-802@5.1.jpg', u'orderNumber': 5, u'thumbnailHdUrl': u'https://i5.ztat.net/thumb_hd/BG/34/2B/00/A8/02/BG342B00A-802@5.1.jpg', u'mediumUrl': u'https://i5.ztat.net/detail/BG/34/2B/00/A8/02/BG342B00A-802@5.1.jpg', u'largeHdUrl': u'https://i5.ztat.net/large_hd/BG/34/2B/00/A8/02/BG342B00A-802@5.1.jpg', u'smallUrl': u'https://i5.ztat.net/catalog/BG/34/2B/00/A8/02/BG342B00A-802@5.1.jpg', u'type': u'UNSPECIFIED', u'smallHdUrl': u'https://i5.ztat.net/catalog_hd/BG/34/2B/00/A8/02/BG342B00A-802@5.1.jpg'}, {u'largeUrl': u'https://i4.ztat.net/large/BG/34/2B/00/A8/02/BG342B00A-802@6.1.jpg', u'mediumHdUrl': u'https://i4.ztat.net/detail_hd/BG/34/2B/00/A8/02/BG342B00A-802@6.1.jpg', u'orderNumber': 6, u'thumbnailHdUrl': u'https://i4.ztat.net/thumb_hd/BG/34/2B/00/A8/02/BG342B00A-802@6.1.jpg', u'mediumUrl': u'https://i4.ztat.net/detail/BG/34/2B/00/A8/02/BG342B00A-802@6.1.jpg', u'largeHdUrl': u'https://i4.ztat.net/large_hd/BG/34/2B/00/A8/02/BG342B00A-802@6.1.jpg', u'smallUrl': u'https://i4.ztat.net/catalog/BG/34/2B/00/A8/02/BG342B00A-802@6.1.jpg', u'type': u'UNSPECIFIED', u'smallHdUrl': u'https://i4.ztat.net/catalog_hd/BG/34/2B/00/A8/02/BG342B00A-802@6.1.jpg'}, {u'largeUrl': u'https://i3.ztat.net/large/BG/34/2B/00/A8/02/BG342B00A-802@7.1.jpg', u'mediumHdUrl': u'https://i3.ztat.net/detail_hd/BG/34/2B/00/A8/02/BG342B00A-802@7.1.jpg', u'orderNumber': 7, u'thumbnailHdUrl': u'https://i3.ztat.net/thumb_hd/BG/34/2B/00/A8/02/BG342B00A-802@7.1.jpg', u'mediumUrl': u'https://i3.ztat.net/detail/BG/34/2B/00/A8/02/BG342B00A-802@7.1.jpg', u'largeHdUrl': u'https://i3.ztat.net/large_hd/BG/34/2B/00/A8/02/BG342B00A-802@7.1.jpg', u'smallUrl': u'https://i3.ztat.net/catalog/BG/34/2B/00/A8/02/BG342B00A-802@7.1.jpg', u'type': u'UNSPECIFIED', u'smallHdUrl': u'https://i3.ztat.net/catalog_hd/BG/34/2B/00/A8/02/BG342B00A-802@7.1.jpg'}],
            u'price': u'41.00',
            u'brand': u'Bagheera',
            u'name': u'Base layer - black',
            u'id': 1
        })
