#!/usr/bin/python3.6
from simplerr.web import web

@web('/article/<name>', '/article/templates/article_template.html')
def article(request, name):
    """Render article."""
    return {'title': name, 'article': 'hello'}
