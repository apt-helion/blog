#!/usr/bin/python3.6
from simplerr.web import web
from common.auth import Auth

@web('/', '/home.html')
def home(request):
    """Render homepage."""
    return {'current': 'home'}

@web('/favicon.ico', file=True)
def favicon(request):
    return "common/static/img/favicon.ico"
