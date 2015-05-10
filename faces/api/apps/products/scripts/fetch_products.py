# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging

from faces.api.apps.products.models import ProductModel

from faces.lib.zalando_api.api import ZalandoAPI


log = logging.getLogger(__name__)


def run(pages=50, page_size=100):
    zalando_api = ZalandoAPI()

    num_created = 0

    pages = zalando_api.articles.get(page_size=page_size, pages=pages)
    for page in pages:
        for article in page:
            # only create if product has images
            if article["media"]["images"]:
                product, created = ProductModel.from_zalando_article(article)
                num_created += int(created)

    log.info("Created {} products".format(num_created))
