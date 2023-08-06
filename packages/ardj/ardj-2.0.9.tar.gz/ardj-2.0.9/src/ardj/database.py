# vim: set ts=4 sts=4 sw=4 et fileencoding=utf-8:
#
# database related functions for ardj.
#
# ardj is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# ardj is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""ARDJ, an artificial DJ.

This module contains the database related code.
"""

import os
import sys

try:
    from sqlite3 import dbapi2 as sqlite
    from sqlite3 import OperationalError
except ImportError:
    print >> sys.stderr, 'Please install pysqlite2.'
    sys.exit(13)

from ardj import get_data_path
from ardj import config
from ardj.log import *
from ardj.util import utf, get_user_path
import ardj.util


class database:
    """
    Interface to the database.
    """
    instance = None

    def __init__(self, filename):
        """
        Opens the database, creates tables if necessary.
        """
        self.filename = filename
        try:
            self.db = sqlite.connect(self.filename, check_same_thread=False)
        except Exception, e:
            log_error('Could not open database {}: {}', utf(filename), e)
            raise

        self.db.create_collation('UNICODE', ardj.util.ucmp)
        self.db.create_function('ULIKE', 2, self.sqlite_ulike)

    def __del__(self):
        self.commit()
        log_debug('Database closed.')

    @classmethod
    def get_instance(cls):
        path = config.get_path("database_path")
        if cls.instance is None:
            cls.instance = cls(path)
        return cls.instance

    def sqlite_ulike(self, a, b):
        if a is None or b is None:
            return None
        if ardj.util.lower(b) in ardj.util.lower(a):
            return 1
        return 0

    def cursor(self):
        """Returns a new SQLite cursor, for internal use."""
        return self.db.cursor()

    def commit(self):
        """Commits current transaction, for internal use. """
        self.db.commit()

    def rollback(self):
        """Cancel pending changes."""
        # log_debug("Rolling back a transaction.")
        self.db.rollback()

    def fetch(self, sql, params=None):
        return self.execute(sql, params, fetch=True)

    def fetchone(self, sql, params=None):
        result = self.fetch(sql, params)
        if result:
            return result[0]

    def fetchcol(self, sql, params=None):
        """Returns a list of first column values."""
        rows = self.fetch(sql, params)
        if rows:
            return [row[0] for row in rows]

    def fetch_row(self, sql, params=None):
        res = self.fetch(sql, params)
        if res:
            return res[0]

    def fetch_cell(self, sql, params=None):
        res = self.fetch_row(sql, params)
        if result:
            return result[0]

    def execute(self, sql, params=None, fetch=False):
        cur = self.db.cursor()
        try:
            args = [sql]
            if params is not None:
                args.append(params)
            cur.execute(*args)
            if fetch:
                return cur.fetchall()
            elif sql.startswith("INSERT "):
                return cur.lastrowid
            else:
                return cur.rowcount
        except:
            log_exception("Failed SQL statement: {}, params: {}", utf(sql), utf(params))
            raise
        finally:
            cur.close()

    def update(self, table, args):
        """Performs update on a label.

        Updates the table with values from the args dictionary, key "id" must
        identify the record.  Example:

        db.update('tracks', {'weight': 1, 'id': 123})
        """
        sql = []
        params = []
        for k in args:
            if k != 'id':
                sql.append(k + ' = ?')
                params.append(args[k])
        params.append(args['id'])

        self.execute('UPDATE %s SET %s WHERE id = ?' % (table, ', '.join(sql)), tuple(params))

    def debug(self, sql, params, quiet=False):
        """Logs the query in human readable form.

        Replaces question marks with parameter values (roughly)."""
        for param in params:
            param = unicode(param)
            if param.isdigit():
                sql = sql.replace(u'?', param, 1)
            else:
                sql = sql.replace(u'?', u"'" + param + u"'", 1)
        log_debug("SQL: {}", utf(sql))
        return sql

    def purge(self):
        """
        Removes stale data.

        Stale data in queue items, labels and votes linked to tracks that no
        longer exist.  In addition to deleting such links, this function also
        analyzed all tables (to optimize indexes) and vacuums the database.
        """
        old_size = os.stat(self.filename).st_size
        for table in ('playlists', 'tracks', 'queue', 'urgent_playlists', 'labels', 'karma'):
            self.execute('ANALYZE ' + table)
        self.execute('VACUUM')
        log_info('{} bytes saved after database purge.', os.stat(self.filename).st_size - old_size)


def connect():
    """Returns the active database instance."""
    return database.get_instance()


def commit():
    connect().commit()


def rollback():
    connect().rollback()


def cmd_console(*args):
    """Open database console (sqlite3)"""
    from subprocess import Popen

    Popen(["sqlite3", "-header", connect().filename]).wait()


def cmd_init():
    """
    Initialize the database

    Initializes the configured database by executing a set of preconfigured SQL
    instructions.  This is non-destructive.  You should run this after you
    empty the database.
    """

    db = connect()

    log_info("Checking database integrity...")
    with open(get_data_path("sqlite_init.sql"), "rb") as f:
        for line in f.readlines():
            if line.startswith("--"):
                continue

            elif not line.strip():
                continue

            try:
                db.execute(line)
            except:
                log_error("Init statement failed: {}", line)
                raise

    db.commit()


def cmd_purge():
    """Delete stale data"""
    db = connect()
    db.purge()
    db.commit()
