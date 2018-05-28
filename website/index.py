#!/usr/bin/python3.6
from simplerr.web import web

@web('/', '/index.html')
def index(request):
    """Render homepage."""
    return {'title': 'blag'}

@web('/favicon.ico', file=True)
def favicon(request):
    return "common/static/img/favicon.ico"
