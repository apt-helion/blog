#!/usr/bin/python3.6
from simplerr.web import web

@web('/about', '/about/templates/about.html')
def about(request):
    return {'title': 'blag | about'}

