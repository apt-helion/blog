#!/usr/bin/env python
import sys
sys.path.append('./website/')
sys.path.append('./bin/')

import click

from os import environ
from simplerr import dispatcher
from updatedb import UpdateDB
from emailsubscribers import send_emails
from common.models.main import Article

"""
Example usage
./manage.py runserver
"""

@click.group()
def cli(): pass

@cli.command()
@click.option('-s', '--site', type=str, default='./website/', help='/app_path')
@click.option('-h', '--hostname', type=str, default='127.0.0.1', help="127.0.0.1")
@click.option('-p', '--port', type=int, default=5000, help="5000")
@click.option('--reloader', is_flag=True, default=True)
@click.option('--debugger', is_flag=True)
@click.option('--evalex', is_flag=True, default=False)
@click.option('--threaded', is_flag=True)
@click.option('--processes', type=int, default=1, help="1")
def runserver(site, hostname, port, reloader, debugger, evalex, threaded, processes):
    """Start a new development server."""

    app = dispatcher.wsgi(
        site, hostname, port,
        use_reloader=reloader,
        use_debugger=debugger,
        use_evalex=evalex,
        threaded=threaded,
        processes=processes
    )

    app.serve()


@cli.command()
def updatedb():
    new_article = UpdateDB.import_articles()

    # Send email if new article
    if environ.get('PRODUCTION') and new_article:
        articles = Article.select().orderby(Article.date.desc()).get()
        send_emails(article.link)


if __name__ == '__main__':
    cli()
