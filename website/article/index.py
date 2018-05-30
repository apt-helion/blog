#!/usr/bin/python3.6
from simplerr.web import web
from common.models.main import *

@web('/article/<name>', '/article/templates/article_layout.html')
def article(request, name):
    """Render article."""

    article = Article.get(Article.link == name)

    previous_article = Article.select().where(Article.id < article.id) or [{'title': '', 'link': '#'}]
    next_article     = Article.select().where(Article.id > article.id) or [{'title': '', 'link': '#'}]

    return {
        'title'    : article.title,
        'article'  : article, 
        'previous' : previous_article[-1:][0],
        'next'     : next_article[0]
    }

@web('/article', '/common/templates/archive.html')
def article_archive(request):
    return {
        'title'       : 'Archive',
        'description' : 'All my articles.',
        'articles'    : Article.select().order_by(Article.id.desc())
    }

@web('/article/wip', '/article/templates/wip.html')
def wip(request):
    from datetime import datetime

    article = {
        'date': datetime(1970, 1, 1),
        'title': 'WIP',
        'category': 'WIP',
        'link': 'wip',
        'thumbnail': 'dual-parallax.jpg',
        'tags': 'wip,helpme,ohno'
    }

    return {
        'title'    : 'Work in progress',
        'article'  : article,
        'previous' : article,
        'next'     : article
    }
