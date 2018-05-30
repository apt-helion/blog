#!/usr/bin/python3.6
import os
import datetime

from simplerr.web import web
from common.models.main import *

def prod_check():
    """Check if we are in production environment."""
    if 'DEVBOX' in os.environ:
        if os.environ['DEVBOX'] == 'PROD': return False
    return True

@web('/admin', '/admin/templates/admin.html', GET)
def admin(request):
    if not prod_check(): return

    if request.args.get('delete'):
        article = Article.get(Article.link == request.args.get('delete'))
        article.delete_instance()

    return {'articles': Article.select()}

@web('/admin', '/admin/templates/admin.html', POST)
def admin(request):
    if not prod_check(): return

    if request.form.get('createnew'):
        Article.create(Article.link == request.form.get('link')).save()
        # To do: redirect

    return {'articles': Article.select()}

@web('/admin/edit_article/<link>', '/admin/templates/edit_article.html')
def edit_article(request, link):
    if not prod_check(): return

    if request.form.get('save'):
        (Article
            .update(
                link=request.form.get('link'),
                title=request.form.get('title'),
                date=request.form.get('date', datetime.datetime.now),
                category=request.form.get('category'),
                content=request.form.get('content'),
                thumbnail=request.form.get('thumbnail'),
                tags=request.form.get('tags')
            )
            .where(Article.link == link)
            .execute()
        )

    if request.form.get('publish'):
        Article.update(wip='no', date=datetime.datetime.now).where(Article.link == link).execute()

    return {'article': Article.get(Article.link == link)}

@web('/admin/view_article/<name>', '/article/templates/article_layout.html')
def view_article(request, name):
    if not prod_check(): return

    article = Article.get(Article.link == name)

    previous_article = Article.select().where(Article.date < article.date, Article.wip == 'no') or [{'title': '', 'link': '#'}]
    next_article     = Article.select().where(Article.date > article.date, Article.wip == 'no') or [{'title': '', 'link': '#'}]

    return {
        'title'    : article.title,
        'article'  : article, 
        'previous' : previous_article[-1:][0],
        'next'     : next_article[0]
    }