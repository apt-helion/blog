#!/usr/bin/python3.6
from simplerr.web import web
from common.models.main import *

@web('/article/<name>', '/article/templates/article_layout.html')
def article(request, name):
    """Render article."""

    article = Article.get(Article.link == name)

    previous_article = Article.select(fn.MIN(Article.id)).where(Article.id > article.id)
    next_article     = Article.select(fn.MAX(Article.id)).where(Article.id < article.id)

    return {
        'title'    : article.title,
        'article'  : article, 
        'previous' : previous_article, 
        'next'     : next_article
    }

@web('/article/wip', '/article/templates/wip.html')
def wip(request):
    from datetime import datetime

    article = {
        'date': datetime(1970, 1, 1),
        'title': 'WIP',
        'category': 'WIP',
        'link': 'wip',
        'thumbnail':
        'dual-parallax.jpg',
        'tags': 'wip,helpme,ohno'
    }

    return {
        'title'    : 'Work in progress',
        'article'  : article,
        'previous' : article,
        'next'     : article
    }
