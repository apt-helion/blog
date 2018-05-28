#!/usr/bin/python3.6
from simplerr.web import web
from common.models.main import *

@web('/article/<name>', '/article/templates/article_template.html')
def article(request, name):
    """Render article."""

    article = Article.get(Article.title == name)

    previous_article = Article.select(fn.MIN(Article.id)).where(Article.id > article.id)
    next_article     = Article.select(fn.MAX(Article.id)).where(Article.id < article.id)

    return {
        'title'    : name, 
        'article'  : article, 
        'previous' : previous_article, 
        'next'     : next_article
    }

@web('/article/wip', '/article/templates/wip.html')
def wip(request):
    return {'title': 'Work in progress'}