#!/usr/bin/python3.6
from simplerr.web import web
from common.models.main import *


@web('/tag/<tag>', '/tag/templates/tag.html')
def tag(request, tag):

    articles = [a for a in Article.select().order_by(Article.id.desc()) if tag in a.tags]

    return {
        'title'       : tag,
        'articles'    : articles
    }


