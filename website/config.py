import os

from peewee import MySQLDatabase
from common.loadenv import LoadEnv

LoadEnv.load_dot_env()


class Config(object):

    DATABASE = MySQLDatabase('blog', **{
        'charset':     'utf8',
        'use_unicode': True,

        'host':   os.environ.get('DB_HOST') or '127.0.0.1',
        'user':   os.environ.get('DB_USER') or 'root',
        'passwd': os.environ.get('DB_PASS', ''),
        'port':   int(os.environ.get('DB_PORT') or 3306)
    })

    EMAIL = {
        'username': os.environ.get('EMAIL_USER'),
        'password': os.environ.get('EMAIL_PASS')
    }

    EXIST = { 'token': os.environ.get('EXIST_TOKEN') }
