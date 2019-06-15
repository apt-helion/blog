#!/usr/bin/python3.6
from simplerr.web import web, GET
from common.models.main import Article


@web('/', '/common/templates/index.html', GET)
def index(request):
    return {
        'title': 'blog',
        'infosec': Article.get_category('infosec').order_by(Article.date.desc()).limit(3),
        'development': Article.get_category('development').order_by(Article.date.desc()).limit(3),
        'engineering': Article.get_category('engineering').order_by(Article.date.desc()).limit(3),
        'miscellaneous': Article.get_category('miscellaneous').order_by(Article.date.desc()).limit(3),
        'latest': Article.get_latest()
    }


@web('/<category>', '/common/templates/archive.html', GET)
def archive(request, category):
    hash_map = {
        'infosec': {
            'title': 'Information Security',
            'description': 'I attempt CTF walkthroughs, infosec \'research\', and you read about it.',
        },
        'development': {
            'title': 'Software Development',
            'description': 'I write software and you read about it.',
        },
        'engineering': {
            'title': 'Engineering',
            'description': 'I build stuff and you read about it.',
        },
        'miscellaneous': {
            'title': 'Miscellaneous',
            'description': 'I look at other stuff and you read about it.',
        },
        'archive': {
            'title': 'Archive',
            'description': 'All my articles.',
        }
    }

    cat = hash_map.get(category, web.redirect('/404'))

    if isinstance(cat, dict):
        cat['articles'] = Article.get_category(category).order_by(Article.date.desc())

    return cat


@web('/about', '/common/templates/about.html', GET)
def about(request):
    pass


@web('/contact', '/common/templates/contact.html', GET)
def contact(request):
    pass


@web('/404', '/common/templates/404.html', GET)
def error404(request):
    pass


@web('/robots.txt', file=True)
def robots(request):
    return "./common/static/robots.txt"


@web('/favicon.ico', file=True)
def favicon(request):
    return "./common/static/img/favicon.ico"
