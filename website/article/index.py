#!/usr/bin/python3.6
from simplerr.web import web
from common.models.main import *

@web('/article/<name>', '/article/templates/article_layout.html')
def article(request, name):
    """Render article."""

    article = Article.get(Article.link == name, Article.wip == 'no')

    previous_article = Article.select().where(Article.date < article.date, Article.wip == 'no') or [{'title': '', 'link': '#'}]
    next_article     = Article.select().where(Article.date > article.date, Article.wip == 'no') or [{'title': '', 'link': '#'}]

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
        'articles'    : Article.select().where(Article.wip == 'no').order_by(Article.date.desc())
    }
