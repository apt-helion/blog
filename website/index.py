#!/usr/bin/python3.6
import uuid
import random

from simplerr.web import web, GET, POST
from common.models.main import *
from common.models.email import EmailVerifications


@web('/', '/index.html')
def index(request):
    """Render homepage."""
    return {
        'title'          : 'blog',
        'infosec'        : Article.get_category('infosec').order_by(Article.date.desc()).limit(3),
        'development'    : Article.get_category('development').order_by(Article.date.desc()).limit(3),
        'engineering'    : Article.get_category('engineering').order_by(Article.date.desc()).limit(3),
        'miscellaneous'  : Article.get_category('miscellaneous').order_by(Article.date.desc()).limit(3),
        'latest'         : list(Article.get_category())[-1]
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

    if category == 'archive':
        title = 'Archive'
        description = 'All my articles.'
        articles = Article.get_category().order_by(Article.date.desc())
    else:
        articles = Article.get_category(category).order_by(Article.date.desc())

    return {
        'title'       : title,
        'description' : description,
        'articles'    : articles
    }


@web('/about', '/about.html')
def about(request): pass


@web('/contact', '/contact.html')
def contact(request): pass


@web('/404', '/404.html')
def error404(request): pass


@web('/favicon.ico', file=True)
def favicon(request):
    return "./common/static/img/favicon.ico"
