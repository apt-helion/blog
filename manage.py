#!/usr/bin/env python
"""Simplerr Configuration."""
import sys
sys.path.append('./website/')
import click
import os
from simplerr import dispatcher
from playhouse.dataset import DataSet
from website.config import Config
from website.common.models import main

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
    app = dispatcher.wsgi(site, hostname, port,
                          use_reloader=reloader,
                          use_debugger=debugger,
                          use_evalex=evalex,
                          threaded=threaded,
                          processes=processes)  # ssl_context=(crt, key)

    app.serve()

@cli.command()
def sqlite_init():
    # Delete old database if exists
    try:
        os.remove("website/pplsrv.db")
        print("Existing database deleted")
    except FileNotFoundError:
        print("No existing database found")

    # Create new database from model
    Config.DATABASE.create_tables(main.BaseModel.__subclasses__())
    print("New database created")

    # Add test data from JSONs
    db = DataSet('sqlite:///website/pplsrv.db')
    for table in db.tables:
        db[table].thaw(format='json',
                       filename='./migration/test_data/' + table + '.json')
    print("Database populated with test data")
    print("Database setup complete!")


@cli.command()
def dbexport():
    """
    Export a MySQL db records to JSON files.
    Before running, modify db declaration to reflect your MySQL server
    Example: 'mysql://root:Blockers12@localhost/pplsrv'
    To run do `./manage.py dbexport`.
    To generate a peewee model from a MySQL DB, use the following bash command:
    python -m pwiz -e mysql -H localhost -u root -P pplsrv > model.py
    Then enter the MySQL password
    """
    # Exports all tables in MySQL db
    data_set = DataSet('mysql://root:Blockers12@localhost/pplsrv')
    for table in data_set.tables:
        data_set.freeze(data_set[table], format='json',
                  filename='./migration/test_data/' + table + '.json')

if __name__ == '__main__':
    cli()
