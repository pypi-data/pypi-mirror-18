# vim: set fileencoding=utf-8:
#
# TODO:
# - reload data if file changes (all get() methods should check that).

import os
import sys
import yaml

from ardj.log import *
from ardj.util import utf, get_user_path


DEFAULT_PLAYLISTS = [{
    "name": "jingles",
    "labels": ["jingle"],
    "delay": 15,
}, {
    "name": "music",
    "labels": ["music"],
}]


class wrapper:
    """Wraps a dictionary for easier access."""
    def __init__(self, data, filename):
        """Initializes the instance without any checking."""
        self.data = data
        self.filename = filename

        self.playlists_mtime = None
        self.playlists_data = []

    def get(self, key, default=None, fail=False):
        """Returns the value of the specified key."""
        v = self.data.get(key, default)
        return v

    def getpath(self, key, default=None, fail=False):
        """Returns a path specified by key.

        The value returned by get() is processed with os.path.expanduser()
        which makes the ~/ prefix available."""
        value = self.get(key, default, fail=fail)
        if value:
            value = os.path.expanduser(value)
        return value

    def list(self):
        """Do not use."""
        return type(self.data) == list and self.data or []

    def has_key(self, key):
        data = self.data
        for key in key.split('/'):
            if type(data) != dict:
                return False
            if key not in data:
                return False
            data = data[key]
        return True

    def get_playlists(self):
        filename = os.path.join(get_config_dir(), 'playlist.yaml')
        if not os.path.exists(filename):
            log_warning("File {} not found, using built-in playlists.", utf(filename))
            return DEFAULT_PLAYLISTS

        stat = os.stat(filename)
        if self.playlists_mtime is None or self.playlists_mtime < stat.st_mtime:
            log_info("Reloading playlists from {}.", utf(filename))
            self.playlists_mtime = stat.st_mtime
            self.playlists_data = yaml.load(open(filename, 'r').read())
        return self.playlists_data

    def __getitem__(self, key):
        """A convenience wrapper.

        Equals to get(key, None)."""
        return self.get(key)

    def __repr__(self):
        """Dumps the data for debugging purposes."""
        return '<ardj.settings.wrapper data=%s>' % self.data


wrapper_instance = None


def get_config_dir():
    config_dir = os.path.expanduser(os.getenv("ARDJ_CONFIG_DIR", "~/.ardj"))
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        print "Created folder %s." % config_dir

    try:
        os.chmod(config_dir, 0750)
    except OSError, e:
        print >> sys.stderr, "Could not change permissions on %s: %s" % (config_dir, e)

    return config_dir


def load_data():
    """Returns the raw contents of the config file."""
    filename = get_user_path("config.yaml")
    if os.path.exists(filename):
        return yaml.load(open(filename, 'rb')), filename
    else:
        log_warning("config file {} not found", filename)
        return {}, None


def load(refresh=False):
    """Loads an object for accessing the config file.

    Instances are cached, subsequent calls will not cause the object to be
    reloaded."""
    global wrapper_instance
    if wrapper_instance is None or refresh:
        data, filename = load_data()
        log_debug("read config from {}", filename)
        wrapper_instance = wrapper(data, filename)
    return wrapper_instance


def get(key, default=None, fail=False):
    """get(k, v) <==> load().get(k, v)"""
    return load().get(key, default, fail=fail)


def get2(key1, key2, default=None, fail=False):
    x = load()
    return x.get(key1, x.get(key2, default, fail))


def get_int(key, default):
    value = get(key, default)
    if isinstance(value, (str, unicode)) and value.isdigit():
        value = int(value)

    if isinstance(value, int):
        return value

    return default


def getpath(key, default=None, fail=False):
    """getpath(k, v) <==> load().getpath(k, v)"""
    return load().getpath(key, default, fail=fail)


def getpath2(key1, key2, default=None, fail=False):
    x = load()
    return x.getpath(key1, x.getpath(key2, default, fail))
