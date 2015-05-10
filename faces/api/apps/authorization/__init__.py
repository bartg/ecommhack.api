# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
import tempfile
from faces.api.apps.images.models import ImageModel
from django.core import files


def facebook_download_image(profile_id):
    """

    :param profile_id: profile if of facebook user
    :return:
    """
    # Steam the image from the url
    image_url = 'http://graph.facebook.com/{0}/picture?width=500&height=500'.format(profile_id)
    request = requests.get(image_url, stream=True)

    # Was the request OK?
    if request.status_code != requests.codes.ok:
        # Nope, error handling, skip file etc etc etc
        return None

    # Get the filename from the url, used for saving later
    file_name = profile_id

    # Create a temporary file
    lf = tempfile.NamedTemporaryFile()

    # Read the streamed image in sections
    for block in request.iter_content(1024 * 8):

        # If no more file then stop
        if not block:
            break

        # Write image block to temporary file
        lf.write(block)

    # Create the model you want to save the image to
    image = ImageModel()

    # Save the temporary image to the model#
    # This saves the model so be sure that is it valid
    image.file.save(file_name, files.File(lf))
    return image