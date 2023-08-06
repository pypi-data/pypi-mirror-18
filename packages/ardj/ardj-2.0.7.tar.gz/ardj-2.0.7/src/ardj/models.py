# encoding=utf-8

"""
Database models for ARDJ.
"""

import random
import time
import urllib

from ardj import config
from ardj.database import connect
from ardj.log import *
from ardj.util import format_duration, utf
import ardj.tags


RECENT_SECONDS = 2 * 3600


class Model(dict):
    table_name = None
    fields = ()
    key_name = None

    @classmethod
    def get_by_id(cls, id):
        fields_sql = ", ".join(cls.fields)
        sql = "SELECT %s FROM %s WHERE %s = ? LIMIT 1" % (fields_sql, cls.table_name, cls.key_name)
        rows = cls._fetch_rows(sql, (id, ))
        if rows:
            return rows[0]

    @classmethod
    def find_all(cls):
        fields_sql = ", ".join(cls.fields)
        sql = "SELECT %s FROM %s" % (fields_sql, cls.table_name)
        return cls._fetch_rows(sql, ())

    @classmethod
    def _fetch_rows(cls, sql, params):
        rows = connect().fetch(sql, params)
        return [cls._from_row(row) for row in rows]

    @classmethod
    def _from_row(cls, row):
        pairs = [(name, row[idx]) for idx, name in enumerate(cls.fields)]
        return cls(dict(pairs))

    @classmethod
    def _fields_sql(cls):
        return ", ".join(cls.fields)

    @classmethod
    def delete_all(cls):
        """Deletes all records from the table."""
        return connect().execute("DELETE FROM %s" % cls.table_name, ())

    def delete(self):
        sql = "DELETE FROM %s WHERE %s = ?" % (self.table_name, self.key_name)
        connect().execute(sql, (self[self.key_name], ))
        self[self.key_name] = None

    def put(self, force_insert=False):
        if self.get(self.key_name) is None or force_insert:
            return self._insert(force_insert)
        return self._update()

    def _insert(self, with_key=False):
        if with_key:
            fields = self.fields
        else:
            fields = [f for f in self.fields if f != self.key_name]
        fields_sql = ", ".join(fields)
        params_sql = ", ".join(["?"] * len(fields))

        sql = "INSERT INTO %s (%s) VALUES (%s)" % (self.table_name, fields_sql, params_sql)
        params = [self.get(field) for field in fields]

        self[self.key_name] = connect().execute(sql, params)
        return self[self.key_name]

    def _update(self):
        fields = [f for f in self.fields if f != self.key_name]
        fields_sql = ", ".join(["%s = ?" % field for field in fields])

        sql = "UPDATE %s SET %s WHERE %s = ?" % (self.table_name, fields_sql, self.key_name)
        params = [self.get(field) for field in fields] + [self[self.key_name]]

        return connect().execute(sql, params)


class Vote(Model):
    """Stores information about votes."""
    table_name = "votes"
    fields = ("track_id", "email", "vote", "ts")

    def get_date(self):
        """Returns a formatted date for this vote."""
        return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(self["ts"]))


class Track(Model):
    """Stores information about a track."""
    table_name = "tracks"
    fields = ("id", "artist", "title", "filename", "length", "weight", "real_weight", "count", "last_played", "owner", "image", "download")
    key_name = "id"

    @classmethod
    def find_all(cls, deleted=False):
        """Returns all tracks with positive weight."""
        sql = "SELECT %s FROM %s" % (cls._fields_sql(), cls.table_name)
        if not deleted:
            sql += " WHERE weight > 0"
        return cls._fetch_rows(sql, ())

    @classmethod
    def find_by_tag(cls, tag):
        """Returns tracks that have a specific tag."""
        sql = "SELECT %s FROM %s WHERE weight > 0 AND id IN (SELECT track_id FROM labels WHERE label = ?)" % (cls._fields_sql(), cls.table_name)
        return cls._fetch_rows(sql, (tag, ))

    @classmethod
    def find_by_url(cls, url):
        """Returns all tracks with the specified download URL."""
        sql = "SELECT %s FROM %s WHERE `download` = ?" % (cls._fields_sql(), cls.table_name)
        return cls._fetch_rows(sql, (url, ))

    @classmethod
    def find_active(cls):
        """Returns tracks which weren't deleted."""
        sql = "SELECT %s FROM %s WHERE `weight` > 0" % (cls._fields_sql(), cls.table_name)
        return cls._fetch_rows(sql, ())

    @classmethod
    def find_recently_played(cls, count=50):
        """Returns a list of recently played tracks."""
        sql = "SELECT %s FROM %s ORDER BY `last_played` DESC LIMIT %u" % (cls._fields_sql(), cls.table_name, count)
        return cls._fetch_rows(sql, ())

    @classmethod
    def get_queue(cls):
        ids = [q["track_id"] for q in Queue.find_all()]
        return [cls.get_by_id(id) for id in ids]

    @classmethod
    def get_artist_names(cls):
        """Returns all artist names."""
        return connect().fetchcol("SELECT DISTINCT artist FROM %s" % self.table_name)

    @classmethod
    def rename_artist(cls, old_name, new_name):
        """Renames an artist."""
        sql = "UPDATE %s SET artist = ? WHERE artist = ?" % (self.table_name, new_name, old_name)
        connect().execute(sql, ())

    @classmethod
    def find_without_lastfm_tags(cls):
        sql = "SELECT %s FROM %s WHERE weight > 0 AND id NOT IN (SELECT track_id FROM labels WHERE label LIKE 'lastfm:%%') ORDER BY id" % (cls._fields_sql(), cls.table_name)
        return cls._fetch_rows(sql, ())

    @classmethod
    def find_tags(cls, min_count=5, cents=100):
        sql = "SELECT label, COUNT(*) FROM labels WHERE track_id IN (SELECT id FROM tracks WHERE weight > 0) GROUP BY label ORDER BY label"
        rows = [row for row in connect().fetch(sql) if row[1] >= min_count and ":" not in row[0] and len(row[0]) > 1]
        return rows

    def get_labels(self):
        if not self.get(self.key_name):
            return []
        if "labels" not in self:
            self["labels"] = connect().fetchcol("SELECT label FROM labels WHERE track_id = ?", (self[self.key_name], ))
        return self["labels"] or []

    def set_labels(self, labels):
        if type(labels) != list:
            raise TypeError("Labels must be a list.")

        db = connect()
        db.execute("DELETE FROM labels WHERE track_id = ?", (self["id"], ))
        for tag in list(set(labels)):
            db.execute("INSERT INTO labels (track_id, label, email) VALUES (?, ?, ?)", (self["id"], tag, "unknown", ))

        log_debug("New labels for track {}: {}", self["id"], utf(labels))

    def set_image(self, url):
        connect().execute("UPDATE tracks SET image = ? WHERE id = ?", (url, self["id"], ))

    def set_download(self, url):
        connect().execute("UPDATE tracks SET download = ? WHERE id = ?", (url, self["id"], ))

    def get_artist_url(self):
        if "lastfm:noartist" in self.get_labels():
            return None
        v = urllib.quote(utf(self["artist"]))
        return "http://www.last.fm/music/%s" % v

    def get_track_url(self):
        if "lastfm:notfound" in self.get_labels():
            return None

        def q(v):
            return urllib.quote(utf(v))

        return "http://www.last.fm/music/%s/_/%s" % (q(self["artist"]), q(self["title"]))

    @classmethod
    def get_average_length(cls):
        """Returns average track length in minutes."""
        s_prc = s_qty = 0.0
        for prc, qty in connect().fetch("SELECT ROUND(length / 60) AS r, COUNT(*) FROM tracks GROUP BY r"):
            s_prc += prc * qty
            s_qty += qty
        return int(s_prc / s_qty * 60 * 1.5)

    def get_votes(self):
        """Returns track votes."""
        result = {}
        for email, vote in connect().fetch("SELECT email, vote FROM votes WHERE track_id = ? ORDER BY ts", (self["id"], )):
            result[email] = vote
        return result

    @classmethod
    def from_file(cls, filename, labels=None):
        """Creates a new track from file, saves it.  If no labels were
        specified, adds the default ones."""
        # FIXME: здесь этому не место
        filepath = os.path.join(config.get_path("musicdir"), filename)
        tags = ardj.tags.get(filepath)

        t = cls(filename=filename.decode("utf-8"))
        if "length" not in tags:
            raise Exception("No length in %s" % filename)
        t["artist"] = tags.get("artist", "Unknown Artist")
        t["title"] = tags.get("title", os.path.basename(filename).decode("utf-8"))
        t["length"] = tags["length"]
        t["weight"] = 1.0
        t["real_weight"] = 1.0
        t.put()

        if labels is None:
            labels = config.get("default_labels")
        if labels:
            t.set_labels(labels)

        return t

    @classmethod
    def find_all_playlists(cls, count):
        sql = "SELECT %s FROM %s WHERE weight > 0 ORDER BY artist, title" % (cls._fields_sql(), cls.table_name)
        params = []
        return cls._fetch_rows(sql, params)

    @classmethod
    def query(cls, playlist=None, artist=None, tag=None, count=100):
        sql = "SELECT %s FROM %s WHERE weight > 0" % (cls._fields_sql(), cls.table_name)
        params = []
        order = "artist, title"

        if not playlist or playlist == "all":
            pass
        elif playlist == "never":
            sql += " AND last_played IS NULL"
        elif playlist == "recent":
            ts = time.time() - RECENT_SECONDS
            sql += " AND last_played > ?"
            params.append(int(ts))
            order = "last_played DESC"
        else:
            sql += " AND id IN (SELECT track_id FROM labels WHERE label = ?)"
            params.append(playlist)

        if artist and artist != "All artists":
            sql += " AND artist = ?"
            params.append(artist)

        if tag and tag != "All tags":
            sql += " AND id IN (SELECT track_id FROM labels WHERE label = ?)"
            params.append(tag)

        sql += " ORDER BY %s" % order

        if count:
            sql += " LIMIT %u" % count

        return cls._fetch_rows(sql, params)

    def queue(self, owner=None):
        """Adds track to queue."""
        q = Queue()
        q["track_id"] = self["id"]
        q["owner"] = owner
        q.put()

    def rocks(self, login):
        pass  # see tracks.add_vote

    def sucks(self, login):
        pass

    def for_template(self):
        t = dict(self)
        t["labels"] = self.get_labels()
        if self["length"]:
            t["duration"] = format_duration(self["length"])
        return t


class Queue(Model):
    """Stores information about a track to play out of regular order."""
    table_name = "queue"
    fields = "id", "track_id", "owner"
    key_name = "id"


class Token(Model):
    table_name = "tokens"
    fields = "token", "login", "login_type", "active"
    key_name = "token"

    @classmethod
    def create(cls, email, active=0):
        db = connect()

        while True:
            tmp = random.randrange(111111, 999999)
            rows = db.fetchone("SELECT 1 FROM tokens WHERE token = ?", (tmp, ))
            if rows is not None:
                continue

            db.execute("INSERT INTO tokens (token, login, login_type, active) VALUES (?, ?, 'email', ?)", (tmp, email, active))

            return cls(token=tmp,
                login=email,
                login_type="email",
                active=active)


class Label(Model):
    table_name = "labels"
    fields = ("track_id", "email", "label")

    @classmethod
    def delete_by_name(cls, name):
        connect().execute("DELETE FROM `%s` WHERE `label` = ?" % cls.table_name, (name, ))

    @classmethod
    def find_all_names(cls):
        rows = connect().fetch("SELECT DISTINCT label FROM labels WHERE track_id IN (SELECT id FROM tracks WHERE weight > 0) ORDER BY label")
        return [r[0] for r in rows]

    @classmethod
    def find_never_played_names(cls):
        rows = connect().fetch("SELECT DISTINCT label FROM labels WHERE track_id IN (SELECT id FROM tracks WHERE weight > 0 AND last_played IS NULL) ORDER BY label")
        return [r[0] for r in rows]

    @classmethod
    def find_recently_played_names(cls):
        limit = time.time() - RECENT_SECONDS
        rows = connect().fetch("SELECT DISTINCT label FROM labels WHERE track_id IN (SELECT id FROM tracks WHERE weight > 0 AND last_played > ?) ORDER BY label", (limit, ))
        return [r[0] for r in rows]

    @classmethod
    def find_crossing_names(cls, name):
        rows = connect().fetch("SELECT DISTINCT label FROM labels WHERE track_id IN (SELECT id FROM tracks INNER JOIN labels l ON l.track_id = tracks.id WHERE weight > 0 AND l.label = ?)", (name, ))
        return [r[0] for r in rows]

    @classmethod
    def query_names(cls, playlist=None, artist=None):
        sql = "SELECT DISTINCT label FROM labels WHERE 1"
        params = []

        if playlist == "all":
            pass
        elif playlist == "never":
            sql += " AND track_id IN (SELECT id FROM tracks WHERE weight > 0 AND last_played IS NULL)"
        elif playlist == "recent":
            ts = time.time() - RECENT_SECONDS
            sql += " AND track_id IN  (SELECT id FROM tracks WHERE weight > 0 AND last_played > ?)"
            params.append(int(ts))
        else:
            sql += " AND track_id IN (SELECT id FROM tracks INNER JOIN labels l ON l.track_id = tracks.id WHERE weight > 0 AND l.label = ?)"
            params.append(playlist)

        if not artist or artist == "All artists":
            pass
        else:
            sql += " AND track_id IN (SELECT id FROM tracks WHERE weight > 0 AND artist = ?)"
            params.append(artist)

        sql += " ORDER BY label"

        return [r[0] for r in connect().fetch(sql, params)]


class Artist(Model):
    """A virtual model without a table."""
    fields = ("name", )

    @classmethod
    def query(cls, playlist=None, tag=None):
        sql = "SELECT DISTINCT artist FROM tracks WHERE weight > 0"
        params = []

        if playlist == "all":
            pass
        elif playlist == "never":
            sql += " AND last_played IS NULL"
        elif playlist == "recent":
            sql += " AND last_played >= ?"
            params.append(time.time() - RECENT_SECONDS)
        else:
            sql += " AND id IN (SELECT track_id FROM labels WHERE label = ?)"
            params.append(playlist)

        if tag and tag != "All tags":
            sql += " AND id IN (SELECT track_id FROM labels WHERE label = ?)"
            params.append(tag)

        sql += " ORDER BY artist"
        return cls._fetch_rows(sql, params)

    @classmethod
    def query_all(cls):
        sql = "SELECT DISTINCT artist FROM tracks WHERE weight > 0 ORDER BY artist"
        return cls._fetch_rows(sql, ())

    @classmethod
    def find_unplayed(cls):
        sql = "SELECT DISTINCT artist FROM tracks WHERE weight > 0 AND last_played IS NULL ORDER BY artist"
        return cls._fetch_rows(sql, ())

    @classmethod
    def find_recent(cls):
        limit = time.time() - RECENT_SECONDS
        sql = "SELECT DISTINCT artist FROM tracks WHERE weight > 0 AND last_played > ? ORDER BY artist"
        return cls._fetch_rows(sql, (limit, ))

    @classmethod
    def find_by_tag(cls, tag):
        sql = "SELECT DISTINCT artist FROM tracks WHERE weight > 0 AND id IN (SELECT track_id FROM labels WHERE label = ?) ORDER BY artist"
        return cls._fetch_rows(sql, (tag, ))
