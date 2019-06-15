#!/usr/bin/env python
import sys
import click

from os import environ
from simplerr import dispatcher
from peewee import OperationalError

sys.path.insert(0, './website/')
from common.loadenv import LoadEnv  # noqa
LoadEnv.load_dot_env()


def create_app(site, hostname='127.0.0.1', port=5000, *args, **kwargs):
    from common.database import DATABASE

    wsgi = dispatcher.wsgi(
        site, hostname, port,
        **kwargs
    )

    @wsgi.pre_response
    def db_connect(request):
        restart = False
        try:
            DATABASE.connect()
        except OperationalError:
            restart = True

        if restart:
            try:
                DATABASE.close()
                DATABASE.connect()
            except Exception:
                pass


    @wsgi.post_response
    def db_close(request, response):
        try:
            DATABASE.close()
        except Exception:
            pass


    @wsgi.post_exception
    def db_close_exception(request, error):
        try:
            DATABASE.close()
        except Exception:
            pass

    return wsgi


@click.group()
def cli():
    pass


@cli.command()
@click.option('-s', '--site', type=str, default='./website/', help='/app_path')
@click.option('-h', '--hostname', type=str, default='127.0.0.1', help="127.0.0.1")
@click.option('-p', '--port', type=int, default=5000, help="5000")
@click.option('--reloader', is_flag=True, default=True)
@click.option('--debugger', is_flag=True)
@click.option('--processes', type=int, default=1, help="1")
@click.option('--evalex',  default=False, is_flag=True)
def runserver(site, hostname, port, reloader, debugger, processes, evalex):
    app = create_app(site, hostname, port, reloader, debugger, evalex, processes)
    app.serve()


@cli.command()
def createdb():
    from common.database import DATABASE
    from common.models.main import Article
    from common.models.email import Emails, EmailLogs

    DATABASE.create_tables([ Article, Emails, EmailLogs ])


@cli.command()
def updatedb():
    sys.path.insert(0, './bin/')

    from updatedb import UpdateDB
    from exist import Exist
    from emailsubscribers import send_emails
    from common.models.main import Article

    new_article = UpdateDB.import_articles()

    # Things to do in production if theres a new article
    if environ.get('PRODUCTION') and new_article:
        # Send email
        article = Article.get_latest()
        send_emails(article.link)
        # Update Exist custom tags
        Exist.update_exist_tags()


@cli.command()
def tests():
    sys.path.insert(0, './tests/')
    from tests import test_processor

    tester = test_processor()
    tester.run()


@cli.command()
@click.option('-m', '--module', multiple=True, default=None)
def runtest(module):
    sys.path.insert(0, './tests/')
    from tests import test_processor

    tester = test_processor()
    tester.modules = module or tester.modules
    tester.run()


if __name__ == '__main__':
    cli()
