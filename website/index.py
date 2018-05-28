#!/usr/bin/python3.6
from simplerr.web import web
from common.models.main import *

@web('/', '/index.html')
def index(request):
    """Render homepage."""

    sec = (Article
           .select()
           .where(Article.category == 'infosec')
           .order_by(Article.id.desc())
           .limit(3))

    dev = (Article
           .select()
           .where(Article.category == 'development')
           .order_by(Article.id.desc())
           .limit(3))


    misc = (Article
            .select()
            .where(Article.category == 'miscellaneous')
            .order_by(Article.id.desc())
            .limit(3))

    return {
        'title'          : 'blag',
        'infosec'        : sec,
        'development'    : dev,
        'misecellaneous' : misc
    }

@web('/<category>', '/common/templates/archive.html')
def archive(request, category):
    if category == 'infosec':
        title = 'Information Security'
        description = 'hello'

    elif category == 'development':
        title = 'Software Development'
        description = 'hello'

    elif category == 'miscellaneous':
        title = 'Miscellaneous'
        description = 'hello'

    else: pass # redirect 404

    articles = Article.select().where(Article.category == category)

    return {
        'title'       : title,
        'description' : description,
        'articles'    : articles
    }

@web('/favicon.ico', file=True)
def favicon(request):
    return "common/static/img/favicon.ico"
