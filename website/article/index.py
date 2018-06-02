#!/usr/bin/python3.6
from simplerr.web import web
from common.models.main import *

@web('/article/<link>', '/article/templates/article_layout.html')
def article(request, link):
    """Render article."""

    article = Article.get_article(link)

    previous_article = Article.select().where(Article.date < article.date, Article.wip == 'no') or [{'title': '', 'link': '#'}]
    next_article     = Article.select().where(Article.date > article.date, Article.wip == 'no') or [{'title': '', 'link': '#'}]

    return {
        'title'    : article.title,
        'article'  : article,
        'previous' : previous_article[-1:][0],
        'next'     : next_article[0]
    }
