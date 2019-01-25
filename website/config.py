import os
from peewee import MySQLDatabase

from common.loadenv import LoadEnv
LoadEnv.load_dot_env()

class Config(object):

    DATABASE = MySQLDatabase('blog', **{
        'charset'     : 'utf8',
        'use_unicode' : True,
        'user'        : os.environ.get('DB_USER', ''),
        'passwd'      : os.environ.get('DB_PASS', '')
    })

    EMAIL = {
        'username': os.environ.get('EMAIL_USER'),
        'password': os.environ.get('EMAIL_PASS')
    }
