#!/usr/bin/python3.6
from simplerr.web import web
from common.models.main import *

@web('/', '/index.html')
def index(request):
    """Render homepage."""

    sec = (Article
           .select()
           .where(Article.category == 'infosec', Article.wip == 'no')
           .order_by(Article.date.desc())
           .limit(3))

    dev = (Article
           .select()
           .where(Article.category == 'development', Article.wip == 'no')
           .order_by(Article.date.desc())
           .limit(3))

    eng = (Article
           .select()
           .where(Article.category == 'engineering', Article.wip == 'no')
           .order_by(Article.date.desc())
           .limit(3))

    misc = (Article
            .select()
            .where(Article.category == 'miscellaneous', Article.wip == 'no')
            .order_by(Article.date.desc())
            .limit(3))

    return {
        'title'          : 'blag',
        'infosec'        : sec,
        'development'    : dev,
        'engineering'    : eng,
        'misecellaneous' : misc,
        'random'         : Article.select().where(Article.wip == 'no').order_by(fn.Rand())[0]
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

    else: return {'redirect': '/404'}

    articles = Article.select().where(Article.category == category, Article.wip == 'no').order_by(Article.date.desc())

    return {
        'title'       : title,
        'description' : description,
        'articles'    : articles
    }

@web('/archive', '/common/templates/archive.html')
def archive(request):
    return {
        'title'       : 'Archive',
        'description' : 'All my articles.',
        'articles'    : Article.select().where(Article.wip == 'no').order_by(Article.date.desc())
    }

@web('/404', '/404.html')
def error404(request):
    return {}

@web('/favicon.ico', file=True)
def favicon(request):
    return "./common/static/img/favicon.ico"
