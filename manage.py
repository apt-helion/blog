#!/usr/bin/env python
import sys
sys.path.append('./website/')
sys.path.append('./bin/')

import click

from os import environ
from simplerr import dispatcher
from config import Config

from updatedb import UpdateDB
from exist import Exist

from emailsubscribers import send_emails

from common.models.main import Article
from common.models.email import *

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
def createdb():
    Config.DATABASE.create_tables([ Article, Emails, EmailLogs, EmailVerifications ])


@cli.command()
def updatedb():
    n = UpdateDB.import_articles()

    # Things to do in production if theres a new article
    if environ.get('PRODUCTION') and n:
        # Send email
        articles = Article.select().orderby(Article.date.desc()).get()
        send_emails(article.link)
        # Update Exist custom tags
        Exist.update_exist_tags()


if __name__ == '__main__':
    cli()
