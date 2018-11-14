import os
from peewee import MySQLDatabase, SqliteDatabase


class ConfigBase(object):
    """
    Get's prods credentials from environment variables
    Yuck, but still safer than putting it in the file
    """

    DATABASE = MySQLDatabase('blog',
                             **{'charset': 'utf8',
                                'use_unicode': True,
                                'user': os.environ.get('BLOG_DB_USER'),
                                'passwd': os.environ.get('BLOG_DB_PASS')})

    EMAIL = {
        'username': os.environ.get('BLOG_EMAIL_USER'),
        'password': os.environ.get('BLOG_EMAIL_PASS')
    }


class Config(ConfigBase): pass

if 'DEVBOX' in os.environ:
    # Travis
    if os.environ['DEVBOX'] == 'travis':
        class Config(ConfigBase):
            DATABASE = MySQLDatabase(
                'blog',
                user='root',
                password='',
            )
    elif os.environ['DEVBOX'] != 'production':
        # Default mysql stuff
        class Config(ConfigBase):
            DATABASE = MySQLDatabase(
                'blog',
                user='root',
                password='',
            )
