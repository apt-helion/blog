#!/usr/bin/env python

import os

from playhouse.pool import PooledDatabase
from peewee import MySQLDatabase, OperationalError


class PooledConnection(PooledDatabase, MySQLDatabase):

    def execute_sql(self, *args, **kwargs):
        """
        Overwritting `execute_sql` to prevent `Error 2006: MySQL server has gone away`.

        If there's an error in execution, the connection is probably dead so we close the
        connection (not returning it to the pool), make a new one, and execute it again.
        """
        try:
            return super().execute_sql(*args, **kwargs)
        except OperationalError:
            self.manual_close()
            self.connect()
            return super().execute_sql(*args, **kwargs)

    def _is_closed(self, conn):
        """
        Taken from original `playhouse.pool.PooledMySQLDatabase` class.

        Not sure what it's for. I think it may trying to solve the same issue our `execute_sql` function,
        but the ping function isn't working correctly. As in, if you ping a dead connection, it should
        return an error, but it doesn't. No idea why.
        """
        is_closed = super()._is_closed(conn)

        if not is_closed:
            try:
                conn.ping(False)
            except Exception:
                is_closed = True

        return is_closed


DATABASE = PooledConnection(
    'blog',
    max_connections=15,
    timeout=60,
    stale_timeout=60, **{
        'host': os.environ.get('DB_HOST') or '127.0.0.1',
        'user': os.environ.get('DB_USER') or 'root',
        'passwd': os.environ.get('DB_PASS', ''),
        'port': int(os.environ.get('DB_PORT') or 3306),
    }
)


class dba(object):
    """Simple Database Access Layer for MySQLdb"""

    database = DATABASE

    @staticmethod
    def _query(query, params):
        cursor = dba.database.cursor()
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
