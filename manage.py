#!/usr/bin/env python
import sys

sys.path.append('./website/')
sys.path.append('./bin/')
sys.path.append('./tests/')

import click

from os import environ
from simplerr import dispatcher
from config import Config

from updatedb import UpdateDB
from exist import Exist

from emailsubscribers import send_emails

from common.models.main import Article
from common.models.email import *

from tests import test_processor

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
@click.option('--evalex',  default=False, is_flag=True)
def runserver(site, hostname, port, reloader, debugger, evalex):
    """Start a new development server."""

    app = dispatcher.wsgi(
        site, hostname, port,
        use_reloader=reloader,
        use_debugger=debugger,
        use_evalex=evalex,
        threaded=True,
        processes=1
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
        article = Article.get_latest()
        send_emails(article.link)
        # Update Exist custom tags
        Exist.update_exist_tags()


@cli.command()
def tests():
    tester = test_processor()
    tester.run()


@cli.command()
@click.option('-m', '--module', multiple=True, default=None)
def runtest(module):
    tester = test_processor()
    tester.modules = module or tester.modules
    tester.run()


if __name__ == '__main__':
    cli()
