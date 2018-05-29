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

    eng = (Article
           .select()
           .where(Article.category == 'engineering')
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
        'engineering'    : eng,
        'misecellaneous' : misc,
        'random'         : Article.select().order_by(fn.Rand())[0]
    }

@web('/<category>', '/common/templates/archive.html')
def archive(request, category):
    if category == 'infosec':
        title = 'Information Security'
        description = 'I attempt CTF walkthroughs, infosec \'research\', and you read about it.'

    elif category == 'development':
        title = 'Software Development'
        description = 'I write software and you read about it.'

    elif category == 'engineering':
        title = 'Engineering'
        description = 'I build stuff and you read about it.'

    elif category == 'miscellaneous':
        title = 'Miscellaneous'
        description = 'I look at other stuff and you read about it.'

    else: pass # redirect 404

    articles = Article.select().where(Article.category == category).order_by(Article.id.desc())

    return {
        'title'       : title,
        'description' : description,
        'articles'    : articles
    }

@web('/favicon.ico', file=True)
def favicon(request):
    return "./common/static/img/favicon.ico"
