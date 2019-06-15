from simplerr.web import web
from common.models.main import Article


@web('/tag/<tag>', '/common/templates/archive.html')
def tag(request, tag):
    articles = [ a for a in Article.select().order_by(Article.date.desc()) if tag in a.tags ]

    return {
        'title': '#' + tag,
        'description': '',
        'articles': articles
    }
