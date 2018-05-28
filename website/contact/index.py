#!/usr/bin/python3.6
from simplerr.web import web

@web('/contact', '/contact/templates/contact.html')
def contact(request):
    return {'title': 'blag | contact'}

