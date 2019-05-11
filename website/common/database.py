#!/usr/bin/env python

import os
import MySQLdb

from .loadenv import LoadEnv
LoadEnv.load_dot_env()


class dba(object):
    """Simple Database Access Layer for MySQLdb"""

    _connection = MySQLdb.connect(**{
        'host':   os.environ.get('DB_HOST') or '127.0.0.1',
        'user':   os.environ.get('DB_USER') or 'root',
        'passwd': os.environ.get('DB_PASS', ''),
        'port':   int(os.environ.get('DB_PORT')) or 3306,
        'db':     'blog'
    })

    @staticmethod
    def _query(query, params):
        cursor = dba._connection.cursor()
        cursor.execute(query, params)

        return cursor


    @staticmethod
    def scalar(query, params):
        cursor = dba._query(query, params)

        rows = cursor.fetchone() or None

        if isinstance(rows, tuple):
            return rows[0]
        else:
            return None


    @staticmethod
    def dict(query, params):
        cursor = dba._query(query, params)

        columns = [col[0] for col in cursor.description]
        rows    = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return rows


    @staticmethod
    def empty(query, params):
        last_id   = None
        row_count = None

        cursor = dba._query(query, params)

        last_id   = cursor.lastrowid
        row_count = cursor.rowcount

        return last_id, row_count
