#!/usr/env/bin python

from simplerr.web import web, GET

@web('/website/article/static/img/<path:file>', file=True)
def article_images(request, file):
    # Website route for article images so can see images on GitHub when previewing the markdown article
    return './article/static/img/' + file
